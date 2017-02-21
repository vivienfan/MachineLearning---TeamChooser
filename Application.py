# -*- coding: utf-8 -*-
"""
Created on Mon Sep 12 13:32:58 2016

@author: Vivien Y. Fan
"""
import pandas
#import numpy

#def RatingCalculator(csv_data, csv_rating):
#    """ This function runs the model with a new set of test data, then update
#        the csv file 
#    """              
#    # To-do: run the model with newGame instance
#    data = pandas.read_csv(filepath_or_buffer=csv_data, index_col=0)
#    matrixData = pandas.DataFrame.as_matrix(data)
#    dic = pandas.Series.from_csv(csv_rating).to_dict()  
#    dic = {}
#    dic_temp = {}
#    dic_copy = {}  
#    min_error = [10000000000, dic]    
#    (row, col) = matrixData.shape
#    
#    # first, assign all the new players with an initial rating 5
#    for x in range (0, row):
#        for y in range(0, col-2):
#            if matrixData[x,y] not in dic:
#                dic[matrixData[x,y]] = 5        
#                dic_temp[matrixData[x,y]] = [0,0]              
#                
#    # now calculate the score error
#    total_error = 0
#    for x in range (0, row):
#        sumA = 0
#        sumB = 0
#        for k in range (0, 6):
#            sumA += dic[matrixData[x, k]]
#            sumB += dic[matrixData[x, k+6]]
#        avgA = sumA / 6
#        avgB = sumB / 6
#        score_diff = abs(matrixData[x, -1] - matrixData[x, -2])
#        score_diff_calc = int(abs(avgA - avgB) * 2)
#        error = abs(score_diff - score_diff_calc)            
#        total_error += error          
#    error_per_game = total_error / row
#    CreateRecord(error_per_game, dic.copy())        
#
#    # loop until ratings stop updating
#    keep_running = True
#    while keep_running:
#        dic_copy = dic.copy()   # a shallow copy of the data
#        # loop through all instances tofind a posible rating for every player in each game
#        for x in range (0, row):
#            teamA = list()
#            teamB = list()
#            for k in range (0, 6):
#                teamA.append(dic[matrixData[x, k]])
#                teamB.append(dic[matrixData[x, k+6]]) 
#            scoreA = matrixData[x, -2]
#            scoreB = matrixData[x, -1]
#            adjustment = CalculateAdjustment(teamA, teamB, (scoreA-scoreB))            
#            
#            for k in range (0, 6):
#                # team a: avgA' = avgA + x
#                dic_temp[matrixData[x, k]][0] += dic[matrixData[x, k]] + adjustment
#                dic_temp[matrixData[x, k]][1] += 1
#                # team b: avgB' = avgB - x
#                dic_temp[matrixData[x, k+6]][0] += dic[matrixData[x, k+6]] - adjustment
#                dic_temp[matrixData[x, k+6]][1] += 1
#
#        # update the rating with the average
#        for key in dic:
#            dic[key] = int(dic_temp[key][0] / dic_temp[key][1])   
#    
#        # now calculate the score error
#        total_error = 0
#        for x in range (0, row):
#            sumA = 0
#            sumB = 0
#            for k in range (0, 6):
#                sumA += dic[matrixData[x, k]]
#                sumB += dic[matrixData[x, k+6]]
#            avgA = sumA / 6
#            avgB = sumB / 6
#            score_diff = abs(matrixData[x, -1] - matrixData[x, -2])
#            score_diff_calc = int(round(abs(avgA - avgB) * 2))
#            error = abs(score_diff - score_diff_calc)            
#            total_error += error                  
#        error_per_game = total_error / row
#        CreateRecord(error_per_game, dic.copy())        
#        
#        if error_per_game <= min_error[0]:
#            min_error[0] = error_per_game
#            min_error[1] = dic.copy() # need to be a shallow copy, otherwise it will be changed in next iteration
#    
#        # check if the ratings stop updating
#        still_updating = False
#        for key in dic:
#            if dic[key] != dic_copy[key]:
#                still_updating = True;
#        if still_updating == False:
#            keep_running = False;
#        
#        if min_error[0] == 0:
#            keep_running = False;
#               
#    player_ratings = pandas.Series(min_error[1])
#    player_ratings.to_csv(csv_rating)
#    return   


threshold = 100
def InferRatings_R(All_GameInstances, csv_rating, size):
    PlayerRating_Init = {} #ReadRatings(csv_rating)    
    PlayerRating = PlayerRating_Init.copy()
    PlayerRating_prev = {}    
    min_error = [10000000000, {}]
    keep_running = True    
    iteration = 0    
    
    while keep_running:
        Rating_Table = {} 
        for i in range(0, len(All_GameInstances)):
            GameInstance = All_GameInstances[i]
            teamA = list()
            teamB = list()
            for j in range(0, len(GameInstance.TeamA)):
                PID = GameInstance.TeamA[j]
                if PID not in PlayerRating:
                    PlayerRating[PID] = 9.0
                if PID not in Rating_Table:
                    Rating_Table[PID] = [0.0, 0]
                teamA.append(round(float(PlayerRating[PID]), 1))
                
            for k in range(0, len(GameInstance.TeamB)):
                PID = GameInstance.TeamB[k]
                if PID not in PlayerRating:
                    PlayerRating[PID] = 9.0
                if PID not in Rating_Table:
                    Rating_Table[PID] = [0.0, 0]
                teamB.append(round(float(PlayerRating[PID]), 1))
            adj = CalculateAdjustment(teamA, teamB, (GameInstance.ScoreA - GameInstance.ScoreB))     
            
            for j in range(0, len(GameInstance.TeamA)):
                PID = GameInstance.TeamA[j]
                Rating_Table[PID][0] += round((float(PlayerRating[PID]) + adj), 1)
                Rating_Table[PID][1] += 1
            for k in range(0, len(GameInstance.TeamB)):
                PID = GameInstance.TeamB[k]
                Rating_Table[PID][0] += round((float(PlayerRating[PID]) - adj), 1)
                Rating_Table[PID][1] += 1

        for PID in Rating_Table:
            PlayerRating[PID] = format((Rating_Table[PID][0] / Rating_Table[PID][1]), '.1f')         
        
        error_per_game = ErrorPerGame(All_GameInstances, PlayerRating) 
        if error_per_game <= min_error[0]:
            min_error[0] = error_per_game
            min_error[1] = PlayerRating.copy() # need to be a shallow copy, otherwise it will be changed in next iteration
                
        # check if the ratings stop updating
        still_updating = False
        for PID in PlayerRating:
            if PID not in PlayerRating_prev:
                still_updating = True
                break
            if PlayerRating[PID] != PlayerRating_prev[PID]:
                still_updating = True
                break
            
        if still_updating == False:
            keep_running = False
        elif min_error[0] == 0:
            keep_running = False
        elif iteration == threshold:
            keep_running = False
        
        iteration += 1     
        PlayerRating_prev = PlayerRating.copy()

    CreateRecord2(size, min_error[0], iteration)
    PR = pandas.Series(min_error[1])
    PR.to_csv(csv_rating)
    print(iteration)
    print(min_error[0])
    print(min_error[1])
    return 


def ReadRatings(csv_rating):
    try:
        PlayerRating = pandas.Series.from_csv(csv_rating).to_dict()  
        return PlayerRating
    except:
        return {}
        
   
def CalculateAdjustment(teamA, teamB, SD_act):
    SD_calc = ScorePredictor(teamA, teamB)
    adjustment = (SD_act - SD_calc) / 1.3
    return adjustment
    
    
def ScorePredictor(teamA, teamB):
    avgA = sum(teamA)/len(teamA)
    avgB = sum(teamB)/len(teamB)
    avgDiff = abs(avgA - avgB)    
    if avgDiff < 0.27:
        return 0
    
    avgDiff = avgDiff * 2
    if 1.5 < avgDiff < 1.75:     
            avgDiff = 1.4
    
    scoreDiff = int(round(avgDiff))
    
    if avgA > avgB:
        return scoreDiff
    else:   # avgA < avgB
        return (0 - scoreDiff)
    
   
def ErrorPerGame(All_GameInstances, PlayerRating):
    Err_total = 0;  
    for i in range(0, len(All_GameInstances)):
        GameInstance = All_GameInstances[i]
        teamA = list()
        teamB = list()
        for j in range (0, len(GameInstance.TeamA)):
            PID = GameInstance.TeamA[j]
            teamA.append(round(float(PlayerRating[PID]), 1)) 
        for k in range(0, len(GameInstance.TeamB)):
            PID = GameInstance.TeamB[k]
            teamB.append(round(float(PlayerRating[PID]), 1))          
        SD_act = abs(GameInstance.ScoreA - GameInstance.ScoreB)
        SD_calc = abs(ScorePredictor(teamA, teamB))
        error = abs(SD_act - SD_calc)            
        Err_total += error    

    Err_per_game = Err_total / (i+1)
    CreateRecord(Err_per_game, PlayerRating)      
    return Err_per_game
  
  
def CreateRecord(error, dic_player_ratings):
    new_list = [[None] * (len(dic_player_ratings) + 1)]
    new_list[0][0] = error
    i = 1
    for key in dic_player_ratings:
        new_list[0][i] = key + ":" + str(dic_player_ratings[key])
        i += 1

    new_row = pandas.DataFrame(new_list)   
    new_row.to_csv(r'C:\Users\shang\Documents\GitHub\MachineLearning---TeamChooser\G_1_3_Records_Error_Rating_20170126.csv', mode='a', index=False, header=False)
    return
    
def CreateRecord2(size, error, iteration):
    new_list = [[None]*3]
    new_list[0][0] = size
    new_list[0][1] = error
    new_list[0][2] = iteration
    new_row = pandas.DataFrame(new_list)   
    new_row.to_csv(r'C:\Users\shang\Documents\GitHub\MachineLearning---TeamChooser\G_1_3_Records_Error_Iteration_20170126.csv', mode='a', index=False, header=False)
    return
    