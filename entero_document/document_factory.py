#!/usr/bin/env python3
"""
DocumentFactory class
"""

__author__ = "Jason Beach"
__version__ = "0.1.0"
__license__ = "MIT"

from .config import EnteroConfig
from .record import record_attrs, DocumentAttributeShell
from .url import UniformResourceLocator
from .extractor import Extractor
from .document import Document

#from . import ARCHIVE_extractions as ex

from pathlib import Path, PosixPath
import shutil
import itertools


#config = EnteroConfig(logger=False)



class DocumentFactory:

    def __init__(self, config=None):
        if config:
            self.config = config
        else:
            self.config = EnteroConfig(apply_logger=False)
        if self.config.applySpacy:
            import spacy
            nlp = spacy.load("en_core_web_sm")
            Document._spacyNlp = nlp
        
    def build(self, path_or_url):
        """Create Document object with path or url."""
        validation_dict = self._validate(path_or_url=path_or_url)
        if validation_dict:
            return Document(path_or_url_format=validation_dict[0],
                            path_or_url_obj=validation_dict[1],
                            logger=self.config.logger,
                            applySpacy=self.config.applySpacy,
                            output_mapping=self.config.output_mapping
                            )
        else:
            return None

    def _validate(self, *args, **kwargs):
        """Validate input or fail object creation and return None."""
        try:
            assert not args
            assert list(kwargs.keys()) == ['path_or_url']
        except AssertionError:
            return False
        path_or_url = kwargs['path_or_url']
        cond0 = type(path_or_url) == UniformResourceLocator
        cond1 = type(path_or_url) == PosixPath
        if cond0:
            if path_or_url.file_document:
                url = path_or_url
                return ('url', url)
            else:
                self.config.logger.error(f"Error: no artifact associated with {path_or_url} ")
                #raise TypeError
                return False
        elif cond1:
            if path_or_url.is_file():
                path = path_or_url
                return ('path', path)
            else:
                self.config.logger.info(f"arg `path` {path_or_url} must be a file")
                #raise TypeError
                return False
        else:
            self.config.logger.info(f"TypeError: arg `path` {path_or_url} must be of type {Path} or {UniformResourceLocator}")
            #raise TypeError
            return False