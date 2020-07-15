# -*- coding: utf-8 -*-
"""
Created on Sat Jul  4 04:58:39 2020
Prototype of market and inventory downloader
@author: shaolun du
@contact: shaolun.du@gmail.com
"""
from abc import ABC, abstractmethod
class exc_parser(ABC):
    @abstractmethod
    def _download(self, *args, **kwargs): 
        # Download market information from exchange
        pass
    @abstractmethod
    def _get_data_df(self, *args, **kwargs): 
        # Return dataframe
        pass
    @abstractmethod
    def _get_URL_TEMP(self, *args, **kwargs): 
        # Return url template
        pass
    @abstractmethod
    def _read_html_format(self, *args, **kwargs):
        # Return data frame after read html
        pass
