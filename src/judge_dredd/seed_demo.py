from .db import init_db, SessionLocal
from .models import Case, Subject, Evidence, Assertion, Charge

def main():
    init_db()
    with SessionLocal() as db:
        if db.get(Case, "demo-001"):
            print("demo-001 already seeded")
            return
        db.add(Subject(id="demo-subject", display_name="Fictional Person", is_synthetic=True))
        db.add(Case(id="demo-001", title="Synthetic educational case (NOT REAL)",
                    procedural_status="fictional", subject_id="demo-subject", is_synthetic=True))
        db.add(Evidence(id="demo-evidence-1", case_id="demo-001", kind="fictional_document",
                        description="Illustrative narrative produced for tests; not evidence of any real event",
                        source_document_id="SYNTHETIC-FIXTURE", pinpoint="paragraph 1",
                        source_status="synthetic"))
        db.add(Assertion(id="demo-assertion-1", case_id="demo-001", evidence_id="demo-evidence-1",
                         text="A fictional subject was alleged to have damaged property.", status="alleged"))
        db.add(Charge(id="demo-charge-1", case_id="demo-001", law_reference="FICTIONAL LAW",
                      allegation="Alleged property damage (synthetic fixture)",
                      legal_elements=["act", "intent", "harm"], status="alleged"))
        db.commit()
        print("Seeded demo-001 (synthetic)")

if __name__ == "__main__":
    main()
