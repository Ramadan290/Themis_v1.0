from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.Payroll_Models.benefit_catalog_model import BenefitCatalog
from app.schemas.Payroll_Schemas.benefit_catalog_schema import BenefitCatalogCreate

# Create a new catalog entry
def create_catalog_benefit(benefit_data: BenefitCatalogCreate, db: Session):
    existing = db.query(BenefitCatalog).filter(BenefitCatalog.name == benefit_data.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Benefit already exists in catalog")

    benefit = BenefitCatalog(**benefit_data.dict())
    db.add(benefit)
    db.commit()
    db.refresh(benefit)
    return benefit

# Get all catalog benefits
def get_all_catalog_benefits(db: Session):
    return db.query(BenefitCatalog).all()

# (Optional) Delete a benefit from catalog
def delete_catalog_benefit(benefit_id: int, db: Session):
    benefit = db.query(BenefitCatalog).filter(BenefitCatalog.id == benefit_id).first()
    if not benefit:
        raise HTTPException(status_code=404, detail="Benefit not found")
    db.delete(benefit)
    db.commit()
    return {"detail": "Benefit removed from catalog"}
