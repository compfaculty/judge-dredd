from uuid import uuid4
from importlib.resources import files
from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy import select
from sqlalchemy.orm import Session
from .db import get_db, init_db
from .models import Case, HumanReview, AuditEvent, Assessment, CourtJudgment, Evidence, SourceSnapshot
from .schemas import ReviewInput
from .assessment import inventory

app = FastAPI(title="Judge Dredd — Research Prototype", version="0.1.0")

@app.on_event("startup")
def startup():
    init_db()

@app.get("/health")
def health():
    return {"status": "ok", "mode": "research_only"}

@app.get("/cases")
def list_cases(db: Session = Depends(get_db)):
    cases = db.scalars(select(Case).order_by(Case.id)).all()
    return [{"id": c.id, "title": c.title, "procedural_status": c.procedural_status,
             "is_synthetic": c.is_synthetic} for c in cases]

@app.get("/cases/{case_id}")
def get_case(case_id: str, db: Session = Depends(get_db)):
    c = db.get(Case, case_id)
    if not c:
        raise HTTPException(status_code=404, detail="Case not found")
    return {"id": c.id, "title": c.title, "jurisdiction": c.jurisdiction,
            "procedural_status": c.procedural_status, "subject_id": c.subject_id,
            "is_synthetic": c.is_synthetic}

@app.get("/cases/{case_id}/assessment")
def get_assessment(case_id: str, db: Session = Depends(get_db)):
    snapshot = db.scalar(select(Assessment).where(Assessment.case_id == case_id).order_by(Assessment.created_at, Assessment.id))
    if snapshot:
        return {**snapshot.report, "assessment_id": snapshot.id, "frozen_at": snapshot.created_at.isoformat()}
    try:
        return inventory(db, case_id)
    except LookupError:
        raise HTTPException(status_code=404, detail="Case not found")

@app.post("/cases/{case_id}/reviews", status_code=201)
def post_review(case_id: str, data: ReviewInput, db: Session = Depends(get_db)):
    if db.get(Case, case_id) is None:
        raise HTTPException(status_code=404, detail="Case not found")
    if data.assessment_id:
        assessment = db.get(Assessment, data.assessment_id)
        if assessment is None or assessment.case_id != case_id:
            raise HTTPException(status_code=422, detail="Assessment does not belong to this case")
    elif db.scalar(select(Assessment.id).where(Assessment.case_id == case_id)):
        raise HTTPException(status_code=422, detail="assessment_id required for a frozen case review")
    review_id = str(uuid4())
    db.add(HumanReview(id=review_id, case_id=case_id, **data.model_dump()))
    db.add(AuditEvent(id=str(uuid4()), case_id=case_id, action="human_review_created",
                      payload={"review_id": review_id, "opinion": data.opinion,
                               "reviewer": data.reviewer, "assessment_id": data.assessment_id}))
    db.commit()
    return {"id": review_id, "case_id": case_id, "recorded": True,
            "note": "Researcher feedback, not an official court judgment."}


@app.get("/cases/{case_id}/review", response_class=HTMLResponse)
def review_page(case_id: str, db: Session = Depends(get_db)):
    if db.get(Case, case_id) is None:
        raise HTTPException(status_code=404, detail="Case not found")
    return files("judge_dredd").joinpath("review.html").read_text()


@app.get("/cases/{case_id}/sources/{page_number}")
def source_page(case_id: str, page_number: int, db: Session = Depends(get_db)):
    source = db.scalar(select(SourceSnapshot).where(SourceSnapshot.case_id == case_id))
    if source is None or not 1 <= page_number <= len(source.pages):
        raise HTTPException(status_code=404, detail="Source page not found")
    return {"source": source.metadata_record, **source.pages[page_number - 1]}


@app.get("/cases/{case_id}/judgments")
def judgments(case_id: str, db: Session = Depends(get_db)):
    if db.get(Case, case_id) is None:
        raise HTTPException(status_code=404, detail="Case not found")
    rows = db.scalars(select(CourtJudgment).where(CourtJudgment.case_id == case_id).order_by(CourtJudgment.id)).all()
    result = []
    for row in rows:
        evidence = db.get(Evidence, row.source_evidence_id)
        result.append({"court": row.court, "decision_date": row.decision_date,
                       "disposition": row.disposition, "appeal_status": row.appeal_status,
                       "source_evidence_id": row.source_evidence_id,
                       "source_url": evidence.source_url, "pinpoint": evidence.pinpoint})
    return result


@app.get("/cases/{case_id}/reviews")
def reviews(case_id: str, db: Session = Depends(get_db)):
    if db.get(Case, case_id) is None:
        raise HTTPException(status_code=404, detail="Case not found")
    rows = db.scalars(select(HumanReview).where(HumanReview.case_id == case_id).order_by(HumanReview.created_at, HumanReview.id)).all()
    return [{"id": row.id, "assessment_id": row.assessment_id, "reviewer": row.reviewer,
             "opinion": row.opinion, "rationale": row.rationale,
             "created_at": row.created_at.isoformat()} for row in rows]
