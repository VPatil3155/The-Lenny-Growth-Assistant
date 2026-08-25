import { useCallback, useState } from "react";
import type { ArtifactResponse, GenerateArtifactRequest } from "../types";
import { generateArtifact as apiGenerateArtifact } from "../services/api";

export interface ArtifactState {
  artifact: ArtifactResponse | null;
  isGenerating: boolean;
  error: string | null;
}

export interface ArtifactActions {
  generate: (request: GenerateArtifactRequest) => Promise<void>;
  clear: () => void;
}

export function useArtifact(): ArtifactState & ArtifactActions {
  const [artifact, setArtifact] = useState<ArtifactResponse | null>(null);
  const [isGenerating, setIsGenerating] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const generate = useCallback(async (request: GenerateArtifactRequest) => {
    setIsGenerating(true);
    setError(null);
    try {
      const result = await apiGenerateArtifact(request);
      setArtifact(result);
    } catch {
      setError("Failed to generate artifact. Please try again.");
    } finally {
      setIsGenerating(false);
    }
  }, []);

  const clear = useCallback(() => {
    setArtifact(null);
    setError(null);
  }, []);

  return { artifact, isGenerating, error, generate, clear };
}
