import axios from "axios";
import type {
  ArtifactResponse,
  ChatTurnResponse,
  CreateMessageRequest,
  CreateSessionRequest,
  GenerateArtifactRequest,
  Message,
  ProviderInfo,
  Session,
} from "../types";

const apiClient = axios.create({
  baseURL: "http://127.0.0.1:8000",
  headers: {
    "Content-Type": "application/json",
  },
});

export async function createSession(
  data?: CreateSessionRequest,
): Promise<Session> {
  const response = await apiClient.post<Session>("/sessions", data ?? {});
  return response.data;
}

export async function getSessions(): Promise<Session[]> {
  const response = await apiClient.get<Session[]>("/sessions");
  return response.data;
}

export async function getSession(sessionId: string): Promise<Session> {
  const response = await apiClient.get<Session>(`/sessions/${sessionId}`);
  return response.data;
}

export async function deleteSession(sessionId: string): Promise<void> {
  await apiClient.delete(`/sessions/${sessionId}`);
}

export async function updateSession(
  sessionId: string,
  title: string,
): Promise<Session> {
  const response = await apiClient.patch<Session>(`/sessions/${sessionId}`, {
    title,
  });
  return response.data;
}

export async function getMessages(sessionId: string): Promise<Message[]> {
  const response = await apiClient.get<Message[]>(
    `/sessions/${sessionId}/messages`,
  );
  return response.data;
}

export async function sendMessage(
  sessionId: string,
  data: CreateMessageRequest,
): Promise<ChatTurnResponse> {
  const response = await apiClient.post<ChatTurnResponse>(
    `/sessions/${sessionId}/messages`,
    data,
  );
  return response.data;
}

export async function generateArtifact(
  data: GenerateArtifactRequest,
): Promise<ArtifactResponse> {
  const response = await apiClient.post<ArtifactResponse>(
    "/artifacts/generate",
    data,
  );
  return response.data;
}

export async function getProviderInfo(): Promise<ProviderInfo> {
  const response = await apiClient.get<ProviderInfo>("/provider");
  return response.data;
}

export async function setProvider(provider: string): Promise<ProviderInfo> {
  const response = await apiClient.post<ProviderInfo>("/provider", {
    provider,
  });
  return response.data;
}

export default apiClient;
