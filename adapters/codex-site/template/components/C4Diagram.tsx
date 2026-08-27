"use client";

import { useEffect, useId, useState } from "react";

export function C4Diagram({ source }: { source: string }) {
  const id = useId().replace(/:/g, "-");
  const [svg, setSvg] = useState<string | null>(null);
  const [error, setError] = useState(false);

  useEffect(() => {
    let active = true;
    void import("mermaid").then(async ({ default: mermaid }) => {
      mermaid.initialize({ startOnLoad: false, securityLevel: "strict", theme: "base" });
      const rendered = await mermaid.render(`c4-${id}`, source);
      if (active) setSvg(rendered.svg);
    }).catch(() => { if (active) setError(true); });
    return () => { active = false; };
  }, [id, source]);

  return <figure className="diagram" aria-labelledby={`${id}-caption`}><figcaption id={`${id}-caption`}>C4 diagram</figcaption>{svg && !error ? <div aria-hidden="true" dangerouslySetInnerHTML={{ __html: svg }} /> : <p role="status">Diagram rendering is unavailable; use the textual fallback below.</p>}<details open><summary>C4 textual fallback</summary><pre>{source}</pre></details></figure>;
}
