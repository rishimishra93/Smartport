from fastapi import FastAPI
from schemas  import VehicleDutyRequest, VehicleDutyResponse
from tools import Calculate_Vehical_duty

from sqlmodel import Session,select


app=FastAPI(
    title="SmartPort API",
    description="Automated Vehicle Import Duty & Clearance Assistant",
    version="1.0.0"
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
    calculate=Calculate_Vehical_duty(
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


