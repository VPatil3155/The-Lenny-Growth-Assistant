import type { ArtifactResponse } from "../../types";
import ArtifactViewer from "./ArtifactViewer";

interface ArtifactPanelProps {
  artifact: ArtifactResponse | null;
  isGenerating: boolean;
  error: string | null;
  onClose: () => void;
}

export default function ArtifactPanel({
  artifact,
  isGenerating,
  error,
  onClose,
}: ArtifactPanelProps) {
  const isVisible = artifact !== null || isGenerating || error !== null;

  return (
    <div className={`artifact-panel ${isVisible ? "artifact-panel--open" : ""}`}>
      <button
        className="artifact-panel-close"
        onClick={onClose}
        title="Close panel"
      >
        &times;
      </button>

      {isGenerating && !artifact && (
        <div className="artifact-panel-state">
          <div className="artifact-spinner" />
          <p>Generating artifact...</p>
        </div>
      )}

      {error && !artifact && (
        <div className="artifact-panel-state artifact-panel-state--error">
          <p>{error}</p>
          <button className="artifact-action-btn" onClick={onClose}>
            Dismiss
          </button>
        </div>
      )}

      {artifact && (
        <ArtifactViewer artifact={artifact} />
      )}

      {!isGenerating && !error && !artifact && (
        <div className="artifact-panel-state">
          <p>No artifact generated yet.</p>
        </div>
      )}
    </div>
  );
}
