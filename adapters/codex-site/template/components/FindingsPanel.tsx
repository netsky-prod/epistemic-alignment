import { StatusBadge } from "./StatusBadge";

type Finding = { id: string; title: string; detail: string; status?: string; source?: string };

export function FindingsPanel({ findings }: { findings: Finding[] }) {
  return <section className="findings-panel" aria-labelledby="findings-title"><h3 id="findings-title">Review findings</h3><p>These findings remain visible for human judgment; the presentation does not resolve them.</p><ul>{findings.map((finding) => <li key={finding.id}><div><strong>{finding.id}: {finding.title}</strong>{finding.status && <StatusBadge status={finding.status} />}</div><p>{finding.detail}</p>{finding.source && <a href={finding.source}>Source: {finding.source}</a>}</li>)}</ul></section>;
}
