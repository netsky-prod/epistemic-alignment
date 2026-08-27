import type { ReactNode } from "react";

export function Shell({ children, project, source }: { children: ReactNode; project: string; source: string }) {
  return <><a className="skip-link" href="#main-content">Skip to review content</a><header className="site-header"><a href={source} className="brand">Epistemic alignment</a><p>{project}</p></header>{children}<footer className="site-footer">Derived presentation — canonical evidence remains in the linked dossier.</footer></>;
}
