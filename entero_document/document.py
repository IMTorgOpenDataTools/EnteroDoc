#!/usr/bin/env python3
"""
Document and DocumentFactory class
"""

__author__ = "Jason Beach"
__version__ = "0.1.0"
__license__ = "MIT"

from .config import EnteroConfig
from .record import record_attrs, DocumentAttributeShell
from .extractor import Extractor
from .url import UniformResourceLocator
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
            self.config = EnteroConfig(logger=False)
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
                            applySpacy=self.config.applySpacy
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


class Document:
    """Determine doc type and apply appropriate extractions and transformations.
    
    TODO:I added attrs: {'file_document', 'file_str'}, where should these be organized?
    """
    _spacyNlp = None
    #TODO:add lists of extensions, i.e. `.doc` with `.docx`
    _useable_suffixes = {'.html': Extractor.extract_from_html,
                         '.pdf': Extractor.extract_from_pdf,
                         '.ppt': None,
                         '.docx': None,
                         '.csv': None,
                         '.xlsx': None
                        }
    #TODO:_record_attrs = record_attrs
    _record_attrs = [
            #file indexing
            "id",
            "reference_number",
            "filepath",
            "filename_original",
            "filename_modified",

            #raw
            "file_extension",
            "filetype",
            "file_str",
            "file_document",
            "page_nos",
            "length_lines",
            "file_size_mb",
            "date",

            #inferred / searchable
            "title",
            "author",
            "subject",
            "toc",
            "pp_toc",

            "body",
            "clean_body",
            "readability_score",
            "tag_categories",
            "keywords",
            "summary"
    ]
    #TODO: word_extensions = [".doc", ".odt", ".rtf", ".docx", ".dotm", ".docm"]
    #TODO: ppt_extensions = [".ppt", ".pptx"]
    #TODO: initialize all attributes before running methods

    def __init__(self, path_or_url_format, path_or_url_obj, logger, applySpacy):
        """Args:
                path_or_url_format - 'url', 'path'
                path_or_url_obj - <UniformResourceLocator>, <PosixPath>
                logger - EnteroConfig.logger
                applySpacy - EnteroConfig.applySpacy

        private vars - `self._<name>`
        record vars - `self.record.<name>`
        """
        self._file_format = path_or_url_format
        self._obj = path_or_url_obj
        self._logger = logger
        self._applySpacy = applySpacy
        self.record = DocumentAttributeShell()

        # set file indexing and raw attrs
        if self._file_format=='url':
            url = self._obj
            self.record.filepath = url
            self.record.filename_original = url.get_filename()
            self.record.file_extension = url.get_suffix()
            self.record.filetype = '.'+url.file_format
            self.record.file_str = url.file_str
            self.record.file_document = url.file_document      #TODO:add file_document to filepath as FileImitator, [ref](https://stackoverflow.com/questions/40391487/how-to-create-a-python-object-that-be-passed-to-be-open-as-a-file)
            self.record.file_size_mb = url.file_size_mb

        elif self._file_format=='path':
            path = self._obj
            self.record.filepath = path
            self.record.filename_original = path.stem
            self.record.file_extension = path.suffix
            self.record.file_str = None
            self.record.file_document = None
            self.record.filetype, self.record.file_size_mb = self.determine_file_info()

        self.set_filename_modified()

        # process inferred metadata
        record_extracts = self.run_extraction_pipeline()
        self.update_record_attrs(record_extracts, replace=False)

        # process searchable text
        self._docs = None
        if self.record.body and self._applySpacy:
            self.run_spacy_pipeline(body=self.record.body)
        
        # compare current and template attrs
        missing_attr = self.get_missing_attributes()
        cnt = missing_attr.__len__()
        logger.info(f"Document `{self.record.filename_original}` populated with {cnt} missing (None) attributes: {missing_attr}")

    def _asdict(self):
        """Return dict of recode attributes."""
        result = {}
        for attr in self._record_attrs:
            val = getattr(self, attr)
            result[attr] = val
        return result

    def determine_file_info(self):
        """Determine file system information for the file.

        The format (extension) of the filepath is important 
        to determine what extraction method to use.  Additional
        information is also included.
        """
        path = self.record.filepath
        if not self.record.filetype:
            if path.suffix in list(self._useable_suffixes.keys()):
                filetype = path.suffix
            else:
                filetype = None
        else:
            filetype = self.record.filetype

        if not self.record.file_size_mb:
            size_in_mb = int(path.stat().st_size) * 1e-6
            filesize = round(size_in_mb, ndigits=3)
        else:
            filesize = self.record.file_size_mb
        return filetype, filesize
    
    def set_filename_modified(self):
        """Determine `self.filename_modified` for the new file name."""
        file_extension = '' if self.record.file_extension == None else self.record.file_extension
        if self.record.title:
            self.record.filename_modified = self.record.title + file_extension
        else:
            self.record.filename_modified = self.record.filename_original + file_extension
        return 1
    
    def update_record_attrs(self, record_extracts, replace=True):
        """Update the Document's record attributes.
        Use `replace` to select whether to overwrite current
        attribute values.
        """
        for k,v in record_extracts.items():
            if hasattr(self.record, k):
                if replace==False:
                    current_value = getattr(self.record,k)
                    if not current_value:
                        setattr(self.record, k, v)
                if replace==True:
                    setattr(self.record, k, v)

    def run_extraction_pipeline(self):
        """Apply extractions appropriate for the format.

        Don't throw exception if not an available 
        filetype.  Instead, fail gracefully with result
        of only None values.
        """
        result = {}
        check0 = self.record.filetype in self._useable_suffixes.keys()
        check1 = self._useable_suffixes[self.record.filetype] if check0 else None
        if check1:
            fun_call = self._useable_suffixes[self.record.filetype]
            result = (fun_call)(self.record)
            result['pp_toc'] = self.pretty_print_toc( result['toc'] )
        else:
            self._logger.info("filetype (extension) is not one of the supported suffixes")
            result['pp_toc'] = None
        return result

    def run_spacy_pipeline(self, body):
        """Run nlp pipeline to apply tags.
        
        Get the number of sentences (`length_lines`) for the excerpts made,
        which is based on `utils.MAX_PAGE_EXTRACT`.
        """
        docs = self._spacyNlp.pipe(body)
        docs, gen1 = itertools.tee(docs)
        self._docs = docs
        length_lines = 0
        for doc in gen1:
            length_lines += len(list(doc.sents))
        self.length_lines = length_lines
        return 1

    def get_missing_attributes(self):
        """Count the number of attributes not populated after initialization
        pipelines are run."""
        result = {}
        missing = []
        for attr in self._record_attrs:
            val = getattr(self.record, attr)
            result[attr] = val
            if val == None: 
                missing.append(attr)
        return missing

    def save_modified_file(self, filepath_modified):
        """Copy the original file with the modified name.
        
        This is the only method not automatically performed on initialization
        because it is making modification outside the object.
        """
        filepath_dst = filepath_modified / self.record.filename_modified
        shutil.copy(src=self.record.filepath,
                    dst=filepath_dst
        )
        return 1

    def pretty_print_toc(self, toc, file_or_screen='file'):
        """Print table of contents (toc) in human-readable manner."""
        outlines = toc
        if outlines:
            if file_or_screen == 'screen':
                #TODO:for(level,title,dest,a,se) in outlines:
                for(level,title,dest) in outlines:
                    print( ' '.join(title.split(' ')[1:]) )

            elif file_or_screen=='file':              
                outline_lst = []
                for(level,title,dest) in outlines:
                    item = f'{title}'
                    outline_lst.append(item)
                outline_html_str = ('<br>').join(outline_lst)
                return outline_html_str

            else:
                return 0