import sqlalchemy as sa
import sqlalchemy.orm as so
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime, timezone
from ..core.db import Base

class User(Base):
    __tablename__ = "users"

    id: so.Mapped[uuid.UUID] = so.mapped_column(
        UUID(as_uuid=True), 
        primary_key=True, 
        default=uuid.uuid4
    )
    email: so.Mapped[str] = so.mapped_column(sa.String(128), unique=True, index=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(64))
    created_at: so.Mapped[datetime] = so.mapped_column(
        sa.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True
    )

    projects: so.Mapped[list["Project"]] = so.relationship("Project", back_populates="owner", cascade="all, delete-orphan") # type: ignore
    
    assigned_tasks: so.Mapped[list["Task"]] = so.relationship("Task", back_populates="assignee")# type: ignore