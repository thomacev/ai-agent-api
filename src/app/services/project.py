"""
GET /projects
GET /projects/{id}/tasks
POST /projects/{id}/tasks
"""
#Solo endpoints basicos para testing
#NO hay login ni nada por ahora, solo hay que testear que la IA puede crear proyectos y tareas, y listarlos.
#Luego se pueden agregar endpoints mas complejos como asignar tareas a usuarios, etc.

from uuid import UUID
from fastapi import APIRouter, Depends, status, Body
from sqlalchemy.orm import Session
from app.models.project import Project
from app.models.task import Task

router = APIRouter(tags=["projects"])

router.post("/projects", status_code=status.HTTP_201_CREATED)
async def create_project(
    project_data: dict = Body(...),
    db: Session = Depends(...)
):
    new_project = Project(**project_data)
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    return new_project

router.get("/projects", status_code=status.HTTP_200_OK)
async def list_projects(db: Session = Depends(...)):
    query = db.query(Project).all()
    return query

router.post("/projects/{project_id}/tasks", status_code=status.HTTP_201_CREATED)
async def create_project_task(
    project_id: UUID,
    task_data: dict = Body(...),
    db: Session = Depends(...)
):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        return {"error": "Project not found"}
    new_task = Task(**task_data, project_id=project_id)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

router.get("/projects/{project_id}/tasks", status_code=status.HTTP_200_OK)
async def list_project_tasks(   
    project_id: UUID,
    db: Session = Depends(...)
):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        return {"error": "Project not found"}
    return project.tasks