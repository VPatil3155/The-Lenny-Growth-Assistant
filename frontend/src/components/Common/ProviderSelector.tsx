import { useProvider } from "../../hooks/useProvider";

const PROVIDER_LABELS: Record<string, string> = {
  ollama: "Ollama",
  openai: "OpenAI",
};

export default function ProviderSelector() {
  const { provider, isLoading, error, switchProvider } = useProvider();

  const handleChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    switchProvider(e.target.value);
  };

  if (error && !provider) {
    return (
      <span className="provider-selector provider-selector--error">
        {error}
      </span>
    );
  }

  return (
    <div className="provider-selector">
      <label className="provider-selector-label" htmlFor="llm-provider">
        Provider
      </label>
      <select
        id="llm-provider"
        className="provider-selector-dropdown"
        value={provider?.active_provider ?? ""}
        onChange={handleChange}
        disabled={isLoading || !provider}
      >
        {!provider && <option value="">Loading...</option>}
        {provider?.supported_providers.map((p) => (
          <option key={p} value={p}>
            {PROVIDER_LABELS[p] ?? p}
          </option>
        ))}
      </select>
      {provider && (
        <span
          className={`provider-status-dot ${provider.available ? "provider-status-dot--ok" : "provider-status-dot--warn"}`}
          title={provider.message}
        />
      )}
    </div>
  );
}
