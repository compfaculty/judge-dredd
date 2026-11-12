import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from judge_dredd.db import Base
from judge_dredd.models import Case, Evidence, Assertion, Charge
from judge_dredd.assessment import inventory

@pytest.fixture
def db():
    engine = create_engine("sqlite+pysqlite:///:memory:")
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        session.add(Case(id="c", title="Test", is_synthetic=True))
        session.add(Evidence(id="e", case_id="c", kind="doc", description="test", source_status="unverified"))
        session.add(Assertion(id="a", case_id="c", evidence_id="e", text="Alleged", status="alleged"))
        session.add(Charge(id="q", case_id="c", law_reference="TEST", allegation="Test charge", legal_elements=[]))
        session.commit()
        yield session
    engine.dispose()

def test_no_guilt_inference(db):
    result = inventory(db, "c")
    assert result["status"] == "HUMAN_REVIEW_REQUIRED"
    assert result["guilt_probability"] is None
    assert result["severity_msu"] is None
    assert result["assertions"][0]["status"] == "alleged"
    assert result["unverified_evidence_count"] == 1

def test_unknown_case(db):
    with pytest.raises(LookupError):
        inventory(db, "missing")
