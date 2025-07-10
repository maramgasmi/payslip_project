from sqlalchemy.orm import Session
import schemas 
import crud 
import models 

def create_payslip (db: Session, payslip: schemas.PayslipCreate):
    payslip_data = payslip.dict()
    payslip_data['net_salary'] = payslip_data['gross_salary'] - payslip_data['deductions']
    db_payslip = models.Payslip(**payslip_data)
    db.add(db_payslip)
    db.commit()
    db.refresh(db_payslip)
    return db_payslip

def get_payslip(db: Session, payslip_id: int ):
    return db.query(models.Payslip).filter(models.Payslip.id == payslip_id).first()

def get_all_payslips(db: Session):
    return db.query(models.Payslip).all()
 

def delete_payslip(db: Session, payslip_id: int):
    db_payslip = db.query(models.Payslip).filter(models.Payslip.id== payslip_id).first()
    if db_payslip:
        db.delete(db_payslip)
        db.commit()
        return True 
    return False

def update_payslip(db: Session, payslip_id: int, updated_data: schemas.PayslipCreate):
    payslip = get_payslip(db, payslip_id)
    if not payslip:
        return None
    for field, value in updated_data.dict().items():
        setattr(payslip, field, value)
    payslip.net_salary = payslip.gross_salary - payslip.deductions  # recalcule
    db.commit()
    db.refresh(payslip)
    return payslip