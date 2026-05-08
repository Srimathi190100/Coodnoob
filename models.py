from typing import Dict, List, Optional
from pydantic import BaseModel, Field

class Booking(BaseModel):
    """Base model for all travel bookings."""
    name: str
    price: Optional[str] = None
    status: str = "CONFIRMED"

class Profile(BaseModel):
    """User profile data model."""
    name: str = "Nomad User"
    user_id: str = "user_99"

class NomadState(BaseModel):
    """Represents the current real-time state of the nomad."""
    budget_remaining_pct: int = Field(default=85, ge=0, le=100)
    aqi: int = Field(default=45, ge=0)
    rain: bool = False
    high_workload: bool = False
    emergency: bool = False

class TravelPlan(BaseModel):
    """Comprehensive travel plan containing bookings and state."""
    profile: Profile
    bookings: Dict[str, List[Booking]]
    state: NomadState
