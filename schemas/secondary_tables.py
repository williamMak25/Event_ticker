from sqlalchemy.dialects.postgresql import UUID
from extensions import db

user_events = db.Table(
    'user_events',
    db.Column('user_id',UUID(as_uuid=True), db.ForeignKey('users.id'), primary_key=True),
    db.Column('event_id',UUID(as_uuid=True), db.ForeignKey('events.id'), primary_key=True)
)