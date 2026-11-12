from datetime import datetime, timezone
from sqlalchemy import String, Text, ForeignKey, DateTime, Float, Integer, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .db import Base

def utcnow():
    return datetime.now(timezone.utc)

class Subject(Base):
    __tablename__ = "subjects"
    id: Mapped[str] = mapped_column(String(80), primary_key=True)
    display_name: Mapped[str] = mapped_column(String(300))
    kind: Mapped[str] = mapped_column(String(40), default="person")
    is_synthetic: Mapped[bool] = mapped_column(default=False)

class Case(Base):
    __tablename__ = "cases"
    id: Mapped[str] = mapped_column(String(80), primary_key=True)
    title: Mapped[str] = mapped_column(String(400))
    jurisdiction: Mapped[str | None] = mapped_column(String(160), nullable=True)
    procedural_status: Mapped[str] = mapped_column(String(80), default="unknown")
    is_synthetic: Mapped[bool] = mapped_column(default=False)
    subject_id: Mapped[str | None] = mapped_column(ForeignKey("subjects.id"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    subject = relationship("Subject")
    evidence = relationship("Evidence", back_populates="case")
    assertions = relationship("Assertion", back_populates="case")

class Event(Base):
    __tablename__ = "events"
    id: Mapped[str] = mapped_column(String(80), primary_key=True)
    case_id: Mapped[str] = mapped_column(ForeignKey("cases.id"))
    event_date: Mapped[str | None] = mapped_column(String(30), nullable=True)
    description: Mapped[str] = mapped_column(Text)
    source_evidence_id: Mapped[str | None] = mapped_column(ForeignKey("evidence.id"), nullable=True)

class Charge(Base):
    __tablename__ = "charges"
    id: Mapped[str] = mapped_column(String(80), primary_key=True)
    case_id: Mapped[str] = mapped_column(ForeignKey("cases.id"))
    law_reference: Mapped[str] = mapped_column(String(500))
    allegation: Mapped[str] = mapped_column(Text)
    legal_elements: Mapped[list] = mapped_column(JSON, default=list)
    status: Mapped[str] = mapped_column(String(60), default="alleged")

class Evidence(Base):
    __tablename__ = "evidence"
    id: Mapped[str] = mapped_column(String(80), primary_key=True)
    case_id: Mapped[str] = mapped_column(ForeignKey("cases.id"))
    kind: Mapped[str] = mapped_column(String(60))
    description: Mapped[str] = mapped_column(Text)
    source_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    source_document_id: Mapped[str | None] = mapped_column(String(300), nullable=True)
    pinpoint: Mapped[str | None] = mapped_column(String(200), nullable=True)
    source_status: Mapped[str] = mapped_column(String(80), default="unverified")
    case = relationship("Case", back_populates="evidence")

class Assertion(Base):
    __tablename__ = "assertions"
    id: Mapped[str] = mapped_column(String(80), primary_key=True)
    case_id: Mapped[str] = mapped_column(ForeignKey("cases.id"))
    evidence_id: Mapped[str] = mapped_column(ForeignKey("evidence.id"))
    text: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(60))  # alleged / disputed / court_established / researcher_claim
    case = relationship("Case", back_populates="assertions")
    evidence = relationship("Evidence")

class CourtJudgment(Base):
    __tablename__ = "court_judgments"
    id: Mapped[str] = mapped_column(String(80), primary_key=True)
    case_id: Mapped[str] = mapped_column(ForeignKey("cases.id"))
    court: Mapped[str] = mapped_column(String(300))
    decision_date: Mapped[str | None] = mapped_column(String(30), nullable=True)
    disposition: Mapped[str] = mapped_column(Text)
    appeal_status: Mapped[str] = mapped_column(String(100), default="unknown")
    source_evidence_id: Mapped[str] = mapped_column(ForeignKey("evidence.id"))

class Assessment(Base):
    __tablename__ = "assessments"
    id: Mapped[str] = mapped_column(String(80), primary_key=True)
    case_id: Mapped[str] = mapped_column(ForeignKey("cases.id"))
    model_version: Mapped[str] = mapped_column(String(120))
    status: Mapped[str] = mapped_column(String(80), default="HUMAN_REVIEW_REQUIRED")
    report: Mapped[dict] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

class HumanReview(Base):
    __tablename__ = "human_reviews"
    id: Mapped[str] = mapped_column(String(80), primary_key=True)
    case_id: Mapped[str] = mapped_column(ForeignKey("cases.id"))
    assessment_id: Mapped[str | None] = mapped_column(ForeignKey("assessments.id"), nullable=True)
    reviewer: Mapped[str] = mapped_column(String(160))
    opinion: Mapped[str] = mapped_column(String(80))
    rationale: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

class ModelVersion(Base):
    __tablename__ = "model_versions"
    id: Mapped[str] = mapped_column(String(120), primary_key=True)
    definition: Mapped[dict] = mapped_column(JSON)
    validation_status: Mapped[str] = mapped_column(String(80), default="experimental")

class AuditEvent(Base):
    __tablename__ = "audit_events"
    id: Mapped[str] = mapped_column(String(80), primary_key=True)
    case_id: Mapped[str | None] = mapped_column(String(80), nullable=True)
    action: Mapped[str] = mapped_column(String(100))
    payload: Mapped[dict] = mapped_column(JSON)
    at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

class SourceSnapshot(Base):
    __tablename__ = "source_snapshots"
    id: Mapped[str] = mapped_column(String(80), primary_key=True)
    case_id: Mapped[str] = mapped_column(ForeignKey("cases.id"))
    metadata_record: Mapped[dict] = mapped_column(JSON)
    pages: Mapped[list] = mapped_column(JSON)
