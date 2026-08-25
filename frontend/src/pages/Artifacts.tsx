import { useState } from "react";
import type { ArtifactType, GenerateArtifactRequest } from "../types";
import { useArtifact } from "../hooks/useArtifact";
import { ArtifactPanel } from "../components/Artifact";

const ARTIFACT_TYPES: { value: ArtifactType; label: string }[] = [
  { value: "marketing_plan", label: "Marketing Plan" },
  { value: "email", label: "Email" },
  { value: "growth_strategy", label: "Growth Strategy" },
  { value: "product_launch_plan", label: "Product Launch Plan" },
  { value: "meeting_summary", label: "Meeting Summary" },
];

export default function Artifacts() {
  const { artifact, isGenerating, error, generate, clear } = useArtifact();
  const [artifactType, setArtifactType] = useState<ArtifactType>("marketing_plan");
  const [topic, setTopic] = useState("");
  const [additionalContext, setAdditionalContext] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const trimmedTopic = topic.trim();
    if (!trimmedTopic) return;

    const request: GenerateArtifactRequest = {
      artifact_type: artifactType,
      topic: trimmedTopic,
    };
    if (additionalContext.trim()) {
      request.additional_context = additionalContext.trim();
    }
    generate(request);
  };

  const hasPanel = artifact !== null || isGenerating || error !== null;

  return (
    <div className={`artifacts-layout ${hasPanel ? "artifacts-layout--split" : ""}`}>
      <div className="artifacts-form-container">
        <div className="artifacts-form-wrapper">
          <h1 className="artifacts-heading">Generate Artifact</h1>
          <p className="artifacts-subheading">
            Create structured documents powered by AI.
          </p>

          <form className="artifacts-form" onSubmit={handleSubmit}>
            <div className="artifacts-field">
              <label className="artifacts-label" htmlFor="artifact-type">
                Type
              </label>
              <select
                id="artifact-type"
                className="artifacts-select"
                value={artifactType}
                onChange={(e) => setArtifactType(e.target.value as ArtifactType)}
                disabled={isGenerating}
              >
                {ARTIFACT_TYPES.map((t) => (
                  <option key={t.value} value={t.value}>
                    {t.label}
                  </option>
                ))}
              </select>
            </div>

            <div className="artifacts-field">
              <label className="artifacts-label" htmlFor="artifact-topic">
                Topic
              </label>
              <input
                id="artifact-topic"
                className="artifacts-input"
                type="text"
                placeholder="e.g. AI resume builder launch campaign"
                value={topic}
                onChange={(e) => setTopic(e.target.value)}
                disabled={isGenerating}
                required
              />
            </div>

            <div className="artifacts-field">
              <label className="artifacts-label" htmlFor="artifact-context">
                Additional Context{" "}
                <span className="artifacts-label-hint">(optional)</span>
              </label>
              <textarea
                id="artifact-context"
                className="artifacts-textarea"
                placeholder="Any extra details to include..."
                value={additionalContext}
                onChange={(e) => setAdditionalContext(e.target.value)}
                disabled={isGenerating}
                rows={3}
              />
            </div>

            <div className="artifacts-form-actions">
              <button
                type="submit"
                className="artifacts-submit-btn"
                disabled={isGenerating || !topic.trim()}
              >
                {isGenerating ? "Generating..." : "Generate"}
              </button>
              {artifact && (
                <button
                  type="button"
                  className="artifacts-clear-btn"
                  onClick={clear}
                >
                  Clear
                </button>
              )}
            </div>
          </form>

          {error && artifact && (
            <div className="artifacts-inline-error">{error}</div>
          )}
        </div>
      </div>

      <ArtifactPanel
        artifact={artifact}
        isGenerating={isGenerating}
        error={error}
        onClose={clear}
      />
    </div>
  );
}
