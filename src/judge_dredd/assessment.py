from sqlalchemy import select
from sqlalchemy.orm import Session
from .models import Case, Evidence, Assertion, Charge

VALID_ASSERTION_STATUSES = {"alleged", "disputed", "court_established", "researcher_claim"}

def inventory(db: Session, case_id: str) -> dict:
    case = db.get(Case, case_id)
    if case is None:
        raise LookupError(case_id)
    assertions = db.scalars(select(Assertion).where(Assertion.case_id == case_id)).all()
    evidence = db.scalars(select(Evidence).where(Evidence.case_id == case_id)).all()
    charges = db.scalars(select(Charge).where(Charge.case_id == case_id)).all()
    if any(a.status not in VALID_ASSERTION_STATUSES for a in assertions):
        raise ValueError("Unknown assertion status")
    return {
        "case_id": case.id,
        "status": "HUMAN_REVIEW_REQUIRED",
        "finding": None,
        "guilt_probability": None,
        "severity_msu": None,
        "risk_score": None,
        "disclaimer": "Evidence inventory only. No calibrated guilt probability, moral score, or court verdict.",
        "charges": [{"id": c.id, "law_reference": c.law_reference, "status": c.status,
                     "legal_elements": c.legal_elements} for c in charges],
        "assertions": [{"text": a.text, "status": a.status, "evidence_id": a.evidence_id,
                        "source_url": a.evidence.source_url, "pinpoint": a.evidence.pinpoint} for a in assertions],
        "evidence_count": len(evidence),
        "unverified_evidence_count": sum(e.source_status != "verified" for e in evidence),
        "limitations": ["Source verification and charge-element analysis are not automated in MVP."]
    }
