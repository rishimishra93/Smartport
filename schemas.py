from pydantic import BaseModel, Field
from typing import Literal

# 1. Incoming payload schema (What the user sends)
class VehicleDutyRequest(BaseModel):
    # Regex for standard 17-character VIN (ISO 3779 standard, excluding I, O, Q)
    vin:str=Field(
        ...,
        pattern=r"[A-HJ-NPR-Z0-9]{17}$",
        description="Standerd 17 character Vehical Indentification number"
    ) 
    cif_value_inr:float=Field(
        ...,
        gt=0,
        description="cost,insaurance and fridget value in INR (must be positive)"
    )
    engine_cc:int=Field(
        ...,
        gt=0,
        description="Engine displacement in cubic centimeters"
    )
    fule_type:Literal["petrol","diesel","electric"]=Field(
        ...,
        description="Fuel type should be petrol,diesel,electric"
    )

    # 2. Outgoing response schema (What FastAPI guarantees to return)
class VehicleDutyResponse(BaseModel):
    vin:str
    cif_value:float
    duty_rate_percent: float
    basic_customs_duty: float
    social_welfare_surcharge: float
    total_duty_payable: float
    final_landed_cost: float
    is_luxury_bracket: bool