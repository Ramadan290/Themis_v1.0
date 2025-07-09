from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.Payroll_Models.benefits_model import Benefit
from app.models.Payroll_Models.benefit_catalog_model import BenefitCatalog
from app.models.User_Models.user_model import User
from app.schemas.Payroll_Schemas.benefits_schema import BenefitCreate
from app.models.Payroll_Models.payroll_fixed_model import PayrollFixed
from decimal import Decimal


def assign_benefit_to_user(benefit: BenefitCreate, db: Session):
    # Get catalog entry
    catalog = db.query(BenefitCatalog).filter(BenefitCatalog.id == benefit.benefit_catalog_id).first()
    if not catalog:
        raise HTTPException(status_code=404, detail="Benefit catalog entry not found")

    # Set amount: user input or catalog default
    benefit_amount = benefit.amount if benefit.amount is not None else catalog.default_amount

    existing = db.query(Benefit).filter(
    Benefit.user_id == benefit.user_id,
    Benefit.benefit_catalog_id == benefit.benefit_catalog_id
    ).first()

    if existing:
        raise HTTPException(status_code=409, detail="Benefit already assigned.")

    # Create benefit record
    new_benefit = Benefit(
        user_id=benefit.user_id,
        benefit_catalog_id=benefit.benefit_catalog_id,
        amount=benefit_amount
    )
    db.add(new_benefit)
    db.commit()
    db.refresh(new_benefit)

    # 🧮 Recalculate total payroll
    payroll = db.query(PayrollFixed).filter(PayrollFixed.user_id == benefit.user_id).first()
    if payroll:
        all_benefits = db.query(Benefit).filter(Benefit.user_id == benefit.user_id).all()
        total_benefits = sum(b.amount for b in all_benefits)
        payroll.total = payroll.base_salary + Decimal(str(total_benefits))
        db.commit()

    return new_benefit


def get_user_benefits(user_id: int, db: Session):
    benefits = db.query(Benefit).filter(Benefit.user_id == user_id).all()
    return benefits


def add_default_benefits(user_id: int, db: Session):
    default_catalogs = db.query(BenefitCatalog).limit(3).all()  # or use filter if you want specific names

    for catalog in default_catalogs:
        benefit = Benefit(
            user_id=user_id,
            benefit_catalog_id=catalog.id,
            amount=catalog.default_amount
        )
        db.add(benefit)

    db.commit()
