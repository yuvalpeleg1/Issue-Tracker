import { useState, type FormEvent } from "react";
import type { Issue, IssueCreate, IssuePriority, IssueStatus, IssueUpdate } from "../types";

interface CreateProps {
  mode: "create";
  onSubmit: (payload: IssueCreate) => void | Promise<void>;
}

interface EditProps {
  mode: "edit";
  issue: Issue;
  onSubmit: (payload: IssueUpdate) => void | Promise<void>;
}

type IssueEditorProps = CreateProps | EditProps;

export default function IssueEditor(props: IssueEditorProps) {
  const isEdit = props.mode === "edit";
  const [title, setTitle] = useState(isEdit ? props.issue.title : "");
  const [description, setDescription] = useState(isEdit ? props.issue.description : "");
  const [priority, setPriority] = useState<IssuePriority>(
    isEdit ? props.issue.priority : "medium",
  );
  const [status, setStatus] = useState<IssueStatus>(isEdit ? props.issue.status : "open");

  async function handleSubmit(event: FormEvent) {
    event.preventDefault();

    if (props.mode === "create") {
      await props.onSubmit({ title, description, priority });
      setTitle("");
      setDescription("");
      setPriority("medium");
      return;
    }

    await props.onSubmit({ title, description, priority, status });
  }

  return (
    <form className="issue-editor" onSubmit={handleSubmit}>
      <input
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        placeholder="Title"
        required
        minLength={3}
        maxLength={100}
      />
      <textarea
        value={description}
        onChange={(e) => setDescription(e.target.value)}
        placeholder="Description"
        required
        minLength={5}
        maxLength={1000}
      />
      <select
        value={priority}
        onChange={(e) => setPriority(e.target.value as IssuePriority)}
      >
        <option value="low">low</option>
        <option value="medium">medium</option>
        <option value="high">high</option>
      </select>
      {isEdit && (
        <select
          value={status}
          onChange={(e) => setStatus(e.target.value as IssueStatus)}
        >
          <option value="open">open</option>
          <option value="in_progress">in_progress</option>
          <option value="closed">closed</option>
        </select>
      )}
      <button type="submit">{isEdit ? "Save" : "Create"}</button>
    </form>
  );
}
