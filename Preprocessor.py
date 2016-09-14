# -*- coding: utf-8 -*-
"""
Created on Mon Sep 12 13:32:58 2016

@author: Vivien Y. Fan
"""


def RawDataProcessor(csvFile):
    """ Extract and processe raw data from a given csv file.
    
        Arg:
            csvFile: the path to a csv file
        Returns:
            extracted data in a metrix form
        Raises:
            OSError: file does not exist            
    """
    import pandas
    return pandas.read_csv(csvFile)
