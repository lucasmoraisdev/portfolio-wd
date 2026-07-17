from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.modules.toys.models import Toys
from app.modules.events.models import Events
from app.modules.testimonials.models import Testimonials
from app.modules.faq.models import FAQ
from app.modules.contacts.models import ContactMessage
from app.modules.dashboard.schemas import DashboardStatsResponse

class DashboardService:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_stats(self) -> DashboardStatsResponse:
        # Count Toys
        total_toys = self.db.execute(select(func.count(Toys.id))).scalar() or 0
        active_toys = self.db.execute(select(func.count(Toys.id)).where(Toys.is_active)).scalar() or 0

        # Count Events
        total_events = self.db.execute(select(func.count(Events.id))).scalar() or 0
        active_events = self.db.execute(select(func.count(Events.id)).where(Events.is_active)).scalar() or 0

        # Count Testimonials
        total_testimonials = self.db.execute(select(func.count(Testimonials.id))).scalar() or 0
        active_testimonials = self.db.execute(select(func.count(Testimonials.id)).where(Testimonials.is_active)).scalar() or 0

        # Count FAQ
        total_faqs = self.db.execute(select(func.count(FAQ.id))).scalar() or 0
        active_faqs = self.db.execute(select(func.count(FAQ.id)).where(FAQ.is_active)).scalar() or 0

        # Count Contacts
        total_contacts = self.db.execute(select(func.count(ContactMessage.id))).scalar() or 0
        unread_contacts = self.db.execute(select(func.count(ContactMessage.id)).where(ContactMessage.is_read == False)).scalar() or 0

        return DashboardStatsResponse(
            total_toys=total_toys,
            active_toys=active_toys,
            total_events=total_events,
            active_events=active_events,
            total_testimonials=total_testimonials,
            active_testimonials=active_testimonials,
            total_faqs=total_faqs,
            active_faqs=active_faqs,
            total_contacts=total_contacts,
            unread_contacts=unread_contacts,
        )
