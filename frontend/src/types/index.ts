export interface Session {
  id: string;
  title: string;
  created_at: string;
  updated_at: string;
}

export interface CreateSessionRequest {
  title?: string | null;
}

export interface Message {
  id: string;
  session_id: string;
  role: "user" | "assistant" | "system";
  content: string;
  created_at: string;
}

export interface CreateMessageRequest {
  content: string;
  role?: "user";
}

export interface ChatTurnResponse {
  user_message: Message;
  assistant_message: Message;
  session?: Session;
}

export type ArtifactType =
  | "marketing_plan"
  | "email"
  | "growth_strategy"
  | "product_launch_plan"
  | "meeting_summary";

export interface GenerateArtifactRequest {
  artifact_type: ArtifactType;
  topic: string;
  additional_context?: string | null;
}

export interface ArtifactResponse {
  artifact_type: ArtifactType;
  title: string;
  content: string;
}

export interface ProviderInfo {
  active_provider: string;
  supported_providers: string[];
  available: boolean;
  message: string;
}
