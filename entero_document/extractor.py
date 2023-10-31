#!/usr/bin/env python3
"""
Extractor class
"""

__author__ = "Jason Beach"
__version__ = "0.1.0"
__license__ = "MIT"

from .config import ConfigObj
from .extracts_pdf import PdfExtracts
from .extracts_html import HtmlExtracts
#from .office_extracts import OfficeExtracts



class ExtractsSuite:
    """Singleton of all `extracts_*.py` logic.
    :param config: object of type EnteroConfig

    Tightly-coupled to Document attributes through `parent` variable.

    Usage::
        Selected from within Document and applied for use with each file_type
        _useable_suffixes = {'.html': Extractor.extract_from_html,
                             '.pdf': Extractor.extract_from_pdf,
                             '.ppt': None,
                             '.docx': None,
                             '.csv': None,
                             '.xlsx': None
                            }
    """

    def __init__(self, config):
        self.Pdf = PdfExtracts(config)
        self.Html = HtmlExtracts(config)

    def extract_from_pdf(self, record):
        pdf_stream = ''
        with open(record.filepath, 'rb') as f:
            pdf_stream = f.read()
        result_record = self.Pdf.extract_from_pdf_string(pdf_stream)
        return result_record

    def extract_from_html(self, record):
        html_str = ''
        with open(record.filepath, 'r') as f:
            html_str = f.read()
        record_from_context, pdf_bytes = self.Html.html_string_to_pdf(html_str=html_str, 
                                                              url_path=None, 
                                                              record=record
                                                              )
        result_record = self.Pdf.extract_from_pdf_string(pdf_stream=pdf_bytes, 
                                                         record=record_from_context
                                                         )
        return result_record


# export
#config = Config(apply_logger=False)
Extractor = ExtractsSuite(ConfigObj)