from pydantic import BaseModel, Field
from datetime import datetime
from typing import Dict, Any, Optional

class ProjectBase(BaseModel):
    brief: str = Field(..., description="Proje açıklaması")
    status: Optional[str] = Field("active", description="Proje durumu")
    phase: Optional[str] = Field("planning", description="Proje aşaması")

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(BaseModel):
    brief: Optional[str] = None
    code: Optional[str] = None
    status: Optional[str] = None
    phase: Optional[str] = None
    agent_outputs: Optional[Dict[str, Any]] = None
    quality_score: Optional[float] = Field(None, ge=0, le=100)
    cost: Optional[float] = Field(None, ge=0)

class ProjectResponse(ProjectBase):
    id: int
    code: str
    created_at: datetime
    updated_at: datetime
    agent_outputs: Dict[str, Any]
    quality_score: float
    cost: float
    
    class Config:
        from_attributes = True