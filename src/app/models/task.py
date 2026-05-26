import sqlalchemy as sa
import sqlalchemy.orm as so
from enum import Enum
from typing import Optional
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy import Enum as SqlEnum
from datetime import datetime, timezone
from ..core.db import Base


class TaskStatus(Enum):
    ACTIVE = "active"
    COMPLETED = "completed"
    ARCHIVED = "archived"

class PriorityLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Task(Base):
    __tablename__ = "tasks"

    id: so.Mapped[uuid.UUID] = so.mapped_column(
        UUID(as_uuid=True), 
        primary_key=True, 
        default=uuid.uuid4
    )
    title: so.Mapped[str] = so.mapped_column(sa.String(256), index=True)
    description: so.Mapped[Optional[str]] = so.mapped_column(sa.String(512), nullable=True)
    project_id: so.Mapped[uuid.UUID] = so.mapped_column( UUID(as_uuid=True), sa.ForeignKey("projects.id"),index=True )
    assignee_id: so.Mapped[uuid.UUID] = so.mapped_column( UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=True,index=True )
    status: so.Mapped[TaskStatus] = so.mapped_column(SqlEnum(TaskStatus), default=TaskStatus.ACTIVE,index=True)
    priority: so.Mapped[PriorityLevel] = so.mapped_column(SqlEnum(PriorityLevel), default=PriorityLevel.MEDIUM,index=True)
    due_date: so.Mapped[Optional[datetime]] = so.mapped_column(sa.DateTime(timezone=True), nullable=True, index=True)
    created_at: so.Mapped[datetime] = so.mapped_column(
        sa.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True
    )

    project: so.Mapped["Project"] = so.relationship("Project", back_populates="tasks") # type: ignore
    assignee: so.Mapped[Optional["User"]] = so.relationship("User", back_populates="assigned_tasks") # type: ignore
