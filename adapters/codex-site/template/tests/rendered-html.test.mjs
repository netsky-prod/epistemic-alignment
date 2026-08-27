import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import test from "node:test";

async function render() {
  const workerUrl = new URL("../dist/server/index.js", import.meta.url);
  workerUrl.searchParams.set("test", `${process.pid}-${Date.now()}`);
  const { default: worker } = await import(workerUrl.href);

  return worker.fetch(
    new Request("http://localhost/", { headers: { accept: "text/html" } }),
    { ASSETS: { fetch: async () => new Response("Not found", { status: 404 }) } },
    { waitUntil() {}, passThroughOnException() {} },
  );
}

test("renders all seven dossier sections and exposes epistemic state labels", async () => {
  const response = await render();
  assert.equal(response.status, 200);
  const html = await response.text();
  const text = html.replace(/<!--.*?-->/g, "");

  for (const id of [
    "summary",
    "stakeholders",
    "use-cases",
    "behavior",
    "architecture",
    "decisions-and-risks",
    "review-readiness",
  ]) {
    assert.match(html, new RegExp(`id="${id}"`));
  }

  assert.match(text, /Status: Proposed/);
  assert.match(text, /Status: Uncertain/);
  assert.match(text, /Status: Conflicting/);
});

test("keeps findings before readiness and provides a C4 text fallback", async () => {
  const response = await render();
  const html = await response.text();

  const findingsIndex = html.indexOf("Review findings");
  const readinessIndex = html.indexOf("Snapshot readiness");
  assert.ok(findingsIndex >= 0 && findingsIndex < readinessIndex);
  assert.match(html, /C4 textual fallback/);
  assert.match(html, /Snapshot hash/);
  assert.doesNotMatch(html, /Approve dossier|Record approval/);
});

test("renders dossier sources as resolvable internal evidence links", async () => {
  const response = await render();
  const html = await response.text();
  const text = html.replace(/<!--.*?-->/g, "");

  assert.match(text, /Evidence:.*charter\.md#goals/);
  assert.match(text, /Evidence:.*review\.md#F-01/);
  const evidenceHrefs = [...html.matchAll(/class="evidence-reference"[^>]*href="#([^"]+)"/g)]
    .map((match) => match[1]);
  assert.ok(evidenceHrefs.length > 0, "expected clickable evidence references");
  const evidenceTargetIds = [...html.matchAll(/<li id="(evidence-source-[^"]+)"/g)]
    .map((match) => match[1]);
  assert.equal(new Set(evidenceTargetIds).size, evidenceTargetIds.length);
  assert.equal(new Set(evidenceHrefs).size, evidenceTargetIds.length);
  for (const href of evidenceHrefs) {
    assert.match(html, new RegExp(`id="${href}"`), `missing target for #${href}`);
  }
  for (const [, href] of html.matchAll(/href="#([^"]+)"/g)) {
    assert.match(html, new RegExp(`id="${href}"`), `missing internal target for #${href}`);
  }
  assert.doesNotMatch(html, /href="[^"]*(?:alignment\/|\.md|\.feature)/);
});

test("uses deterministic C4 caption and Mermaid render identifiers", async () => {
  const [response, component] = await Promise.all([
    render(),
    readFile(new URL("../components/C4Diagram.tsx", import.meta.url), "utf8"),
  ]);
  const html = await response.text();

  assert.match(html, /aria-labelledby="c4-diagram-caption"/);
  assert.match(html, /figcaption id="c4-diagram-caption"/);
  assert.match(component, /const id = "c4-diagram"/);
  assert.match(component, /mermaid\.render\(id, source\)/);
  assert.doesNotMatch(component, /\buseId\b/);
});
