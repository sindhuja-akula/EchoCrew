from sqlalchemy import Column, Integer, String, Enum as SQLEnum
from sqlalchemy.orm import relationship
from database.models.base import Base, TimestampMixin
from database.models.enums import UserRole

class User(Base, TimestampMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=True)
    role = Column(
        SQLEnum(UserRole, name="user_role", native_enum=True),
        default=UserRole.CITIZEN,
        nullable=False
    )

    reports = relationship("GarbageReport", back_populates="reporter")

    def __repr__(self):
        return f"<User id={self.id} username='{self.username}' role='{self.role}'>"
