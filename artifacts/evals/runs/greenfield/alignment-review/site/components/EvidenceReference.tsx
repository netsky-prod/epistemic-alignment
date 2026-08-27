export function EvidenceReference({ source }: { source: string }) {
  return <p className="evidence-reference">Evidence: <code>{source}</code></p>;
}
