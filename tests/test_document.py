#!/usr/bin/env python3
"""
Tests for Document class
"""

__author__ = "Jason Beach"
__version__ = "0.1.0"
__license__ = "MIT"

from entero_document.document import DocumentFactory, Document
from entero_document.record import DocumentRecord

from pathlib import Path
import pytest

Doc = DocumentFactory()


def test_document_attributes():
    test_file = Path('tests/examples/example.pdf')
    doc = Doc.build(test_file)
    docrec = DocumentRecord()
    result = docrec.validate_object_attrs(doc)
    assert list(result) == ['target_attrs_to_remove', 'target_attrs_to_add']

def test_document_populated():
    test_file = Path('tests/demo/econ_2301.00410.pdf')
    doc = Doc.build(test_file)
    docrec = DocumentRecord()
    result = docrec.validate_object_attrs(doc)
    check1 = len(result['target_attrs_to_remove']) == 0
    check2 = not bool(result['target_attrs_to_add'])
    check3 = doc.get_missing_attributes() == ['id', 'reference_number', 'file_str', 'file_document', 'length_lines', 'readability_score', 'tag_categories', 'summary']
    assert not False in [check1, check2, check3]

def test_document_creation_fail():
    test_file = Path('tests/examples/no_file.docx')
    '''previous flow:
    with pytest.raises(Exception) as e_info:
        doc = Doc.build(test_file)
    assert type(e_info) == pytest.ExceptionInfo
    '''
    doc = Doc.build(test_file)
    assert doc == None

def test_document_determine_filetype_fail():
    """Filetypes that fail: .doc, .rtf, .tif, .docm, .dot
    This tests that file exists, but is not supported by 
    method `Document.run_extraction_pipeline()`.  So, attr
    are None, and not empty string ''.
    """
    test_file = Path('tests/examples/unavailable_extension.doc')
    doc = Doc.build(test_file)
    assert doc.record.file_document == None

def test_document_extraction():
    """TODO: create separate tests using pytest."""
    #TODO:currently these fail to capture actual title
    lst = { '.docx': ['tests/examples/example.docx', 'Document Title'],
            '.html': ['tests/examples/example.html', 'The Website Title'],
            '.pdf': ['tests/examples/example.pdf', 'The Website Title'],
            '.csv': ['tests/examples/example.csv', 'Document Title'],
            '.xlsx': ['tests/examples/example.xlsx', 'Document Title'],
            }
    checks = []
    for k,v in lst.items():
        filepath = v[0]
        title = v[1]
        test_file = Path(filepath)
        doc = Doc.build(test_file)
        check = hasattr(doc.record, 'title') == True
        checks.append(check)
    assert all(checks) == True