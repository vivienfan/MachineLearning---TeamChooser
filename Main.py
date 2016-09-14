# -*- coding: utf-8 -*-
"""
Created on Mon Sep 12 13:32:58 2016

@author: Vivien Y. Fan
"""
import Preprocessor
import MachineLearningAlgorithm
import Predictor


def main():
    csvFile_toRead = r'C:\Users\shang\Downloads\Sacramentorealestatetransactions.csv'
    csvFile_toWrite = r'C:\Users\shang\Downloads\ToWrite.csv'
    
    # step 1: preprocessing and feature extracting
    games = Preprocessor.RawDataProcessor(csvFile_toRead)
    print(games.columns)
    print(games.head())

    # step 2: Training (offline) - machine learning system (iterative process)
    model = MachineLearningAlgorithm.IterativeTrainingSystem(games)
    print(model)
  
    # step 3: Testing (online)
    newGame = ["player1", "player2","player3","player4","player5",
               "player6","player7","player8","player9","player10",
               "3:2"] # temperary
    Predictor.PredictingFunction(model, games, newGame, csvFile_toWrite)
    return
    
  
if __name__ == "__main__":
    main()