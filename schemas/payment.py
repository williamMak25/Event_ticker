from extensions import db
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid
class Wallet(db.Model):
    __tablename__ = "wallets"

    id = db.Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
    user_id = db.Column(UUID(as_uuid=True),db.ForeignKey('users.id'),nullable=False)
    balance = db.Column(db.Float,nullable=False,default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.now)

    transtions = db.relationship('Transtions',back_populates='wallets',lazy='select', cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Wallets {self.id}>"
    
    def to_dict(self):
        return{
            "id": str(self.id),
            "user_id": str(self.user_id),
            "balance": float(self.balance),
            "transtions": [transtion.to_dict() for transtion in self.transtions],
            "created_at": self.created_at.isoformat(),
        }
    
class Transtions(db.Model):
    __tablename__ = "transtions"

    id = db.Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
    wallet_id = db.Column(UUID(as_uuid=True),db.ForeignKey('wallets.id'),nullable=False)

    amount = db.Column(db.Float,nullable=False)
    type = db.Column(db.String(50),nullable=False)  # 'credit' or 'debit'
    created_at = db.Column(db.DateTime, default=datetime.now)

    wallets = db.relationship('Wallet',back_populates='transtions',lazy='select')

    def __repr__(self):
        return f"<Transtions {self.id}>"
    
    def to_dict(self):
        return{
            "id": str(self.id),
            "wallet_id": str(self.wallet_id),
            "amount": float(self.amount),
            "type": str(self.type),
            "created_at": self.created_at.isoformat(),
        }