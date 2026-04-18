from sqlalchemy.orm import Mapped,mapped_column,relationship
from sqlalchemy import String,Boolean,DateTime,ForeignKey,Integer
from datetime import datetime,timezone
from app.db.config import Base
class UserCredit(Base):
    __tablename__="user_ credit"
    id:Mapped[int]=mapped_column(primary_key=True)
    user_id:Mapped[int]=mapped_column(ForeignKey("user.id",ondelete="CASCADE"),unique=True)
    credits:Mapped[int]=mapped_column(Integer,default=10)
class APIKey(Base):
    __tablename__="key"
    id:Mapped[int]=mapped_column(primary_key=True)
    key:Mapped[str]=mapped_column(String(255),unique=True,nullable=True,index=True)
    user_id:Mapped[int]=mapped_column(ForeignKey("user.id",ondelete="CASCADE"),unique=True)
class CreditRequest(Base):
    __tablename__="credit_user"
    id:Mapped[int]=mapped_column(primary_key=True)
    user_id:Mapped[int]=mapped_column(ForeignKey("user.id",ondelete="CASCADE"),nullable=False)
    credit_request:Mapped[int]=mapped_column(Integer,nullable=False)
    status:Mapped[int]=mapped_column(String(50),default="pending")
    created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=lambda:datetime.now(timezone.utc))