from typing import List
from pydantic import BaseModel

from src.core.helpers.options.add_purchase_options import AddPurchaseOptions


class AddPurchaseSchema(BaseModel):
    purchase_id: int
    products: List[AddPurchaseOptions]
