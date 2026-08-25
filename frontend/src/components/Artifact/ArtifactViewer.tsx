import { useCallback, useState } from "react";
import Markdown from "react-markdown";
import rehypeRaw from "rehype-raw";
import DOMPurify from "dompurify";
import type { Plugin } from "unified";
import type { Root } from "hast";
import type { ArtifactResponse } from "../../types";

const rehypeSanitizeDomPurify: Plugin<[], Root> = () => (tree) => {
  const rawHtml = String(tree);
  const clean = DOMPurify.sanitize(rawHtml, { USE_PROFILES: { html: true } });
  tree.children = [
    { type: "raw", value: clean } as unknown as (typeof tree.children)[number],
  ];
};

interface ArtifactViewerProps {
  artifact: ArtifactResponse;
}

export default function ArtifactViewer({ artifact }: ArtifactViewerProps) {
  const [copied, setCopied] = useState(false);

  const handleCopy = useCallback(async () => {
    try {
      await navigator.clipboard.writeText(artifact.content);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch {
      const textarea = document.createElement("textarea");
      textarea.value = artifact.content;
      document.body.appendChild(textarea);
      textarea.select();
      document.execCommand("copy");
      document.body.removeChild(textarea);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  }, [artifact.content]);

  const handleDownload = useCallback(() => {
    const filename = `${artifact.title.replace(/[^a-z0-9]/gi, "_").toLowerCase()}.md`;
    const blob = new Blob([artifact.content], { type: "text/markdown;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  }, [artifact.title, artifact.content]);

  const typeLabel = artifact.artifact_type
    .replace(/_/g, " ")
    .replace(/\b\w/g, (c) => c.toUpperCase());

  return (
    <div className="artifact-viewer">
      <div className="artifact-viewer-header">
        <div className="artifact-viewer-meta">
          <span className="artifact-viewer-badge">{typeLabel}</span>
          <h2 className="artifact-viewer-title">{artifact.title}</h2>
        </div>
        <div className="artifact-viewer-actions">
          <button
            className="artifact-action-btn"
            onClick={handleCopy}
            title="Copy content"
          >
            {copied ? "Copied!" : "Copy"}
          </button>
          <button
            className="artifact-action-btn"
            onClick={handleDownload}
            title="Download as Markdown"
          >
            Download .md
          </button>
        </div>
      </div>

      <div className="artifact-viewer-body">
        <div className="artifact-markdown">
          <Markdown rehypePlugins={[rehypeRaw, rehypeSanitizeDomPurify]}>
            {artifact.content}
          </Markdown>
        </div>
      </div>
    </div>
  );
}
