from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime

from database import Base

class Advertisement(Base):
**tablename** = "advertisements"

id = Column(Integer, primary_key=True)
title = Column(String, nullable=False)
description = Column(String, nullable=False)
price = Column(Integer, nullable=False)
author = Column(String, nullable=False)
created_at = Column(DateTime, default=datetime.utcnow)