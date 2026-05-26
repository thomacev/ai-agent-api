import sys
import os
#primero tiene que estar esta linea y despues buscar el src
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime, timezone, timedelta
from src.app.core.db import SessionLocal, engine, Base 
from src.app.models.project import Project
from src.app.models.task import Task, TaskStatus, PriorityLevel
from src.app.models.user import User
import asyncio



async def seed_database():
    print("Starting database seeding process...")
    
    print("Checking and creating tables if they don't exist...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with SessionLocal() as session:
        try:
            print("Cleaning previous tables...")
            import sqlalchemy as sa
            await session.execute(sa.delete(Task))
            await session.execute(sa.delete(Project))
            await session.execute(sa.delete(User))
            await session.commit()

            print("Creating user...")
            user = User(
                name="Alex Ortega",
                email="alex.ortega@techcorp.com"
            )
            session.add(user)
            await session.flush() 

            print("Creating project...")
            project = Project(
                name="E-commerce Platform Development",
                description="Development of the checkout module and payment gateway.",
                owner_id=user.id
            )
            session.add(project)
            await session.flush()

            # 4. Crear 5 Tareas
            print("Creating 5 tasks...")
            ahora = datetime.now(timezone.utc)
            
            tareas = [
                Task(
                    title="Design Database Architecture",
                    description="Create the ER diagram and the initial migration scripts.",
                    project_id=project.id,
                    assignee_id=user.id,
                    status=TaskStatus.COMPLETED,
                    priority=PriorityLevel.HIGH,
                    due_date=ahora - timedelta(days=2)
                ),
                Task(
                    title="Integrate Stripe SDK",
                    description="Implement the webhook endpoints.",
                    project_id=project.id,
                    assignee_id=user.id,
                    status=TaskStatus.ACTIVE,
                    priority=PriorityLevel.HIGH,
                    due_date=ahora + timedelta(days=4)
                ),
                Task(
                    title="Set Up AWS Staging Test Server",
                    description="Launch the EC2 instance and configure the proxy.",
                    project_id=project.id,
                    assignee_id=user.id,
                    status=TaskStatus.ACTIVE,
                    priority=PriorityLevel.MEDIUM,
                    due_date=ahora + timedelta(days=7)
                ),
                Task(
                    title="Write Unit Tests for Checkout",
                    description="Achieve a minimum coverage of 85%.",
                    project_id=project.id,
                    assignee_id=user.id,
                    status=TaskStatus.ACTIVE,
                    priority=PriorityLevel.MEDIUM,
                    due_date=ahora + timedelta(days=10)
                ),
                Task(
                    title="UI Validation and Client Feedback",
                    description="Pending meeting to present the interactive mockups.",
                    project_id=project.id,
                    assignee_id=None,
                    status=TaskStatus.ACTIVE,
                    priority=PriorityLevel.LOW,
                    due_date=ahora + timedelta(days=15)
                )
            ]
            
            session.add_all(tareas)
            
            await session.commit()
            print("Database seeding completed successfully!")
            
        except Exception as e:
            print(f"An error occurred: {e}")
            await session.rollback()

if __name__ == "__main__":
    asyncio.run(seed_database())