import type { ReactNode } from "react";
import { EvidenceReference } from "./EvidenceReference";

export function Shell({ children, project, source }: { children: ReactNode; project: string; source: string }) {
  return <><a className="skip-link" href="#main-content">Skip to review content</a><header className="site-header"><span className="brand">Epistemic alignment</span><p>{project}</p><EvidenceReference source={source} /></header>{children}<footer className="site-footer">Derived presentation — canonical evidence remains in the dossier.</footer></>;
}
