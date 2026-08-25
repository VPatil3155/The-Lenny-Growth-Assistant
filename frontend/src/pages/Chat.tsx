import { useChat } from "../hooks/useChat";
import { Sidebar } from "../components/Sidebar";
import { ChatWindow, MessageInput } from "../components/Chat";

export default function Chat() {
  const {
    sessions,
    activeSessionId,
    messages,
    isLoadingSessions,
    isLoadingMessages,
    isSending,
    error,
    createNewSession,
    selectSession,
    send,
    deleteSession,
    renameSession,
  } = useChat();

  const isBusy = isSending || isLoadingMessages;

  return (
    <div className="chat-layout">
      <Sidebar
        sessions={sessions}
        activeSessionId={activeSessionId}
        isLoading={isLoadingSessions}
        onSelect={selectSession}
        onDelete={deleteSession}
        onRename={renameSession}
        onNew={createNewSession}
      />

      <main className="chat-main">
        {error && <div className="chat-error">{error}</div>}

        <ChatWindow
          messages={messages}
          isLoading={isSending}
          hasActiveSession={activeSessionId !== null}
        />

        <MessageInput
          onSend={send}
          disabled={!activeSessionId || isBusy}
        />
      </main>
    </div>
  );
}
