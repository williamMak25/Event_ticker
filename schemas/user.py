from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from extensions import db
from schemas.secondary_tables import user_events


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(UUID(as_uuid=True), primary_key=True,default=uuid.uuid4)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(50),nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    password = db.Column(db.String(), nullable=False)

    events = db.relationship('Event',secondary=user_events, back_populates='users', lazy=True)   
    tickets = db.relationship(
        "Ticket",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="select"
    )
    def __repr__(self):
        return f"<User {self.email}>"
    
    def to_dict(self):
        return {
            "id": str(self.id),
            "name": self.name,
            "email": self.email,
            "created_at": self.created_at.isoformat()
        }
    