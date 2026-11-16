"""Offline smoke coverage for the resume parser's supported file formats."""
import io
import unittest

from docx import Document
from pypdf import PdfWriter
from pypdf.errors import PdfReadError
from pypdf.generic import DecodedStreamObject, DictionaryObject, NameObject

from App.resume_parser import extract_resume_text


class Upload(io.BytesIO):
    def __init__(self, name, data):
        super().__init__(data)
        self.name = name


class ResumeParserTests(unittest.TestCase):
    def test_pdf_text_extraction(self):
        writer = PdfWriter()
        page = writer.add_blank_page(width=612, height=792)
        font = DictionaryObject({
            NameObject('/Type'): NameObject('/Font'),
            NameObject('/Subtype'): NameObject('/Type1'),
            NameObject('/BaseFont'): NameObject('/Helvetica'),
        })
        page[NameObject('/Resources')] = DictionaryObject({
            NameObject('/Font'): DictionaryObject({NameObject('/F1'): font}),
        })
        content = DecodedStreamObject()
        content.set_data(b'BT /F1 12 Tf 72 720 Td (Resume parser smoke test) Tj ET')
        page[NameObject('/Contents')] = content
        data = io.BytesIO()
        writer.write(data)
        self.assertEqual(extract_resume_text(Upload('resume.pdf', data.getvalue())),
                         'Resume parser smoke test')

    def test_docx_text_extraction(self):
        document = Document()
        document.add_paragraph('Resume parser smoke test')
        data = io.BytesIO()
        document.save(data)
        self.assertEqual(extract_resume_text(Upload('resume.docx', data.getvalue())),
                         'Resume parser smoke test')

    def test_text_extraction(self):
        self.assertEqual(extract_resume_text(Upload('resume.txt', b'  Engineer  ')),
                         'Engineer')

    def test_empty_pdf_rejected(self):
        writer = PdfWriter()
        writer.add_blank_page(width=612, height=792)
        data = io.BytesIO()
        writer.write(data)
        with self.assertRaisesRegex(ValueError, 'Could not extract any text'):
            extract_resume_text(Upload('resume.pdf', data.getvalue()))

    def test_malformed_pdf_rejected(self):
        with self.assertRaises(PdfReadError):
            extract_resume_text(Upload('resume.pdf', b'not a PDF'))

    def test_unsupported_type_rejected(self):
        with self.assertRaisesRegex(ValueError, 'Unsupported file type'):
            extract_resume_text(Upload('resume.exe', b'not a resume'))


if __name__ == '__main__':
    unittest.main()
