from extensions import db
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
from schemas.secondary_tables import user_events
import uuid
class Event(db.Model):
    __tablename__ = 'events'

    id = db.Column(UUID(as_uuid=True), primary_key=True,default=uuid.uuid4)
    name = db.Column(db.String(200), nullable=False)
    date_time = db.Column(db.DateTime,nullable=False,)
    location = db.Column(db.String(400), nullable=False)
    avaiable_tickets = db.Column(db.Integer, nullable=False)
    ticket_price = db.Column(db.Float , nullable=False ,default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.now)

    users = db.relationship('User',secondary=user_events, back_populates='events', lazy=True)
    tickets = db.relationship('Ticket',back_populates='event',lazy="select", cascade="all, delete-orphan")
    def __repr__(self):
        return f"<Event {self.name}>"
    
    def to_dict(self):
        return {
            "id": str(self.id),
            "name": self.name,
            "location": self.location,
            "created_at": self.created_at.isoformat(),
            "date_time": self.date_time.isoformat(),
            "avaiable_tickets": self.avaiable_tickets,
            "ticket_price":float(self.ticket_price)
        }
