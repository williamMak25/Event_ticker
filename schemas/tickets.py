from extensions import db
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
class Ticket(db.Model):
    __tablename__ = 'tickets'

    id  = db.Column(UUID(as_uuid=True), primary_key=True,default=uuid.uuid4)

    user_id =db.Column(UUID(as_uuid=True),db.ForeignKey('users.id'),nullable=False)
    event_id = db.Column(UUID(as_uuid=True),db.ForeignKey('events.id'),nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    total_token = db.Column(db.Integer,nullable=False)

    user = db.relationship('User',back_populates='tickets',lazy="select")
    event = db.relationship('Event',back_populates='tickets',lazy="select")

    def __repr__(self):
        return f"<Ticket {self.id}>"
    def to_dict(self):
        return {
            "id": str(self.id),
            "user_id": str(self.user_id),
            "user": self.user.to_dict(),
            "event": self.event.to_dict(),
            "event_id": str(self.event_id),
            "created_at": self.created_at.isoformat(),
            "total_token": self.total_token
        }