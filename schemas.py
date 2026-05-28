from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

class AdvertisementCreate(BaseModel):
title: str
description: str
price: int = Field(gt=0)
author: str

class AdvertisementUpdate(BaseModel):
title: Optional[str] = None
description: Optional[str] = None
price: Optional[int] = Field(default=None, gt=0)
author: Optional[str] = None

class AdvertisementResponse(BaseModel):
id: int
title: str
description: str
price: int
author: str
created_at: datetime

class Config:
    from_attributes = True