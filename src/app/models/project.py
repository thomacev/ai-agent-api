import sqlalchemy as sa
import sqlalchemy.orm as so
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime, timezone
from ..core.db import Base


class Project(Base):
    __tablename__ = "projects"

    id: so.Mapped[uuid.UUID] = so.mapped_column(
        UUID(as_uuid=True), 
        primary_key=True, 
        default=uuid.uuid4
    )
    name: so.Mapped[str] = so.mapped_column(sa.String(128), index=True)
    description: so.Mapped[str] = so.mapped_column(sa.String(512), index=True)
    owner_id: so.Mapped[uuid.UUID] = so.mapped_column( UUID(as_uuid=True), sa.ForeignKey("users.id"), index=True )
    created_at: so.Mapped[datetime] = so.mapped_column(
        sa.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True
    )

    owner: so.Mapped["User"] = so.relationship("User", back_populates="projects") # type: ignore
    tasks: so.Mapped[list["Task"]] = so.relationship("Task", back_populates="project", cascade="all, delete-orphan")# type: ignore
