from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.models import Issue
from app.schemas import IssueCreate, IssueOut, IssueStatus, IssueUpdate

router = APIRouter(prefix="/api/v1/issues", tags=["issues"])


@router.get("/", response_model=list[IssueOut])
async def get_issues(db: AsyncSession = Depends(get_db)):
    """Retrieve all issues."""
    result = await db.execute(select(Issue))
    return result.scalars().all()


@router.get("/{issue_id}", response_model=IssueOut)
async def get_issue_by_id(issue_id: str, db: AsyncSession = Depends(get_db)):
    """Retrieve a specific issue by ID."""
    issue = await db.get(Issue, issue_id)
    if not issue:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Issue not found"
        )
    return issue


@router.post("/", response_model=IssueOut, status_code=status.HTTP_201_CREATED)
async def create_issue(payload: IssueCreate, db: AsyncSession = Depends(get_db)):
    """Create a new issue."""
    new_issue = Issue(
        title=payload.title,
        description=payload.description,
        priority=payload.priority.value,
        status=IssueStatus.open.value,
    )
    db.add(new_issue)
    await db.commit()
    await db.refresh(new_issue)
    return new_issue


@router.put("/{issue_id}", response_model=IssueOut)
async def update_issue_by_id(
    issue_id: str, payload: IssueUpdate, db: AsyncSession = Depends(get_db)
):
    """Partially update an issue. Send only the fields you want to change."""
    issue = await db.get(Issue, issue_id)
    if not issue:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Issue not found"
        )
    updates = payload.model_dump(exclude_unset=True, exclude_none=True)
    for field, value in updates.items():
        setattr(issue, field, value.value if hasattr(value, "value") else value)
    await db.commit()
    await db.refresh(issue)
    return issue


@router.delete("/{issue_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_issue_by_id(issue_id: str, db: AsyncSession = Depends(get_db)):
    """Delete a specific issue by ID."""
    issue = await db.get(Issue, issue_id)
    if not issue:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Issue not found"
        )
    await db.delete(issue)
    await db.commit()
