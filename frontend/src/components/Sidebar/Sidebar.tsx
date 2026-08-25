import { useCallback, useRef, useState } from "react";
import type { Session } from "../../types";

interface SidebarProps {
  sessions: Session[];
  activeSessionId: string | null;
  isLoading: boolean;
  onSelect: (sessionId: string) => void;
  onDelete: (sessionId: string) => void;
  onRename: (sessionId: string, title: string) => void;
  onNew: () => void;
}

function formatTime(iso: string): string {
  const date = new Date(iso);
  return date.toLocaleDateString(undefined, {
    month: "short",
    day: "numeric",
  });
}

function EditableTitle({
  session,
  isActive,
  onRename,
}: {
  session: Session;
  isActive: boolean;
  onRename: (sessionId: string, title: string) => void;
}) {
  const [isEditing, setIsEditing] = useState(false);
  const [draft, setDraft] = useState(session.title);
  const inputRef = useRef<HTMLInputElement>(null);

  const commit = useCallback(() => {
    const trimmed = draft.trim();
    if (trimmed && trimmed !== session.title) {
      onRename(session.id, trimmed);
    } else {
      setDraft(session.title);
    }
    setIsEditing(false);
  }, [draft, session.id, session.title, onRename]);

  const handleDoubleClick = useCallback(() => {
    setDraft(session.title);
    setIsEditing(true);
    setTimeout(() => inputRef.current?.select(), 0);
  }, [session.title]);

  const handleKeyDown = useCallback(
    (e: React.KeyboardEvent<HTMLInputElement>) => {
      if (e.key === "Enter") {
        e.preventDefault();
        commit();
      } else if (e.key === "Escape") {
        setDraft(session.title);
        setIsEditing(false);
      }
    },
    [commit, session.title],
  );

  if (isEditing) {
    return (
      <input
        ref={inputRef}
        className="sidebar-item-title-input"
        value={draft}
        onChange={(e) => setDraft(e.target.value)}
        onBlur={commit}
        onKeyDown={handleKeyDown}
        onClick={(e) => e.stopPropagation()}
        maxLength={255}
        autoFocus
      />
    );
  }

  return (
    <span
      className={`sidebar-item-title ${isActive ? "sidebar-item-title--active" : ""}`}
      onDoubleClick={handleDoubleClick}
    >
      {session.title}
    </span>
  );
}

export default function Sidebar({
  sessions,
  activeSessionId,
  isLoading,
  onSelect,
  onDelete,
  onRename,
  onNew,
}: SidebarProps) {
  return (
    <aside className="sidebar">
      <div className="sidebar-header">
        <h2>Chats</h2>
        <button
          className="sidebar-new-btn"
          onClick={onNew}
          disabled={isLoading}
        >
          + New Chat
        </button>
      </div>

      <div className="sidebar-list">
        {isLoading && <p className="sidebar-empty">Loading...</p>}

        {!isLoading && sessions.length === 0 && (
          <p className="sidebar-empty">No conversations yet.</p>
        )}

        {sessions.map((session) => (
          <div
            key={session.id}
            className={`sidebar-item ${session.id === activeSessionId ? "sidebar-item--active" : ""}`}
            onClick={() => onSelect(session.id)}
          >
            <div className="sidebar-item-content">
              <EditableTitle
                session={session}
                isActive={session.id === activeSessionId}
                onRename={onRename}
              />
              <span className="sidebar-item-date">
                {formatTime(session.updated_at)}
              </span>
            </div>
            <button
              className="sidebar-item-delete"
              onClick={(e) => {
                e.stopPropagation();
                onDelete(session.id);
              }}
              title="Delete chat"
            >
              &times;
            </button>
          </div>
        ))}
      </div>
    </aside>
  );
}
