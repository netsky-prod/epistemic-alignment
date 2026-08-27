import review from "../public/review.json";
import { C4Diagram } from "../components/C4Diagram";
import { FindingsPanel } from "../components/FindingsPanel";
import { SectionNav } from "../components/SectionNav";
import { Shell } from "../components/Shell";
import { StatusBadge } from "../components/StatusBadge";

type ReviewItem = { id: string; title: string; detail: string; status?: string; source?: string };
type Stakeholder = ReviewItem & { role: string };
type Architecture = { c4Source: string; responsibilities: ReviewItem[] };
type ReviewData = {
  project: { name: string; source: string };
  summary: { title: string; detail: string; goals: ReviewItem[] };
  stakeholders: Stakeholder[];
  useCases: ReviewItem[];
  behavior: ReviewItem[];
  architecture: Architecture;
  decisions: ReviewItem[];
  risks: ReviewItem[];
  findings: ReviewItem[];
  snapshot: { algorithm: string; digest: string; status: string; paths: string[] };
};

const data = review as ReviewData;

function LinkedItems({ items }: { items: ReviewItem[] }) {
  return <ul className="item-list">{items.map((item) => <li key={item.id} className="item-card"><div className="item-heading"><strong>{item.id}: {item.title}</strong>{item.status && <StatusBadge status={item.status} />}</div><p>{item.detail}</p>{item.source && <a href={item.source}>Source: {item.source}</a>}</li>)}</ul>;
}

export default function Home() {
  return <Shell project={data.project.name} source={data.project.source}><SectionNav /><main id="main-content" className="review-content" tabIndex={-1}>
    <section id="summary" aria-labelledby="summary-title"><p className="eyebrow">Dossier review</p><h1 id="summary-title">{data.summary.title}</h1><p className="lede">{data.summary.detail}</p><h2>Goals</h2><LinkedItems items={data.summary.goals} /></section>
    <section id="stakeholders" aria-labelledby="stakeholders-title"><h2 id="stakeholders-title">Stakeholders and glossary</h2><ul className="stakeholder-grid">{data.stakeholders.map((stakeholder) => <li key={stakeholder.id}><strong>{stakeholder.title}</strong><span>{stakeholder.role}</span><p>{stakeholder.detail}</p>{stakeholder.status && <StatusBadge status={stakeholder.status} />}</li>)}</ul></section>
    <section id="use-cases" aria-labelledby="use-cases-title"><h2 id="use-cases-title">Cockburn use cases</h2><LinkedItems items={data.useCases} /></section>
    <section id="behavior" aria-labelledby="behavior-title"><h2 id="behavior-title">BDD examples</h2><LinkedItems items={data.behavior} /></section>
    <section id="architecture" aria-labelledby="architecture-title"><h2 id="architecture-title">C4 architecture and responsibilities</h2><C4Diagram source={data.architecture.c4Source} /><h3>Responsibility map</h3><LinkedItems items={data.architecture.responsibilities} /></section>
    <section id="decisions-and-risks" aria-labelledby="decisions-title"><h2 id="decisions-title">Decisions and risks</h2><h3>ADRs and open decisions</h3><LinkedItems items={data.decisions} /><h3>Assumptions, contradictions, questions, and risks</h3><LinkedItems items={data.risks} /></section>
    <section id="review-readiness" aria-labelledby="readiness-title"><h2 id="readiness-title">Review readiness</h2><FindingsPanel findings={data.findings} /><aside className="snapshot-panel" aria-labelledby="snapshot-title"><h3 id="snapshot-title">Snapshot readiness</h3><dl><dt>Snapshot hash</dt><dd><code>{data.snapshot.algorithm}:{data.snapshot.digest}</code></dd><dt>State</dt><dd><StatusBadge status={data.snapshot.status} /></dd></dl><p>This page presents evidence only. Explicit human consent remains in the host conversation; this Site cannot record approval.</p><details><summary>Included snapshot paths</summary><ul>{data.snapshot.paths.map((path) => <li key={path}><code>{path}</code></li>)}</ul></details></aside></section>
  </main></Shell>;
}
