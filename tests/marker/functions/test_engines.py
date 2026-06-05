from docx import Document as DocxDocument

from marker.functions.engines import PythonDocxFacade


class TestPythonDocxFacade:
    def test_writes_heading_to_docx(self, tmp_path) -> None:
        facade = PythonDocxFacade()
        facade.add_heading("Introduction", level=1)
        output = tmp_path / "test.docx"
        facade.save(str(output))

        doc = DocxDocument(str(output))
        texts = [p.text for p in doc.paragraphs if p.text]
        assert "Introduction" in texts

    def test_writes_table_to_docx(self, tmp_path) -> None:
        facade = PythonDocxFacade()
        facade.add_table(rows=2, cols=3)
        output = tmp_path / "test.docx"
        facade.save(str(output))

        doc = DocxDocument(str(output))
        assert len(doc.tables) == 1
        assert len(doc.tables[0].rows) == 2
        assert len(doc.tables[0].columns) == 3

    def test_writes_heading_and_table(self, tmp_path) -> None:
        facade = PythonDocxFacade()
        facade.add_heading("Site Investigation Report", level=1)
        facade.add_table(rows=4, cols=2)
        output = tmp_path / "combined.docx"
        facade.save(str(output))

        doc = DocxDocument(str(output))
        texts = [p.text for p in doc.paragraphs if p.text]
        assert "Site Investigation Report" in texts
        assert len(doc.tables) == 1
