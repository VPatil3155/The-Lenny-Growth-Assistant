import Markdown from "react-markdown";
import type { Message } from "../../types";

interface MessageBubbleProps {
  message: Message;
}

export default function MessageBubble({ message }: MessageBubbleProps) {
  const isUser = message.role === "user";

  return (
    <div className={`message ${isUser ? "message--user" : "message--assistant"}`}>
      <div className="message-avatar">{isUser ? "You" : "AI"}</div>
      <div className="message-body">
        {isUser ? (
          <p className="message-text">{message.content}</p>
        ) : (
          <div className="message-text message-markdown">
            <Markdown>{message.content}</Markdown>
          </div>
        )}
      </div>
    </div>
  );
}
