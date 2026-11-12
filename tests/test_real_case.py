import hashlib
from importlib.resources import files

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, func, select
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from judge_dredd.api import app
from judge_dredd.db import Base, get_db
from judge_dredd.import_case import CASE_ID, canonical, extract_pages, import_first_case
from judge_dredd.models import Assessment, AuditEvent, Case, HumanReview, SourceSnapshot


@pytest.fixture
def db():
    engine = create_engine("sqlite://", poolclass=StaticPool, connect_args={"check_same_thread": False})
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        import_first_case(session)
        session.commit()
        yield session
    engine.dispose()


@pytest.fixture
def client(db):
    def dependency():
        yield db
    app.dependency_overrides[get_db] = dependency
    # No lifespan: avoid touching the user's default database.
    client = TestClient(app)
    try:
        yield client
    finally:
        client.close()
    app.dependency_overrides.clear()


def test_import_is_real_idempotent_and_frozen(db):
    assert db.get(Case, CASE_ID).is_synthetic is False
    report = db.get(Assessment, CASE_ID + "-initial").report
    import_first_case(db)
    db.commit()
    assert db.scalar(select(func.count()).select_from(Assessment)) == 1
    assert db.scalar(select(func.count()).select_from(AuditEvent)) == 1
    audit = db.get(AuditEvent, CASE_ID + "-import")
    assert audit.payload["report_sha256"] == hashlib.sha256(canonical(report)).hexdigest()
    source = db.get(SourceSnapshot, CASE_ID + "-source")
    assert len(source.pages) == 15
    assert source.pages[4]["reporter_page"] == 314
    assert "worn or soiled" in source.pages[4]["text"]
    assert "Affirmed." in source.pages[9]["text"]
    assert report["evaluation"]["blinded"] is False
    assert report["finding"] is report["guilt_probability"] is report["severity_msu"] is None
    assert report["assessment"]["conclusion"] == "ABSTAIN_ON_FACTUAL_GUILT"
    refs = {e["id"] for e in report["evidence_inventory"]}
    assert all(a["evidence_id"] in refs for a in report["assertions"])
    assert report["assertions"][0]["status"] == "alleged"
    assert any(a["status"] == "disputed" for a in report["assertions"])
    assert all(set(row["evidence_ids"]) <= refs for row in report["charge_element_coverage"])
    assert any("89-1434" in limitation for limitation in report["limitations"])


def test_source_tampering_rejected():
    pdf = files("judge_dredd").joinpath("data/eichman/opinion.pdf").read_bytes()
    with pytest.raises(ValueError, match="hash mismatch"):
        extract_pages(pdf + b"tampered", hashlib.sha256(pdf).hexdigest())


def test_conflicting_import_rejected(db):
    assessment = db.get(Assessment, CASE_ID + "-initial")
    assessment.report = {**assessment.report, "input_sha256": "bad"}
    db.flush()
    with pytest.raises(ValueError, match="explicit revision"):
        import_first_case(db)


def test_complete_review_workflow(client, db):
    base = f"/cases/{CASE_ID}"
    report = client.get(base + "/assessment").json()
    assert report["assessment_id"] == CASE_ID + "-initial"
    assert client.get(base + "/review").status_code == 200
    assert "textContent" in client.get(base + "/review").text
    assert client.get(base + "/sources/5").json()["reporter_page"] == 314
    assert client.get(base + "/sources/0").status_code == 404
    assert client.get(base + "/sources/16").status_code == 404
    official = client.get(base + "/judgments").json()[0]
    assert "affirmed" in official["disposition"]
    assert official["pinpoint"]
    payload = dict(reviewer="researcher", opinion="abstain", rationale="Need trial exhibits",
                   assessment_id=report["assessment_id"])
    assert client.post(base + "/reviews", json=payload).status_code == 201
    assert client.get(base + "/reviews").json()[0]["rationale"] == "Need trial exhibits"
    assert db.scalar(select(func.count()).select_from(HumanReview)) == 1
    assert client.get(base + "/assessment").json() == report
    assert db.scalar(select(func.count()).select_from(AuditEvent)) == 2


def test_review_cannot_reference_other_case(client, db):
    db.add(Case(id="other", title="Other"))
    db.commit()
    payload = dict(reviewer="r", opinion="agree", rationale="x", assessment_id=CASE_ID + "-initial")
    assert client.post("/cases/other/reviews", json=payload).status_code == 422
    payload["assessment_id"] = "missing"
    assert client.post(f"/cases/{CASE_ID}/reviews", json=payload).status_code == 422
    payload["assessment_id"] = None
    assert client.post(f"/cases/{CASE_ID}/reviews", json=payload).status_code == 422
    payload["opinion"] = "guilty"
    assert client.post(f"/cases/{CASE_ID}/reviews", json=payload).status_code == 422
    payload.update(opinion="abstain", reviewer="   ")
    assert client.post(f"/cases/{CASE_ID}/reviews", json=payload).status_code == 422
    assert db.scalar(select(func.count()).select_from(HumanReview)) == 0
