import uuid

from fastapi import APIRouter, HTTPException, status

from app.schemas import IssueCreate, IssueOut, IssueStatus, IssueUpdate
from app.storage import load_data, save_data

router = APIRouter(prefix="/api/v1/issues", tags=["issues"])


@router.get("/", response_model=list[IssueOut])
async def get_issues():
    """Retrieve all issues."""
    issues = load_data()
    return issues


@router.get("/{issue_id}", response_model=IssueOut)
async def get_issue_by_id(issue_id: str):
    """Retrieve a specific issue by ID."""
    issues = load_data()
    issue = next((issue for issue in issues if issue["id"] == issue_id), None)
    if not issue:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Issue not found"
        )
    return issue


@router.post("/", response_model=IssueOut, status_code=status.HTTP_201_CREATED)
async def create_issue(payload: IssueCreate):
    """Create a new issue."""
    issues = load_data()
    new_issue = {
        "id": str(uuid.uuid4()),
        "title": payload.title,
        "description": payload.description,
        "priority": payload.priority,
        "status": IssueStatus.open,
    }
    issues.append(new_issue)
    save_data(issues)
    return new_issue


@router.put("/{issue_id}", response_model=IssueOut)
async def update_issue_by_id(issue_id: str, payload: IssueUpdate):
    """Partially update an issue. Send only the fields you want to change."""
    issues = load_data()
    issue = next((issue for issue in issues if issue["id"] == issue_id), None)
    if not issue:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Issue not found"
        )
    issue.update(payload.model_dump(exclude_unset=True, exclude_none=True))
    save_data(issues)
    return issue


@router.delete("/{issue_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_issue_by_id(issue_id: str):
    """Delete a specific issue by ID."""
    issues = load_data()
    issue = next((issue for issue in issues if issue["id"] == issue_id), None)
    if not issue:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Issue not found"
        )
    issues.remove(issue)
    save_data(issues)

