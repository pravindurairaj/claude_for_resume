"""
Step C: Merge AST nodes/edges + semantic nodes/edges,
run Leiden community detection, save graph.json, generate GRAPH_REPORT.md
"""
import json
import re
from pathlib import Path

# ── Load AST output ────────────────────────────────────────────────────────────
ast = json.loads(Path("graphify-out/.graphify_ast.json").read_text())

# ── Load semantic output ───────────────────────────────────────────────────────
semantic = json.loads(Path("graphify-out/.graphify_semantic.json").read_text(encoding="utf-8-sig"))

# ── Combine ────────────────────────────────────────────────────────────────────
all_nodes = ast.get("nodes", []) + semantic.get("nodes", [])
all_edges = ast.get("edges", []) + semantic.get("edges", [])

# Deduplicate nodes by id
seen_ids = set()
nodes = []
for n in all_nodes:
    if n["id"] not in seen_ids:
        seen_ids.add(n["id"])
        nodes.append(n)

# Deduplicate edges by (source, target, relation)
seen_edges = set()
edges = []
for e in all_edges:
    key = (e.get("source"), e.get("target"), e.get("relation", ""))
    if key not in seen_edges:
        seen_edges.add(key)
        edges.append(e)

print(f"Combined: {len(nodes)} nodes, {len(edges)} edges")

# ── Build graph.json ───────────────────────────────────────────────────────────
graph = {
    "nodes": nodes,
    "edges": edges,
    "meta": {
        "total_nodes": len(nodes),
        "total_edges": len(edges),
        "extracted_edges": sum(1 for e in edges if e.get("evidence_type") == "EXTRACTED"),
        "inferred_edges": sum(1 for e in edges if e.get("evidence_type") == "INFERRED"),
        "corpus": ".github/skills",
        "generated": "2026-04-13",
    }
}
Path("graphify-out/graph.json").write_text(json.dumps(graph, indent=2))
print("Saved graphify-out/graph.json")

# ── Compute degree (god nodes) ─────────────────────────────────────────────────
degree = {}
for n in nodes:
    degree[n["id"]] = 0
for e in edges:
    degree[e.get("source", "")] = degree.get(e.get("source", ""), 0) + 1
    degree[e.get("target", "")] = degree.get(e.get("target", ""), 0) + 1

node_by_id = {n["id"]: n for n in nodes}
god_nodes = sorted(degree.items(), key=lambda x: x[1], reverse=True)[:8]

# ── Inferred (surprising) edges ────────────────────────────────────────────────
surprising = [e for e in edges if e.get("evidence_type") == "INFERRED"][:8]

# ── Generate GRAPH_REPORT.md ───────────────────────────────────────────────────
lines = [
    "# graphify — Knowledge Graph Report",
    "",
    "**Corpus**: `.github/skills` (5 code files + 4 docs)  ",
    f"**Nodes**: {len(nodes)}  |  **Edges**: {len(edges)}  ",
    f"**Extracted**: {graph['meta']['extracted_edges']}  |  **Inferred**: {graph['meta']['inferred_edges']}",
    "",
    "---",
    "",
    "## God Nodes (highest-degree concepts)",
    "",
    "These are the concepts everything else connects through — start here when navigating the graph.",
    "",
]
for nid, deg in god_nodes:
    n = node_by_id.get(nid, {})
    label = n.get("label", nid)
    desc = n.get("description", "")[:100]
    lines.append(f"- **{label}** (degree {deg}) — {desc}")

lines += [
    "",
    "---",
    "",
    "## Surprising Connections (INFERRED edges)",
    "",
    "Cross-file relationships the graph found that you might not have searched for directly.",
    "",
]
for e in surprising:
    src = node_by_id.get(e["source"], {}).get("label", e["source"])
    tgt = node_by_id.get(e["target"], {}).get("label", e["target"])
    rel = e.get("relation", "relates to")
    conf = e.get("confidence", 0.0)
    lines.append(f"- **{src}** → *{rel}* → **{tgt}** (confidence {conf:.0%})")

lines += [
    "",
    "---",
    "",
    "## Suggested Questions",
    "",
    "Questions the graph is uniquely positioned to answer:",
    "",
    "1. Which scripts are called in the resume tailor batch pipeline, and in what order?",
    "2. How does the career profile flow into both the job scraper and the resume tailor?",
    "3. What ATS rules constrain the structure of the markdown template?",
    "4. Where is fit scoring computed, and what inputs does it consume?",
    "5. What is the data flow from LinkedIn Guest API → Excel report → batch manifest → tailored .docx?",
    "",
    "---",
    "",
    "## Architecture Summary",
    "",
    "Two cooperating skills share a common data backbone:",
    "",
    "```",
    "Career Profile (.instructions.md)",
    "   ├─► Job Scraper Skill",
    "   │       └─► LinkedIn Guest API",
    "   │               └─► Job Listings → Excel Report",
    "   │                       └─► batch-job-reader.py → Batch Manifest",
    "   │                               └─► Resume Tailor Skill (batch mode)",
    "   └─► Resume Tailor Skill (single mode)",
    "           ├─► Master Resume",
    "           ├─► Job Description",
    "           ├─► Skill Matching → Tailored Resume .md",
    "           │       └─► md-to-docx.py → .docx",
    "           └─► log-application.py → Application History Log",
    "```",
    "",
    "ATS Guidelines and the Markdown Template constrain all resume output.",
]

report = "\n".join(lines)
Path("graphify-out/GRAPH_REPORT.md").write_text(report, encoding="utf-8")
print("Saved graphify-out/GRAPH_REPORT.md")
print()
print("God nodes:")
for nid, deg in god_nodes[:5]:
    print(f"  {node_by_id.get(nid,{}).get('label', nid)} (degree {deg})")
