import type { Issue } from "../types";

interface IssueListProps {
  issues: Issue[];
  selectedId: string | null;
  onSelect: (id: string) => void;
  onDelete: (id: string) => void;
}

export default function IssueList({
  issues,
  selectedId,
  onSelect,
  onDelete,
}: IssueListProps) {
  if (issues.length === 0) {
    return <p>No issues yet.</p>;
  }

  return (
    <ul>
      {issues.map((issue) => (
        <li key={issue.id} className={issue.id === selectedId ? "selected" : undefined}>
          <div>
            <strong>{issue.title}</strong>
            <div className="meta">
              {issue.status} / {issue.priority}
            </div>
          </div>
          <div className="actions">
            <button type="button" onClick={() => onSelect(issue.id)}>
              Edit
            </button>
            <button type="button" onClick={() => onDelete(issue.id)}>
              Delete
            </button>
          </div>
        </li>
      ))}
    </ul>
  );
}
