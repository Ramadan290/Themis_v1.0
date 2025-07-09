from pydantic import BaseModel
from typing import Optional

class BenefitCatalogBase(BaseModel):
    name: str
    description: Optional[str] = None
    default_amount: Optional[float] = 0

class BenefitCatalogCreate(BenefitCatalogBase):
    pass

class BenefitCatalogRead(BenefitCatalogBase):
    id: int

    class Config:
        from_attributes = True
