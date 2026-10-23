from fastapi import FastAPI,HTTPException,status,Depends
from schemas  import VehicleDutyRequest, VehicleDutyResponse
from tools import Calculate_Vehicle_duty
from contextlib import asynccontextmanager

from sqlmodel import Session,select

from models import (
    InspectionLab,
    InspectionLabcreate,
    Inspeactionlabread,
    InspectionLabupdate,
)
from database import create_db_and_tables, get_session

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app=FastAPI(
    title="SmartPort API",
    description="Automated Vehicle Import Duty & Clearance Assistant",
    version="1.0.0",
    lifespan=lifespan
)

@app.get("/")
def read_root():
    return{
        "status":"Healthy",
        "service":"Smartport Backend",
        "version":"1.0.0"
    }

@app.get("/api/ports/{port_code}")
def get_port_code(port_code:str):
    return{
        "Port code":port_code.upper(),
        "status":"Operational",
        "icegate connected":True
    }

# New POST endpoint linking Schemas and Tools
@app.post("/api/calculate-duty",response_model=VehicleDutyResponse)
def compute_duty_endpoint(payload:VehicleDutyRequest):
    # 1. Delegate calculation to tools.py using validated fields
    calculate=Calculate_Vehicle_duty(
        cif_value=payload.cif_value_inr,
        engine_cc=payload.engine_cc,
        fule=payload.fule_type
    )
    # 2. Return structured data matching VehicleDutyResponse
    return VehicleDutyResponse(
        vin=payload.vin,
        cif_value=payload.cif_value_inr,
        **calculate
    )

# 1. READ (Filter by State) -> Returns list[InspectionLabRead]
@app.get("/api/labs/{state}", response_model=list[Inspeactionlabread])
def get_labs_by_state(state: str, session: Session = Depends(get_session)):
    statement = select(InspectionLab).where(
        InspectionLab.state.ilike(state),
        InspectionLab.is_active == True
    )
    labs = session.exec(statement).all()

    if not labs:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No approved inspection facilities registered in state: '{state}'"
        )
    return labs


# 2. CREATE -> Takes InspectionLabCreate, returns InspectionLabRead
@app.post(
    "/api/labs", 
    response_model=Inspeactionlabread, 
    status_code=status.HTTP_201_CREATED
)
def create_lab(lab_in: InspectionLabcreate, session: Session = Depends(get_session)):
    # Safely transform validated input schema into table instance
    db_lab = InspectionLab.model_validate(lab_in)
    
    session.add(db_lab)
    session.commit()
    session.refresh(db_lab)
    
    # Serialized back to client via InspectionLabRead (internal_remarks excluded)
    return db_lab


# 3. UPDATE (Partial) -> Takes InspectionLabUpdate, returns InspectionLabRead
@app.patch("/api/labs/{lab_id}", response_model=Inspeactionlabread)
def update_lab(
    lab_id: int, 
    patch_data: InspectionLabupdate, 
    session: Session = Depends(get_session)
):
    db_lab = session.get(InspectionLab, lab_id)
    if not db_lab:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Lab facility with ID {lab_id} not found"
        )

    # exclude_unset=True ignores fields the client didn't supply in the payload
    update_data = patch_data.model_dump(exclude_unset=True)
    db_lab.sqlmodel_update(update_data)

    session.add(db_lab)
    session.commit()
    session.refresh(db_lab)
    return db_lab
