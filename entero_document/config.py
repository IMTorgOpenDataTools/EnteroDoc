#!/usr/bin/env python3
"""
Constants used for configuration
"""

__author__ = "Jason Beach"
__version__ = "0.1.0"
__license__ = "MIT"


from .utils import dotdict
from .record import DocumentRecord

import logzero
from logzero import logger

from pathlib import Path
import json



class EnteroConfig:
    """Config for both Document and UniformResourceLocator classes.
    
    """

    def __init__(self, apply_logger=True):

        #constants
        self.MAX_PAGE_EXTRACT = None
        self.MAX_CONTENT_SIZE = 1e+8         #in bytes => 100MB
        self.ALLOWED_EXTENSIONS = {'.zip'}

        #output
        self.output_mapping_template_path = None
        self.output_mapping = None
        
        # dependencies
        self.applyRequestsRenderJs = False
        self.applySpacy = False
        self.applyPyMuPDF = True
        self.applyOCRmyPDF = False

        # logging
        if apply_logger:
            self.logging_dir = Path() / 'logs' / 'process.log'
            self.logger = logger
            logzero.loglevel(logzero.INFO)                                           #set a minimum log level: debug, info, warning, error
            logzero.logfile(self.logging_dir, maxBytes=1000000, backupCount=3)       #set rotating log file
            self.logger.info('logger created, constants initialized')
        else:
            self.logger = dotdict( {'info': print, 'error': print} )

        # provisioning logic
        self.get_output_mapping_template()


    def get_output_mapping_template(self):
        """TODO"""
        if self.output_mapping_template_path:
            template = Path(self.output_mapping_template_path)
            mapping = ''
            try:
                with open(template, 'r') as f:
                    mapping = json.load(f)
                docrec = DocumentRecord()
                result = docrec.validate_object_attrs(mapping)
                check_mapping = result['target_attrs_to_remove']==[] and result['target_attrs_to_add']==[]
            except:
                self.logger.error(f'There was a problem loading the json file.')
                return False
            else:
                if check_mapping:
                    self.output_mapping = mapping
                    return True
                else:
                    return False