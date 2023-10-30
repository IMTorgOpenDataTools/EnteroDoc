#!/usr/bin/env python3
"""
Constants used for configuration
"""

__author__ = "Jason Beach"
__version__ = "0.1.0"
__license__ = "MIT"


from .utils import dotdict

import logzero
from logzero import logger

from pathlib import Path




class EnteroConfig:
    """Config for both Document and UniformResourceLocator classes.
    
    """

    def __init__(self, logger=True):

        #constants
        self.MAX_PAGE_EXTRACT = None
        self.MAX_CONTENT_SIZE = 1e+8         #in bytes => 100MB
        self.ALLOWED_EXTENSIONS = {'.zip'}

        # dependencies
        self.applyRequestsRenderJs = False
        self.applySpacy = False
        self.applyPyMuPDF = True
        self.applyOCRmyPDF = False

        # logging
        if logger:
            self.logging_dir = Path() / 'logs' / 'process.log'
            self.logger = logger
            logzero.loglevel(logzero.INFO)                                           #set a minimum log level: debug, info, warning, error
            logzero.logfile(self.logging_dir, maxBytes=1000000, backupCount=3)       #set rotating log file
            self.logger.info('logger created, constants initialized')
        else:
            self.logger = dotdict( {'info': print, 'error': print} )