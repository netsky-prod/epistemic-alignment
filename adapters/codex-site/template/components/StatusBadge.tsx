const labels: Record<string, string> = {
  confirmed: "Confirmed",
  proposed: "Proposed",
  uncertain: "Uncertain",
  conflicting: "Conflicting",
  blocked: "Blocked",
  ready: "Ready for review",
};

export function StatusBadge({ status }: { status: string }) {
  const normalized = status.toLowerCase();
  return <span className={`status status-${normalized}`}>Status: {labels[normalized] ?? status}</span>;
}
