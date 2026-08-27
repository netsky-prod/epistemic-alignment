export function evidenceAnchorId(source: string) {
  const encodedSource = Array.from(source, (character) =>
    character.codePointAt(0)!.toString(16).padStart(6, "0"),
  ).join("-");
  return `evidence-source-${encodedSource}`;
}

export function EvidenceReference({ source }: { source: string }) {
  return <p><a className="evidence-reference" href={`#${evidenceAnchorId(source)}`} aria-label={`Open evidence index entry for ${source}`}>Evidence: <code>{source}</code></a></p>;
}
