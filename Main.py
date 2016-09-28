# -*- coding: utf-8 -*-
"""
Created on Mon Sep 12 13:32:58 2016

@author: Vivien Y. Fan
"""
import Preprocessor
import MachineLearningAlgorithm
import Application


def main():
    csvFile_rawData = r'C:\Users\shang\Documents\GitHub\Synthetic-Data-Generator-TeamChooser\game_stances.csv'
    csvFile_processedData = r'C:\Users\shang\Documents\GitHub\MachineLearning---TeamChooser\ProcessedData.csv'
    csvFile_playerRating =  r'C:\Users\shang\Documents\GitHub\MachineLearning---TeamChooser\PlayerRating.csv'
    csvFile_combination = r'C:\Users\shang\Documents\GitHub\MachineLearning---TeamChooser\Combinations.csv'
    # step 1: preprocessing and feature extracting
    Preprocessor.RawDataProcessor(csvFile_rawData, csvFile_processedData, 10) 
    
    # step 2: Training (offline) - machine learning system (iterative process)
#    MachineLearningAlgorithm.IterativeTrainingSystem()
  
    # step 3: Testing (online)
    Application.RatingCalculator(csvFile_processedData, csvFile_playerRating, csvFile_combination)
    return
    
  
if __name__ == "__main__":
    main()