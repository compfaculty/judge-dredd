"""Offline, atomic import of a curated case; never downloads arbitrary URLs."""
import hashlib
import json
from importlib.resources import files
from io import BytesIO

from pypdf import PdfReader
from sqlalchemy.orm import Session

from .db import SessionLocal, init_db
from .models import (
    Assessment, Assertion, AuditEvent, Case, Charge, CourtJudgment,
    Event, Evidence, ModelVersion, SourceSnapshot,
)

CASE_ID = "us-eichman-1990"
MODEL_VERSION = "curated-inventory-v1"


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical(data: dict) -> bytes:
    return json.dumps(data, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode()


def extract_pages(pdf: bytes, expected_sha256: str) -> list[dict]:
    if len(pdf) > 5_000_000 or digest(pdf) != expected_sha256:
        raise ValueError("Source PDF size/hash mismatch")
    reader = PdfReader(BytesIO(pdf), strict=True)
    if len(reader.pages) != 15:
        raise ValueError("Unexpected source pagination")
    pages = []
    for number, page in enumerate(reader.pages, 1):
        text = page.extract_text()
        if not text or not text.strip():
            raise ValueError(f"No extractable text on PDF page {number}; OCR review required")
        pages.append({"pdf_page": number, "reporter_page": 309 + number, "text": text})
    return pages


def import_first_case(db: Session) -> str:
    """Caller owns commit/rollback. Existing imports are checked, never overwritten."""
    root = files("judge_dredd").joinpath("data/eichman")
    raw = root.joinpath("case.json").read_bytes()
    data = json.loads(raw)
    pdf = root.joinpath("opinion.pdf").read_bytes()
    pages = extract_pages(pdf, data["source"]["sha256"])
    input_hash = digest(raw)
    existing = db.get(Case, CASE_ID)
    if existing:
        snapshot = db.get(Assessment, CASE_ID + "-initial")
        if snapshot is None or snapshot.report.get("input_sha256") != input_hash:
            raise ValueError("Existing case differs from this import; explicit revision required")
        return CASE_ID

    # References are checked before any database mutation, including on SQLite.
    refs = {r["id"]: r for r in data["evidence"]}
    if len(refs) != len(data["evidence"]):
        raise ValueError("Duplicate evidence ID")
    for ref in refs.values():
        page = ref["pdf_page"]
        if not 1 <= page <= len(pages) or not ref["pinpoint"]:
            raise ValueError("Invalid evidence anchor")
        # Small extraction anchors detect accidental wrong-page mappings, not factual truth.
        if ref["anchor"] not in pages[page - 1]["text"]:
            raise ValueError(f"Extraction anchor missing: {ref['id']}")
    for assertion in data["assertions"]:
        if assertion["evidence_id"] not in refs or assertion["status"] not in {
            "alleged", "disputed", "court_established", "researcher_claim"
        }:
            raise ValueError("Invalid assertion provenance/status")
    for row in data["coverage"]:
        if any(ref not in refs for ref in row["evidence_ids"]):
            raise ValueError("Invalid coverage provenance")
    for event in data["timeline"]:
        if event["evidence_id"] not in refs:
            raise ValueError("Invalid timeline provenance")
    if data["judgment"]["evidence_id"] not in refs:
        raise ValueError("Invalid judgment provenance")

    db.add(Case(id=CASE_ID, title=data["title"], jurisdiction="United States (federal)",
                procedural_status="closed_section_700_charge", is_synthetic=False))
    db.flush()
    source = {**data["source"], "extraction": "pypdf " + __import__("pypdf").__version__,
              "extraction_review": "Page anchors checked; not independently reviewed",
              "translation": "English original; editorial summaries in English"}
    db.add(SourceSnapshot(id=CASE_ID + "-source", case_id=CASE_ID,
                          metadata_record=source, pages=pages))
    for ref in refs.values():
        db.add(Evidence(id=ref["id"], case_id=CASE_ID, kind=ref["kind"],
                        description=ref["description"], source_url=source["url"],
                        source_document_id=source["document_id"], pinpoint=ref["pinpoint"],
                        source_status="verified"))
    db.flush()
    for i, assertion in enumerate(data["assertions"]):
        db.add(Assertion(id=f"{CASE_ID}-a{i}", case_id=CASE_ID, **assertion))
    db.add(Charge(id=CASE_ID + "-charge", case_id=CASE_ID,
                  law_reference=data["law_reference"], allegation=data["allegation"],
                  legal_elements=[r["element"] for r in data["coverage"]], status="dismissed"))
    for i, event in enumerate(data["timeline"]):
        db.add(Event(id=f"{CASE_ID}-event{i}", case_id=CASE_ID, event_date=event["date"],
                     description=event["description"], source_evidence_id=event["evidence_id"]))
    judgment = data["judgment"]
    db.add(CourtJudgment(id=CASE_ID + "-judgment", case_id=CASE_ID,
                         court="Supreme Court of the United States", decision_date="1990-06-11",
                         disposition=judgment["disposition"], appeal_status=judgment["appeal_status"],
                         source_evidence_id=judgment["evidence_id"]))
    if db.get(ModelVersion, MODEL_VERSION) is None:
        db.add(ModelVersion(id=MODEL_VERSION, validation_status="unvalidated_curated_inventory",
                            definition={"method": "Human-authored source mappings; no predictive model",
                                        "guilt_probability": None, "severity_msu": None}))
    report = {
        "case_id": CASE_ID, "status": "HUMAN_REVIEW_REQUIRED", "finding": None,
        "guilt_probability": None, "severity_msu": None, "risk_score": None,
        "model_version": MODEL_VERSION, "input_sha256": input_hash,
        "source": source, "evidence_inventory": data["evidence"],
        "assertions": data["assertions"], "charge_element_coverage": data["coverage"],
        "law_reference": data["law_reference"], "timeline": data["timeline"],
        "evidence_count": len(refs), "unverified_evidence_count": 0,
        "assessment": data["assessment"], "limitations": data["limitations"],
        "evaluation": {"blinded": False, "reason": "Curated from outcome-bearing judicial opinion; outcome known at authoring"},
        "review_form": {"opinions": ["agree", "disagree", "need_more_evidence", "abstain"],
                        "required": ["reviewer", "opinion", "rationale", "assessment_id"],
                        "prompt": "Review the inventory and limitations, not a model verdict."},
        "disclaimer": "Non-binding research inventory. No calibrated probabilities or MSU; no autonomous verdict.",
    }
    report_hash = digest(canonical(report))
    assessment_id = CASE_ID + "-initial"
    db.add(Assessment(id=assessment_id, case_id=CASE_ID, model_version=MODEL_VERSION, report=report))
    db.add(AuditEvent(id=CASE_ID + "-import", case_id=CASE_ID, action="case_imported_and_assessment_frozen",
                      payload={"assessment_id": assessment_id, "report_sha256": report_hash,
                               "input_sha256": input_hash, "source_sha256": source["sha256"],
                               "blinded": False}))
    db.flush()
    return CASE_ID


def main():
    init_db()
    with SessionLocal.begin() as db:
        case_id = import_first_case(db)
    print(f"Imported/verified {case_id}; HUMAN_REVIEW_REQUIRED")


if __name__ == "__main__":
    main()
