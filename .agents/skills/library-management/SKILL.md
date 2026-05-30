---
name: library-management
description: Use when indexing, renaming, or adding books to the digital library at <library-root> -- covers scanning folders, extracting metadata from PDFs, using the SNZ scraper for NZ/AU standard metadata (title, status, canonical code), updating the Excel index, and renaming files to the canonical convention.
---

# Library Management

Operations for the digital library: scanning, metadata extraction, indexing, and renaming files to the canonical convention.

## Boundary Contract

**Applies To:** Physical digital library at \<library-root>\ -- PDF/EPUB files, the Excel index, and SNZ/AS metadata scraping | **Produces:** Updated index rows, canonically renamed files, dedup notes | **Does Not Cover:** NotebookLM notebook management (otebooklm-index\), geotechnical domain judgments (route to Graeme), content decisions <!-- hook: allow -->

## Quick Reference

| Operation | Tool / Command |
|---|---|
| Extract metadata from a PDF | \metadata_extractor.py\ -- never throwaway scripts |
| Scrape NZ/AU standard metadata | \get_snz_metadata()\ -- filename is never the canonical title |
| Write to the index workbook | \workbook_utils.py\ imports under \WorkbookLock\ |
| Verify after a batch run | \erify_index.py\ -- report file count, NEEDS_REVIEW, duplicates |
| Handle duplicates | Add \DUPLICATE of <path>\ in notes; never silently skip |

See \procedures/library-management.md\ for full workflow: batch phases, dedup pass, chapter merging, EPUB conversion, SNZ scraping details, and extended anti-patterns.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Using filename as \	itle\ for NZ/AU standards | Call \get_snz_metadata\ first; filename is never the canonical title |
| Not saving after each workbook mutation | Save atomically before moving to the next file |
| Running multiple workbook writers simultaneously | All writers must acquire \WorkbookLock\; confirm no active writer before removing a lock |
| Deleting duplicate files without user instruction | Flag in otes\ -- the user decides |
| Invoking a persona agent (Knowledge Operator, Domain Expert) for execution | Persona agents are advisory; apply their skills directly and execute in the main agent |
