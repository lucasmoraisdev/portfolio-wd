from pydantic import BaseModel

class DashboardStatsResponse(BaseModel):
    total_toys: int
    active_toys: int
    total_events: int
    active_events: int
    total_testimonials: int
    active_testimonials: int
    total_faqs: int
    active_faqs: int
    total_contacts: int
    unread_contacts: int
