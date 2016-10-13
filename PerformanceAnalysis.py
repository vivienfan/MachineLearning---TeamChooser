# -*- coding: utf-8 -*-
"""
Created on Wed Oct 12 13:23:43 2016

@author: Viven.Y Fan
"""

def Analysis(csv_actual_rating, csv_calculated_rating, csv_performance, num_games, num_players):
    import pandas
    
    dic_act = pandas.Series.from_csv(csv_actual_rating).to_dict() 
    dic_cal = pandas.Series.from_csv(csv_calculated_rating).to_dict() 

    total_error = 0;
    counter = 0;

    for key in dic_cal:
        actual_rating = int(dic_act[key])
        calculated_rating = int(dic_cal[key])
        total_error += (abs(actual_rating - calculated_rating) / actual_rating) * 100
        counter += 1

    avg_error = total_error / counter
    
    new_row_list = [(num_games, num_players, avg_error)]
    print(new_row_list)
    new_row = pandas.DataFrame(new_row_list)
    new_row.to_csv(csv_performance, mode='a', index=False, header=False)
    
    return
    
def Plot(csv_performance):
    import pandas
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D   
    import pylab
    
    performance = pandas.read_csv(csv_performance)    
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(performance['# game instances'], performance['# players'], performance['avg %error'])
    pylab.show()
    return