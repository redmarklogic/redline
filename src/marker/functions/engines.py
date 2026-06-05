from pathlib import Path

from docx import Document as DocxDocument


class PythonDocxFacade:
    def __init__(self, template: Path | None = None) -> None:
        if template is not None:
            self._doc = DocxDocument(str(template))
        else:
            self._doc = DocxDocument()

    def add_heading(self, text: str, level: int) -> None:
        self._doc.add_heading(text, level=level)

    def add_table(self, rows: int, cols: int) -> None:
        self._doc.add_table(rows=rows, cols=cols)

    def save(self, path: str) -> None:
        self._doc.save(path)
