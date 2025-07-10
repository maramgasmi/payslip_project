from pydantic import BaseModel
from datetime import date

class PayslipBase(BaseModel):

    employee_id: str 
    employee_name: str 
    position: str
    base_salary: float
    bonus:float
    deductions:float
    net_salary: float
    gross_salary: float 
    period_start: date
    period_end: date
    company_name: str
    company_adress:str
    date_isuued:date
    status : str

class PayslipCreate(PayslipBase):
    pass 

class PayslipResponse(PayslipBase):
    id: int

    model_config = {"from_attributes": True}