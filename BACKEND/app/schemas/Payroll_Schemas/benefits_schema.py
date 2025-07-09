""""

This schemas are responsible for how data is sent to the API and received from it.
It also verifies input and output , more of validation

orm_mode = true , allows pydantic schemes to access fields via attributes instead of dict keys which would be a hassle 

This file is responsible for the Benefits including :

 1 -  The base benefits will output all benefits info  

 2 -  Creating a new beenfit will jsut inherit everything
        
 3 -  Reading Benefits , only the id is enough as i said before we dont want a lot of api communication for performance

"""

# schemas/benefit.py

from pydantic import BaseModel
from typing import Optional

class BenefitBase(BaseModel):
    user_id: int
    benefit_catalog_id: int

class BenefitCreate(BaseModel):
    user_id: int
    benefit_catalog_id: int
    amount: Optional[float] = None  # <-- not required

class BenefitRead(BenefitBase):
    id: int

    class Config:
        from_attributes = True
