from typing import Optional
from sqlmodel import SQLModel,Field

# 1. BASE SCHEMA: Shared domain attributes across intake & persistence
class InspectionLabBase(SQLModel):
    lab_name:str=Field(
        min_length=3,
        max_length=150,
        description="Official registered name of the testing lab"
    )
    state:str=Field(
        min_length=3,
        max_length=50,
        description="Name of the state"
    )
    city:str=Field(
        min_length=3,
        max_length=50,
        description="Name of the city"
    )
    supports_elec:bool=Field(
        default=True,
        description="Whether the facility has EV battery & dyno testing equipment"
    )

# 2. INTAKE SCHEMAS (Client -> API)
class InspectionLabcreate(InspectionLabBase):
    """
    Intake schema for POST /api/labs.
    Inherits validation from Base. Excludes internal audit fields.
    """
    pass
class InspectionLabupdate(SQLModel):
    """
    Intake schema for PATCH /api/labs/{id}.
    All fields are Optional so clients only send the attributes they want to modify.
    """
    lab_name: Optional[str] = Field(default=None, min_length=3, max_length=150)
    state: Optional[str] = Field(default=None, min_length=2, max_length=50)
    city: Optional[str] = Field(default=None, min_length=2, max_length=50)
    supports_electric: Optional[bool] = None

# 3. DATABASE TABLE (ORM / Disk Layer)
class InspectionLab(InspectionLabBase,table=True):
    """
    Actual SQL table on disk.
    table=True tells SQLModel/SQLAlchemy to register it in metadata.
    """
    __tablename__="INSPECTION_LABS"
    id:Optional[int]=Field(default=None,primary_key=True)
    # Internal fields: stored in SQL, never accepted directly from client payload
    is_active:bool=Field(default=True,)
    intrenal_remarks:Optional[str]=Field(
        default=None,
        description="Confidential inspector remarks that stays within the API"
    )

# 4. OUTPUT SCHEMA (API -> Client)
class Inspeactionlabread(InspectionLabBase):
    """
    Outgoing response contract.
    Exposes the system ID and operational status, but omits internal_remarks.
    """
    id:int
    is_active:bool

