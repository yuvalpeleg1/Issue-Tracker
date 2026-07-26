import { useCallback, useEffect, useState } from "react";
import { createIssue, deleteIssue, listIssues, updateIssue } from "./api";
import IssueEditor from "./components/IssueEditor";
import IssueList from "./components/IssueList";
import type { Issue, IssueCreate, IssueUpdate } from "./types";

export default function App() {
  const [issues, setIssues] = useState<Issue[]>([]);
  const [selectedId, setSelectedId] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  const selected = issues.find((issue) => issue.id === selectedId) ?? null;

  const load = useCallback(async () => {
    setError(null);
    try {
      const data = await listIssues();
      setIssues(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load issues");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    void load();
  }, [load]);

  async function handleCreate(payload: IssueCreate) {
    setError(null);
    try {
      const created = await createIssue(payload);
      setIssues((prev) => [...prev, created]);
      setSelectedId(created.id);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to create issue");
    }
  }

  async function handleUpdate(id: string, payload: IssueUpdate) {
    setError(null);
    try {
      const updated = await updateIssue(id, payload);
      setIssues((prev) => prev.map((issue) => (issue.id === id ? updated : issue)));
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to update issue");
    }
  }

  async function handleDelete(id: string) {
    setError(null);
    try {
      await deleteIssue(id);
      setIssues((prev) => prev.filter((issue) => issue.id !== id));
      if (selectedId === id) {
        setSelectedId(null);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to delete issue");
    }
  }

  return (
    <main>
      <h1>Issue Tracker</h1>
      {error && <p className="error">{error}</p>}
      {loading ? (
        <p>Loading…</p>
      ) : (
        <div className="layout">
          <section>
            <h2>Create</h2>
            <IssueEditor mode="create" onSubmit={handleCreate} />
            <h2>Issues</h2>
            <IssueList
              issues={issues}
              selectedId={selectedId}
              onSelect={setSelectedId}
              onDelete={handleDelete}
            />
          </section>
          <section>
            <h2>Edit</h2>
            {selected ? (
              <IssueEditor
                key={selected.id}
                mode="edit"
                issue={selected}
                onSubmit={(payload) => handleUpdate(selected.id, payload)}
              />
            ) : (
              <p>Select an issue to edit.</p>
            )}
          </section>
        </div>
      )}
    </main>
  );
}
