import os

from great_tables import GT


def print_gt(gt_tbl: GT) -> None:
    """Render a GT table for both HTML and PDF/Typst Quarto outputs.

    Use with ``#| output: asis`` on the enclosing code cell so Quarto
    treats the output as raw markup rather than wrapping it in a code block.
    """
    _qfmt = os.environ.get("QUARTO_DOCUMENT_FORMAT", "html")
    if _qfmt in ("pdf", "typst", "latex", "beamer"):
        print(gt_tbl.as_latex())
    else:
        print(gt_tbl.as_raw_html())
