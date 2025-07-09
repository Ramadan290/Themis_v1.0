from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.controllers.Payroll_Controllers import benefits_catalog_controller
from app.schemas.Payroll_Schemas.benefit_catalog_schema import BenefitCatalogCreate, BenefitCatalogRead
from app.database.session import get_db
from app.core.dependencies import require_role

router = APIRouter(prefix="/catalog/benefit", tags=["Benefit Catalog"])

# Create new benefit in catalog (restricted to HR/Admin)
@router.post("/add", response_model=BenefitCatalogRead, dependencies=[Depends(require_role(["admin", "hr"]))])
def add_benefit_to_catalog(benefit: BenefitCatalogCreate, db: Session = Depends(get_db)):
    return benefits_catalog_controller.create_catalog_benefit(benefit, db)

# Get all benefits in catalog (restricted to HR/Admin)
@router.get("/list", response_model=List[BenefitCatalogRead], dependencies=[Depends(require_role(["admin", "hr"]))])
def list_all_benefits(db: Session = Depends(get_db)):
    return benefits_catalog_controller.get_all_catalog_benefits(db)

# Delete a catalog benefit (restricted to HR/Admin)
@router.delete("/{benefit_id}", dependencies=[Depends(require_role(["admin", "hr"]))])
def delete_benefit(benefit_id: int, db: Session = Depends(get_db)):
    return benefits_catalog_controller.delete_catalog_benefit(benefit_id, db)

