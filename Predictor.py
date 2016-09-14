# -*- coding: utf-8 -*-
"""
Created on Mon Sep 12 13:32:58 2016

@author: Vivien Y. Fan
"""


def PredictingFunction(model, games, newGame, csvFile):
    """ This function runs the model with a new set of test data, then update
        the csv file 
    """
    import pandas
    # To-do: run the model with newGame instance
    updatedData = pandas.DataFrame(games)
    updatedData.to_csv(csvFile)    
    print ("---------- Testing ----------")
    return
    