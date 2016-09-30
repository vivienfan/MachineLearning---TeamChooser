# -*- coding: utf-8 -*-
"""
Created on Mon Sep 12 13:32:58 2016

@author: Vivien Y. Fan
"""


def RatingCalculator(csv_data, csv_rating):
    """ This function runs the model with a new set of test data, then update
        the csv file 
    """
    import pandas
    import numpy
                
    # To-do: run the model with newGame instance
    data = pandas.read_csv(filepath_or_buffer=csv_data, index_col=0)
    matrixData = pandas.DataFrame.as_matrix(data)
#    dic = pandas.Series.from_csv(csv_rating).to_dict()  
    dic = {}
    dic_temp = {}
    dic_copy = {}  
    
    (row, col) = matrixData.shape
    
    # first, assign all the new players with an initial rating 5
    for x in range (0, row):
        for y in range(0, col-2):
            if matrixData[x,y] not in dic:
                dic[matrixData[x,y]] = 8        # if set to 5, all numbers are off by 3, a bias in the given ratings
                dic_temp[matrixData[x,y]] = []

    i = 0
    # loop until ratings stop updating
    keep_running = True
    while keep_running:
        dic_copy = dic.copy()
        # loop through all instances tofind a posible rating for every player in each game
        for x in range (0, row):
            sumA = 0
            sumB = 0     
            for k in range (0, 6):
                sumA += dic[matrixData[x, k]]
                sumB += dic[matrixData[x, k+6]]
                
            avgA = sumA / 6
            avgB = sumB / 6   
            scoreA = matrixData[x, -2]
            scoreB = matrixData[x, -1]      
            x_adjustment = (((scoreA - scoreB) / 2 - (avgA - avgB))) * 2 * 11 
            for k in range (0, 6):
                # team a: avgA' = avgA + x
                dic_temp[matrixData[x, k]].append(dic[matrixData[x, k]] + x_adjustment)
                # team b: avgB' = avgB - x
                dic_temp[matrixData[x, k+6]].append(dic[matrixData[x, k+6]] - x_adjustment)

        # update the rating with the average
        for key in dic:
            dic[key] = int(numpy.mean(dic_temp[key]))
    
        # check if the ratings stop updating
        still_updating = False
        for key in dic:
            if dic[key] != dic_copy[key]:
                still_updating = True;
        if still_updating == False:
            keep_running = False;
        
    print(i)        
    player_ratings = pandas.Series(dic)
    player_ratings.to_csv(csv_rating)
    return
    