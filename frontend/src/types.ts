// Mirror of app/schemas.py — keep these in sync with the backend enums/models.

export type IssueStatus = "open" | "in_progress" | "closed";
export type IssuePriority = "low" | "medium" | "high";

export interface Issue {
  id: string;
  title: string;
  description: string;
  priority: IssuePriority;
  status: IssueStatus;
}

export interface IssueCreate {
  title: string;
  description: string;
  priority: IssuePriority;
}

export interface IssueUpdate {
  title?: string;
  description?: string;
  priority?: IssuePriority;
  status?: IssueStatus;
}
