import { useEffect, useRef } from "react";
import type { Message } from "../../types";
import MessageBubble from "./MessageBubble";

interface ChatWindowProps {
  messages: Message[];
  isLoading: boolean;
  hasActiveSession: boolean;
}

export default function ChatWindow({
  messages,
  isLoading,
  hasActiveSession,
}: ChatWindowProps) {
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isLoading]);

  if (!hasActiveSession) {
    return (
      <div className="chat-window chat-window--empty">
        <p>Select a chat or start a new one.</p>
      </div>
    );
  }

  return (
    <div className="chat-window">
      <div className="chat-messages">
        {messages.length === 0 && !isLoading && (
          <div className="chat-window--empty">
            <p>No messages yet. Say something!</p>
          </div>
        )}

        {messages.map((msg) => (
          <MessageBubble key={msg.id} message={msg} />
        ))}

        {isLoading && (
          <div className="message message--assistant">
            <div className="message-avatar">AI</div>
            <div className="message-body">
              <div className="typing-indicator">
                <span className="dot" />
                <span className="dot" />
                <span className="dot" />
              </div>
            </div>
          </div>
        )}

        <div ref={bottomRef} />
      </div>
    </div>
  );
}
