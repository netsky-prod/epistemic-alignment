import { evidenceAnchorId } from "./EvidenceReference";

type EvidenceEntry = { source: string; excerpt: string; status?: string; related?: string[] };

export function EvidenceIndex({ entries }: { entries: EvidenceEntry[] }) {
  return <section className="evidence-index" aria-labelledby="evidence-index-title"><h3 id="evidence-index-title">Evidence index</h3><p>Each target shows the cited dossier source and a substantive review excerpt. Canonical evidence remains in the dossier.</p><ul>{entries.map((entry) => <li id={evidenceAnchorId(entry.source)} key={entry.source} tabIndex={-1}><code>{entry.source}</code>{entry.status && <p><strong>Status:</strong> {entry.status}</p>}<blockquote>{entry.excerpt}</blockquote>{entry.related?.length ? <p><strong>Related:</strong> {entry.related.join(", ")}</p> : null}</li>)}</ul></section>;
}
