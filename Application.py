# -*- coding: utf-8 -*-
"""
Created on Mon Sep 12 13:32:58 2016

@author: Vivien Y. Fan
"""
import pandas
import numpy

def RatingCalculator(csv_data, csv_rating):
    """ This function runs the model with a new set of test data, then update
        the csv file 
    """
                
    # To-do: run the model with newGame instance
    data = pandas.read_csv(filepath_or_buffer=csv_data, index_col=0)
    matrixData = pandas.DataFrame.as_matrix(data)
    dic = pandas.Series.from_csv(csv_rating).to_dict()  
    dic = {}
    dic_temp = {}
    dic_copy = {}  
    min_error = [10000000000, dic]
    
    (row, col) = matrixData.shape
    
    # first, assign all the new players with an initial rating 5
    for x in range (0, row):
        for y in range(0, col-2):
            if matrixData[x,y] not in dic:
                dic[matrixData[x,y]] = 5        
                dic_temp[matrixData[x,y]] = []
                
                
    # now calculate the score error
    total_error = 0
    for x in range (0, row):
        sumA = 0
        sumB = 0
        for k in range (0, 6):
            sumA += dic[matrixData[x, k]]
            sumB += dic[matrixData[x, k+6]]
        avgA = sumA / 6
        avgB = sumB / 6
        score_diff = abs(matrixData[x, -1] - matrixData[x, -2])
        score_diff_calc = int(abs(avgA - avgB) * 2)
        error = abs(score_diff - score_diff_calc)            
        total_error += error          

    error_per_game = total_error / row
    CreateRecord(error_per_game, dic.copy())        
        
        

    # loop until ratings stop updating
    keep_running = True
    while keep_running:
        dic_copy = dic.copy()   # a shallow copy of the data
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
            x_adjustment = (((scoreA - scoreB) / 2 - (avgA - avgB))) * 7 
            for k in range (0, 6):
                # team a: avgA' = avgA + x
                dic_temp[matrixData[x, k]].append(dic[matrixData[x, k]] + x_adjustment)
                # team b: avgB' = avgB - x
                dic_temp[matrixData[x, k+6]].append(dic[matrixData[x, k+6]] - x_adjustment)

        # update the rating with the average
        for key in dic:
            dic[key] = int(numpy.mean(dic_temp[key]))   
    
        # now calculate the score error
        total_error = 0
        for x in range (0, row):
            sumA = 0
            sumB = 0
            for k in range (0, 6):
                sumA += dic[matrixData[x, k]]
                sumB += dic[matrixData[x, k+6]]
            avgA = sumA / 6
            avgB = sumB / 6
            score_diff = abs(matrixData[x, -1] - matrixData[x, -2])
            score_diff_calc = int(abs(avgA - avgB) * 2)
            error = abs(score_diff - score_diff_calc)            
            total_error += error          
    
        error_per_game = total_error / row
        CreateRecord(error_per_game, dic.copy())        
        
        if error_per_game <= min_error[0]:
            min_error[0] = error_per_game
            min_error[1] = dic.copy() # need to be a shallow copy, otherwise it will be changed in next iteration
    
        # check if the ratings stop updating
        still_updating = False
        for key in dic:
            if dic[key] != dic_copy[key]:
                still_updating = True;
        if still_updating == False:
            keep_running = False;
               
    player_ratings = pandas.Series(min_error[1])
    player_ratings.to_csv(csv_rating)
    return
    
    
def CreateRecord(error, dic_player_ratings):
    new_list = [[None] * (len(dic_player_ratings) + 1)]
    new_list[0][0] = error
    i = 1
    for key in dic_player_ratings:
        new_list[0][i] = key + ":" + str(dic_player_ratings[key])
        i += 1

    new_row = pandas.DataFrame(new_list)   
    new_row.to_csv(r'C:\Users\shang\Documents\GitHub\MachineLearning---TeamChooser\Records.csv', mode='a', index=False, header=False)
    return
    