#!/usr/bin/env python3
"""
Tests for Document class
"""

__author__ = "Jason Beach"
__version__ = "0.1.0"
__license__ = "MIT"


from entero_document.config import EnteroConfig
from entero_document.record import DocumentRecord
from entero_document.document_factory import DocumentFactory

from pathlib import Path
import pytest


def test_output_mapping():
    test_file = Path('tests/examples/example.pdf')
    config = EnteroConfig()
    config.output_mapping_template_path = Path('tests/data/mapping_template.json')
    config.get_output_mapping_template()

    Doc = DocumentFactory(config)
    doc = Doc.build(test_file)
    output_mapped = doc.get_record(map_output=True)

    docrec = DocumentRecord()
    result = docrec.validate_object_attrs(output_mapped)
    assert result['target_attrs_to_remove'] == result['target_attrs_to_add'] == set()