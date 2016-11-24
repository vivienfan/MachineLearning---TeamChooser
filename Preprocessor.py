# -*- coding: utf-8 -*-
"""
Created on Mon Sep 12 13:32:58 2016

@author: Vivien Y. Fan
"""
import math
import pandas
import GameInstance

#def RawDataProcessor(csvFile_toRead, csvFile_toWrite, size):
#    """ Extract raw data from a given csv file.
#        Preprocess the raw data into desired form.
#        Write processed data into a csv file.
#    
#        Arg:
#            csvFile: the path to a csv file
#        Returns:
#        Raises:
#            OSError: file does not exist            
#    """    
#    processedData = [['player_A1', 'player_A2', 'player_A3', 
#                     'player_A4', 'player_A5', 'player_A6', 'score_A',
#                     'player_B1', 'player_B2', 'player_B3', 
#                     'player_B4', 'player_B5', 'player_B6', 'score_B']]
#    rawData = pandas.read_csv(filepath_or_buffer=csvFile_toRead, index_col=None,header=None)
#    rawMatrix = pandas.DataFrame.as_matrix(rawData)    
#
#    a = [None] * 14             
#    for i in range (0, size):
#        for j in range(0, 6):
#            a[j] = rawMatrix[i*8+j][0]
#            a[j+6] = rawMatrix[i*8+j][2]
#        a[12] = rawMatrix[i*8+j+1][1]
#        a[13] = rawMatrix[i*8+j+1][3]
#        processedData.append(a.copy())
#            
#    updatedData = pandas.DataFrame(processedData)
#    updatedData.to_csv(csvFile_toWrite, header=0)
#
#    return
        
        
def isNaN(value):
    try:
        return math.isnan(float(value))
    except:
        return False
    

def ExtractData(csvFile_toRead, size):
    rawData = pandas.read_csv(csvFile_toRead, header=None)
    rawMatrix = pandas.DataFrame.as_matrix(rawData) 
    All_GameInstances = []
    extract_more = True
    row = 0
    game_count = 0
    while(extract_more):
        teamA = []
        teamB = []
        extract_one = True
        while(extract_one):
            if isNaN(rawMatrix[row][0]) == False: # row is not empty
                if rawMatrix[row][0] == "Game ID: ":
                    GID = rawMatrix[row][1]
                elif rawMatrix[row][0] == "Score":
                    scoreA = int(rawMatrix[row][2])
                    scoreB = int(rawMatrix[row][5])
                elif rawMatrix[row][0] == "player id":
                    pass # do nothing
                else:   # player info, only add player if the cell is not empty
                    if isNaN(rawMatrix[row][0]) == False:
                        teamA.append(rawMatrix[row][0])
                    if isNaN(rawMatrix[row][3]) == False:
                        teamB.append(rawMatrix[row][3])
            else: # row is empty, done reading one game instance
                game_count += 1
                new_GameInstance = GameInstance.GameInstance(GID, teamA, teamB, scoreA, scoreB)
                All_GameInstances.append(new_GameInstance)
                extract_one = False
            row += 1 # increament row
            
        if game_count == size:
            extract_more = False;
        
    return All_GameInstances