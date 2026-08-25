import { useCallback, useEffect, useRef, useState } from "react";
import type { Message, Session } from "../types";
import {
  createSession as apiCreateSession,
  deleteSession as apiDeleteSession,
  getMessages as apiGetMessages,
  getSessions as apiGetSessions,
  sendMessage as apiSendMessage,
  updateSession as apiUpdateSession,
} from "../services/api";

export interface ChatState {
  sessions: Session[];
  activeSessionId: string | null;
  messages: Message[];
  isLoadingSessions: boolean;
  isLoadingMessages: boolean;
  isSending: boolean;
  error: string | null;
}

export interface ChatActions {
  loadSessions: () => Promise<void>;
  createNewSession: () => Promise<Session>;
  selectSession: (sessionId: string) => void;
  send: (content: string) => Promise<void>;
  deleteSession: (sessionId: string) => Promise<void>;
  renameSession: (sessionId: string, title: string) => Promise<void>;
}

export function useChat(): ChatState & ChatActions {
  const [sessions, setSessions] = useState<Session[]>([]);
  const [activeSessionId, setActiveSessionId] = useState<string | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoadingSessions, setIsLoadingSessions] = useState(false);
  const [isLoadingMessages, setIsLoadingMessages] = useState(false);
  const [isSending, setIsSending] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const abortRef = useRef(false);

  const loadSessions = useCallback(async () => {
    setIsLoadingSessions(true);
    setError(null);
    try {
      const data = await apiGetSessions();
      setSessions(data);
    } catch {
      setError("Failed to load sessions.");
    } finally {
      setIsLoadingSessions(false);
    }
  }, []);

  useEffect(() => {
    loadSessions();
  }, [loadSessions]);

  useEffect(() => {
    if (!activeSessionId) {
      setMessages([]);
      return;
    }

    let cancelled = false;

    async function fetchMessages() {
      setIsLoadingMessages(true);
      setError(null);
      try {
        const data = await apiGetMessages(activeSessionId!);
        if (!cancelled) setMessages(data);
      } catch {
        if (!cancelled) setError("Failed to load messages.");
      } finally {
        if (!cancelled) setIsLoadingMessages(false);
      }
    }

    fetchMessages();

    return () => {
      cancelled = true;
    };
  }, [activeSessionId]);

  const createNewSession = useCallback(async (): Promise<Session> => {
    setError(null);
    const session = await apiCreateSession();
    setSessions((prev) => [session, ...prev]);
    setActiveSessionId(session.id);
    return session;
  }, []);

  const selectSession = useCallback((sessionId: string) => {
    setActiveSessionId(sessionId);
  }, []);

  const send = useCallback(
    async (content: string) => {
      if (!activeSessionId || isSending) return;

      setIsSending(true);
      setError(null);
      abortRef.current = false;

      try {
        const turn = await apiSendMessage(activeSessionId, { content });
        if (!abortRef.current) {
          setMessages((prev) => [
            ...prev,
            turn.user_message,
            turn.assistant_message,
          ]);

          setSessions((prev) =>
            prev.map((s) => {
              if (s.id !== activeSessionId) return s;
              const updated = {
                ...s,
                updated_at: turn.assistant_message.created_at,
              };
              if (turn.session) {
                updated.title = turn.session.title;
              }
              return updated;
            }),
          );
        }
      } catch {
        if (!abortRef.current) {
          setError("Failed to send message.");
        }
      } finally {
        setIsSending(false);
      }
    },
    [activeSessionId, isSending],
  );

  const deleteSessionHandler = useCallback(
    async (sessionId: string) => {
      setError(null);
      try {
        await apiDeleteSession(sessionId);
        setSessions((prev) => prev.filter((s) => s.id !== sessionId));
        if (activeSessionId === sessionId) {
          setActiveSessionId(null);
          setMessages([]);
        }
      } catch {
        setError("Failed to delete session.");
      }
    },
    [activeSessionId],
  );

  const renameSession = useCallback(
    async (sessionId: string, title: string) => {
      setError(null);
      try {
        const updated = await apiUpdateSession(sessionId, title);
        setSessions((prev) =>
          prev.map((s) => (s.id === sessionId ? updated : s)),
        );
      } catch {
        setError("Failed to rename session.");
      }
    },
    [],
  );

  return {
    sessions,
    activeSessionId,
    messages,
    isLoadingSessions,
    isLoadingMessages,
    isSending,
    error,
    loadSessions,
    createNewSession,
    selectSession,
    send,
    deleteSession: deleteSessionHandler,
    renameSession,
  };
}
