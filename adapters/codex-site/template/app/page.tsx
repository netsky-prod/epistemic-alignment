import review from "../public/review.json";
import { C4Diagram } from "../components/C4Diagram";
import { EvidenceIndex } from "../components/EvidenceIndex";
import { EvidenceReference } from "../components/EvidenceReference";
import { FindingsPanel } from "../components/FindingsPanel";
import { SectionNav } from "../components/SectionNav";
import { Shell } from "../components/Shell";
import { StatusBadge } from "../components/StatusBadge";

type ReviewItem = { id: string; title: string; detail: string; status?: string; source: string };
type Stakeholder = ReviewItem & { role: string };
type Architecture = { c4Source: string; source: string; responsibilities: ReviewItem[] };
type EvidenceEntry = { source: string; excerpt: string; status?: string; related?: string[] };
type ReviewData = {
  project: { name: string; source: string };
  summary: { title: string; detail: string; source: string; goals: ReviewItem[]; evidence: EvidenceEntry[] };
  stakeholders: Stakeholder[];
  useCases: ReviewItem[];
  behavior: ReviewItem[];
  architecture: Architecture;
  decisions: ReviewItem[];
  risks: ReviewItem[];
  findings: ReviewItem[];
  snapshot: {
    mode?: "conversational" | "exact-snapshot";
    algorithm?: string | null;
    digest?: string | null;
    status: string;
    paths: string[];
    note?: string;
  };
};

const data = review as ReviewData;

function LinkedItems({ items }: { items: ReviewItem[] }) {
  return <ul className="item-list">{items.map((item) => <li key={item.id} className="item-card"><div className="item-heading"><strong>{item.id}: {item.title}</strong>{item.status && <StatusBadge status={item.status} />}</div><p>{item.detail}</p><EvidenceReference source={item.source} /></li>)}</ul>;
}

function referencedSources(reviewData: ReviewData) {
  return [...new Set([
    reviewData.project.source,
    reviewData.summary.source,
    ...reviewData.summary.goals.map((item) => item.source),
    ...reviewData.stakeholders.map((item) => item.source),
    ...reviewData.useCases.map((item) => item.source),
    ...reviewData.behavior.map((item) => item.source),
    reviewData.architecture.source,
    ...reviewData.architecture.responsibilities.map((item) => item.source),
    ...reviewData.decisions.map((item) => item.source),
    ...reviewData.risks.map((item) => item.source),
    ...reviewData.findings.map((item) => item.source),
  ])].sort();
}

export default function Home() {
  const evidenceSources = referencedSources(data);
  const evidenceEntries = [...data.summary.evidence].sort((left, right) => left.source.localeCompare(right.source));
  const missingEvidence = evidenceSources.filter((source) => !evidenceEntries.some((entry) => entry.source === source));
  if (missingEvidence.length) throw new Error(`Missing substantive evidence for: ${missingEvidence.join(", ")}`);
  const exactSnapshot = data.snapshot.mode === "exact-snapshot" && data.snapshot.algorithm && data.snapshot.digest;
  return <Shell project={data.project.name} source={data.project.source}><SectionNav /><main id="main-content" className="review-content" tabIndex={-1}>
    <section id="summary" aria-labelledby="summary-title"><p className="eyebrow">Dossier review</p><h1 id="summary-title">{data.summary.title}</h1><p className="lede">{data.summary.detail}</p><EvidenceReference source={data.summary.source} /><h2>Goals</h2><LinkedItems items={data.summary.goals} /></section>
    <section id="stakeholders" aria-labelledby="stakeholders-title"><h2 id="stakeholders-title">Stakeholders and glossary</h2><ul className="stakeholder-grid">{data.stakeholders.map((stakeholder) => <li key={stakeholder.id}><strong>{stakeholder.title}</strong><span>{stakeholder.role}</span><p>{stakeholder.detail}</p>{stakeholder.status && <StatusBadge status={stakeholder.status} />}<EvidenceReference source={stakeholder.source} /></li>)}</ul></section>
    <section id="use-cases" aria-labelledby="use-cases-title"><h2 id="use-cases-title">Cockburn use cases</h2><LinkedItems items={data.useCases} /></section>
    <section id="behavior" aria-labelledby="behavior-title"><h2 id="behavior-title">BDD examples</h2><LinkedItems items={data.behavior} /></section>
    <section id="architecture" aria-labelledby="architecture-title"><h2 id="architecture-title">C4 architecture and responsibilities</h2><C4Diagram source={data.architecture.c4Source} /><EvidenceReference source={data.architecture.source} /><h3>Responsibility map</h3><LinkedItems items={data.architecture.responsibilities} /></section>
    <section id="decisions-and-risks" aria-labelledby="decisions-title"><h2 id="decisions-title">Decisions and risks</h2><h3>ADRs and open decisions</h3><LinkedItems items={data.decisions} /><h3>Assumptions, contradictions, questions, and risks</h3><LinkedItems items={data.risks} /></section>
    <section id="review-readiness" aria-labelledby="readiness-title"><h2 id="readiness-title">Review readiness</h2><FindingsPanel findings={data.findings} /><aside className="snapshot-panel" aria-labelledby="snapshot-title"><h3 id="snapshot-title">Review binding</h3><dl><dt>Binding</dt><dd>{exactSnapshot ? <code>{data.snapshot.algorithm}:{data.snapshot.digest}</code> : "Conversational — not exact-byte bound"}</dd><dt>State</dt><dd><StatusBadge status={data.snapshot.status} /></dd></dl>{data.snapshot.note && <p>{data.snapshot.note}</p>}<p>This page presents evidence only. Explicit human consent remains in the host conversation; this Site cannot record approval.</p><details><summary>Reviewed source paths</summary><ul>{data.snapshot.paths.map((path) => <li key={path}><code>{path}</code></li>)}</ul></details></aside><EvidenceIndex entries={evidenceEntries} /></section>
  </main></Shell>;
}
