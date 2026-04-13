# graphify — Knowledge Graph Report

**Corpus**: `.github/skills` (5 code files + 4 docs)  
**Nodes**: 101  |  **Edges**: 154  
**Extracted**: 40  |  **Inferred**: 11

---

## God Nodes (highest-degree concepts)

These are the concepts everything else connects through — start here when navigating the graph.

- **batch-job-reader.py** (degree 18) — 
- **scrape-linkedin-jobs.py** (degree 13) — 
- **md-to-docx.py** (degree 11) — 
- **main()** (degree 10) — 
- **Resume Markdown Template** (degree 10) — Canonical Markdown scaffold defining section order and placeholder syntax for generating ATS-friendl
- **log-application.py** (degree 8) — 
- **main()** (degree 5) — 
- **resolve_output_names()** (degree 5) — 

---

## Surprising Connections (INFERRED edges)

Cross-file relationships the graph found that you might not have searched for directly.

- **Resume Markdown Template** → *structures output of* → **Tailored Resume (Markdown)** (confidence 95%)
- **ATS Guidelines** → *constrains formatting in* → **Resume Tailor Skill** (confidence 95%)
- **ATS Formatting Rules** → *governs structure of* → **Resume Markdown Template** (confidence 90%)
- **Keyword Matching Strategy** → *is implemented by* → **Skill Matching Process** (confidence 85%)
- **ATS Section Order** → *defines section sequence of* → **Resume Markdown Template** (confidence 90%)
- **Bullet Point Formula** → *incorporates* → **Quantification Rule** (confidence 85%)
- **Excel Job Report** → *feeds job listings into* → **Batch Mode** (confidence 90%)
- **Career Profile** → *provides contact details to* → **Resume Tailor Skill** (confidence 88%)

---

## Suggested Questions

Questions the graph is uniquely positioned to answer:

1. Which scripts are called in the resume tailor batch pipeline, and in what order?
2. How does the career profile flow into both the job scraper and the resume tailor?
3. What ATS rules constrain the structure of the markdown template?
4. Where is fit scoring computed, and what inputs does it consume?
5. What is the data flow from LinkedIn Guest API → Excel report → batch manifest → tailored .docx?

---

## Architecture Summary

Two cooperating skills share a common data backbone:

```
Career Profile (.instructions.md)
   ├─► Job Scraper Skill
   │       └─► LinkedIn Guest API
   │               └─► Job Listings → Excel Report
   │                       └─► batch-job-reader.py → Batch Manifest
   │                               └─► Resume Tailor Skill (batch mode)
   └─► Resume Tailor Skill (single mode)
           ├─► Master Resume
           ├─► Job Description
           ├─► Skill Matching → Tailored Resume .md
           │       └─► md-to-docx.py → .docx
           └─► log-application.py → Application History Log
```

ATS Guidelines and the Markdown Template constrain all resume output.