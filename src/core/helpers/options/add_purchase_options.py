from typing import List, Optional
from pydantic import BaseModel


class AddPurchaseOptions(BaseModel):
    product_id: int
    components: Optional[List[int]] = None
