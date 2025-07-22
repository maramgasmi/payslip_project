from  sqlalchemy  import Column, Integer, String, Float , Date
from database import Base 


class Payslip(Base):
    __tablename__="payslips"
    id= Column(Integer, primary_key=True, index=True)
    employee_id= Column(String, index=True)
    employee_name=Column(String,nullable=False)
    position=Column(String)
    base_salary=Column(Float)
    bonus=Column(Float)
    deductions= Column(Float)
    net_salary= Column(Float)
    gross_salary = Column(Float)
    period_start= Column(Date)
    period_end= Column(Date)
    company_name= Column(String)
    company_address=Column(String)
    date_issued= Column(Date)
    status = Column(String)