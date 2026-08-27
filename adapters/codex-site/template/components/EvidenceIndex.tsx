import { evidenceAnchorId } from "./EvidenceReference";

export function EvidenceIndex({ sources }: { sources: string[] }) {
  return <section className="evidence-index" aria-labelledby="evidence-index-title"><h3 id="evidence-index-title">Evidence index</h3><p>Each review reference resolves here while preserving the dossier path or stable ID shown in the source.</p><ul>{sources.map((source) => <li id={evidenceAnchorId(source)} key={source} tabIndex={-1}><code>{source}</code></li>)}</ul></section>;
}
