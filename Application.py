# -*- coding: utf-8 -*-
"""
Created on Tue Sep 27 23:24:58 2016

@author: shang
"""

def RatingCalculator(csv_data, csv_rating, csv_combination):
    """ This function runs the model with a new set of test data, then update
        the csv file 
    """
    import pandas
    
    # game instances
    data = pandas.read_csv(filepath_or_buffer=csv_data, index_col=0)
    matrixData = pandas.DataFrame.as_matrix(data)  
    (num_games, dontcare) = matrixData.shape
    print(matrixData.shape)    
    
    # lookup table
    lookup_table = {}
    (row, col) = matrixData.shape
    num_players = 0
    for x in range (0, row):
        for y in range(0, col-2):
            if matrixData[x,y] not in lookup_table:
                lookup_table[matrixData[x,y]] = num_players
                num_players += 1           
    print(lookup_table)  

    # rating combination per game
    combination = pandas.read_csv(csv_combination, header=None)
    matrixCombination = pandas.DataFrame.as_matrix(combination)
    print(matrixCombination)
    
    # loop through all game instances
    for g in range (0, num_games):
        # For each, loop through all combination, 
        # and find all possible combination
        # use lookup table to append to possible rating combinations
        score_diff = matrixData[g][-2] - matrixData[g][-1]  # team A - team B
        
    
    
                    
    return