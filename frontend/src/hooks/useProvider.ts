import { useCallback, useEffect, useState } from "react";
import type { ProviderInfo } from "../types";
import {
  getProviderInfo as apiGetProviderInfo,
  setProvider as apiSetProvider,
} from "../services/api";

const STORAGE_KEY = "lenny-llm-provider";

export interface ProviderState {
  provider: ProviderInfo | null;
  isLoading: boolean;
  error: string | null;
}

export interface ProviderActions {
  fetchProvider: () => Promise<void>;
  switchProvider: (provider: string) => Promise<void>;
}

export function useProvider(): ProviderState & ProviderActions {
  const [provider, setProvider] = useState<ProviderInfo | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchProvider = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    try {
      const info = await apiGetProviderInfo();
      setProvider(info);
      localStorage.setItem(STORAGE_KEY, info.active_provider);
    } catch {
      setError("Failed to load provider info.");
    } finally {
      setIsLoading(false);
    }
  }, []);

  const switchProvider = useCallback(
    async (providerName: string) => {
      setIsLoading(true);
      setError(null);
      try {
        const info = await apiSetProvider(providerName);
        setProvider(info);
        localStorage.setItem(STORAGE_KEY, info.active_provider);
      } catch {
        setError("Failed to switch provider.");
      } finally {
        setIsLoading(false);
      }
    },
    [],
  );

  useEffect(() => {
    fetchProvider();
  }, [fetchProvider]);

  return { provider, isLoading, error, fetchProvider, switchProvider };
}
