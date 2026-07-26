import type { Issue, IssueCreate, IssueUpdate } from "./types";

// Relative URL — browser hits Vite (:5173), proxy forwards /api to FastAPI (:8000).
// Do NOT hardcode http://localhost:8000 here; that would bypass the proxy and hit CORS.
const API = "/api/v1/issues/";

async function request<T>(url: string, init?: RequestInit): Promise<T> {
  const response = await fetch(url, {
    headers: { "Content-Type": "application/json", ...init?.headers },
    ...init,
  });

  if (!response.ok) {
    const detail = await response.text();
    throw new Error(detail || `Request failed (${response.status})`);
  }

  // DELETE returns 204 No Content — nothing to parse.
  if (response.status === 204) {
    return undefined as T;
  }

  return response.json() as Promise<T>;
}

export function listIssues(): Promise<Issue[]> {
  return request<Issue[]>(API);
}

export function getIssue(id: string): Promise<Issue> {
  return request<Issue>(`${API}${id}`);
}

export function createIssue(payload: IssueCreate): Promise<Issue> {
  return request<Issue>(API, {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function updateIssue(id: string, payload: IssueUpdate): Promise<Issue> {
  return request<Issue>(`${API}${id}`, {
    method: "PUT",
    body: JSON.stringify(payload),
  });
}

export function deleteIssue(id: string): Promise<void> {
  return request<void>(`${API}${id}`, { method: "DELETE" });
}
