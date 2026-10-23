from sqlmodel import SQLModel,create_engine,Session,select
from models import InspectionLab

DB_FILE="smartport.db"
sqlite_url=f"sqlite:///{DB_FILE}"

# check_same_thread: False allows FastAPI background threads to access SQLite
engine=create_engine(sqlite_url,connect_args={"check_same_thread": False})

def create_db_and_tables():
    """Initializes tables and seeds baseline records if table is empty."""
    SQLModel.metadata.create_all(engine)
    seed_initial_data()


def seed_initial_data():
    with Session(engine) as session:
        statement = select(InspectionLab)
        existing = session.exec(statement).first()

        if not existing:
            sample_labs = [
                InspectionLab(
                    lab_name="ARAI Pune Central Testing Laboratory",
                    state="Maharashtra",
                    city="Pune",
                    supports_elec=True,
                    intrenal_remarks="Confidential: Primary central testing agency"
                ),
                InspectionLab(
                    lab_name="ICAT Manesar Automotive Testing Centre",
                    state="Haryana",
                    city="Manesar",
                    supports_elec=True,
                    intrenal_remarks="Confidential: Regular capacity constraints on Mondays"
                ),
                InspectionLab(
                    lab_name="GARC Chennai Testing Facility",
                    state="Tamil Nadu",
                    city="Chennai",
                    supports_elec=False,
                    intrenal_remarks="Confidential: EV certification line under audit"
                ),
                InspectionLab(
                    lab_name="VRDE Ahmednagar Vehicle Research Station",
                    state="Maharashtra",
                    city="Ahmednagar",
                    supports_elec=False,
                    intrenal_remarks="Confidential: Defense/Heavy commercial preference"
                ),
                InspectionLab(
                    lab_name="CIRT Pune Inspection Station",
                    state="Maharashtra",
                    city="Pune",
                    supports_elec=True,
                    intrenal_remarks="Confidential: Certified for retrofitted components"
                ),
            ]
            session.add_all(sample_labs)
            session.commit()


def get_session():
    """Yields a database session per HTTP request and guarantees clean closure."""
    with Session(engine) as session:
        yield session 
