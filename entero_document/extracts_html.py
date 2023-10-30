#!/usr/bin/env python3
"""
Extraction functions for each file type to be used with Document class

"""

__author__ = "Jason Beach"
__version__ = "0.1.0"
__license__ = "MIT"


from entero_document.record import record_attrs, DocumentAttributeShell

#html
import bs4
from xhtml2pdf import pisa 

import io
import time


class HtmlExtracts:
    """Singleton of extract logic for pdf format.
    
    TODO:check html_str is bs4 compliant
    TODO:check with url_path
    """

    def __init__(self, config):
        self.config = config


    def html_string_to_pdf(self, html_str, url_path=None, record=DocumentAttributeShell()):
        """Generate a pdf:str and associated record metadata (title, toc, ...) 
        from html string content.
        """
        time0 = time.time()

        context = {}
        result = io.BytesIO()
        if len(record.keys())==0:
            for key in record_attrs:
                record[key] = None
        meta_attrs = ["title", "author", "subject", "keywords"]

        try:
            html = io.StringIO(html_str) 
            context = pisa.pisaDocument(src=html,
                                     dest=result,
                                     path=url_path)
        except:
            print("Error: unable to create the PDF")

        if context:
            for key in meta_attrs:
                record[key] = context.meta[key]
        pdf_bytes = result.getvalue()

        time1 = time.time()
        self.config.logger.info(f'Convert html to pdf took: {time1 - time0} secs')

        return record, pdf_bytes