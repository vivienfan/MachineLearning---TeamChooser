# -*- coding: utf-8 -*-
"""
Created on Mon Sep 12 13:32:58 2016

@author: Vivien Y. Fan
"""
import Preprocessor
import GameInstance
#import MachineLearningAlgorithm
import Application
#import PerformanceAnalysis


def main(size):
#    csvFile_actualRating = r'C:\Users\shang\Documents\GitHub\MachineLearning---TeamChooser\Milestone3_DataAnalysis\rating_list.csv'
#    csvFile_rawData = r'C:\Users\shang\Documents\GitHub\MachineLearning---TeamChooser\game_instances_.csv'
    csvFile_rawData = r'C:\Users\shang\Documents\GitHub\MachineLearning---TeamChooser\database.csv'
#    csvFile_processedData = r'C:\Users\shang\Documents\GitHub\MachineLearning---TeamChooser\ProcessedData.csv'
    csvFile_playerRating =  r'C:\Users\shang\Documents\GitHub\MachineLearning---TeamChooser\PlayerRating.csv'
#    csvFile_analysis = r'C:\Users\shang\Documents\GitHub\MachineLearning---TeamChooser\Milestone3_DataAnalysis\PerformanceAnalysis.csv'
    
#    num_players = 150
    
#    for i in range (1, 201):
        # step 1: preprocessing and feature extracting
#    Preprocessor.RawDataProcessor(csvFile_rawData, csvFile_processedData, 1000)    
    All_GameInstances = Preprocessor.ExtractData(csvFile_rawData, size)
        # step 2: Training (offline) - machine learning system (iterative process)
    #    MachineLearningAlgorithm.IterativeTrainingSystem()
      
        # step 3: Testing (online)
#    Application.RatingCalculator(csvFile_processedData, csvFile_playerRating)
    Application.InferRatings_R(All_GameInstances, csvFile_playerRating, size)
    
        # extra step: Performance analysis
#        PerformanceAnalysis.Analysis(csvFile_actualRating, csvFile_playerRating, csvFile_analysis, i*5, num_players)    
        
#    PerformanceAnalysis.Plot(csvFile_analysis)
    return
    
  
if __name__ == "__main__":
    main(5)
    main(10)
    main(20)
    main(30)
    main(40)
    main(50)
    main(60)
    main(70)
    main(80)
    main(90)
    main(100)
    main(110)
    main(120)
    main(130)
    main(140)
    main(150)
    main(160)
    main(170)
    main(180)
    main(190)
    main(200)
    main(250)
    main(300)
    main(400)
    main(500)
    main(600)
    main(700)
    main(800)
    main(900)
    main(1000)