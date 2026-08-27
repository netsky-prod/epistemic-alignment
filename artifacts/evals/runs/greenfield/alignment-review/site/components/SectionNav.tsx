const sections = [
  ["summary", "Summary"], ["stakeholders", "Stakeholders"], ["use-cases", "Use cases"],
  ["behavior", "Behavior"], ["architecture", "Architecture"], ["decisions-and-risks", "Decisions & risks"], ["review-readiness", "Readiness"],
] as const;

export function SectionNav() {
  return <nav className="section-nav" aria-label="Review sections"><ol>{sections.map(([id, label]) => <li key={id}><a href={`#${id}`}>{label}</a></li>)}</ol></nav>;
}
