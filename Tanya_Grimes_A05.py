# -*- coding: utf-8 -*-
"""
PROG8420 - Programming for Big Data

Assignment 05

Created on Wed Jul 29 16:40:46 2020

@author: Tanya Grimes

References:
    Additional learning materials:
    * https://numpy.org/doc/stable/reference/generated/numpy.unique.html
    * https://www.programiz.com/python-programming/methods/built-in/zip
"""


#-----------------------------------------------------
# Library imports


import numpy as np
import pandas as pd

# set dataframe options, so that the dataframe does not 
# truncate under these limits
pd.set_option('display.max_rows', 1000)
pd.set_option('display.max_columns', 1000)
pd.set_option('display.width', 200)


#-----------------------------------------------------
# Variable & Constant Declarations


# assuming each die has six sides
DIE_SIDES = 6
DIE_RANGE_END = DIE_SIDES + 1

die_num = 0
roll_num = 0
events_num = 0

outcomes = {
    'total': np.arange(1, DIE_RANGE_END, dtype=int),
    'u_total': np.empty(0),
    't_likelihood': np.empty(0),
    'a_actual': np.empty(0),
    'e_percentage': np.empty(0)
}


#-----------------------------------------------------
# Function Definitions

def run_simulation():
    # starts the simulation steps
    
    # calls to generate sum of outcomes
    prepare_outcomes_total()
        
    # calls to generate theoretical likelihood
    generate_outcomes_likelihood()
    
    # calls to generate simualtion of actual rolls
    generate_outcomes_actual()
    
    # calls to generate absolute error percentage
    generate_percentage_error()
    
    # print simulation result
    display_simulation_results()

        
def prepare_outcomes_total():
    # calls to generate outcome totals, based on dice user input
    
    global outcomes
    
    # loop through to add to outcome total list
    for d in range(1, die_num):
        outcomes['total'] = generate_outcomes_total()
  
            
def generate_outcomes_total():
    # generates a list of new totals from previous list
    
    total_each_outcome = np.empty(0)
    
    for f in range(1, DIE_RANGE_END):
        for l in outcomes['total']:
            total = f + l
            total_each_outcome = np.append(total_each_outcome, total)
    
    return total_each_outcome


def generate_outcomes_likelihood():
    # generates list of theoretical likelihood as a percentage
    
    global outcomes
    
    # stores two arrays: one for unique theoretical sums, one for frequency of each sum
    t_unique, t_frequency = np.unique(outcomes['total'], return_counts = True)
        
    # at larger values, the likelihood can get truncated
    rounded = 2 if die_num < 6 else 4
    
    # generates the theoretical likelihood of the sums
    t_likelihood = np.round(t_frequency / events_num * 100, rounded)
    
    outcomes['t_likelihood'] = t_likelihood
    outcomes['u_total'] = t_unique
    

def generate_outcomes_actual():
    # generates list of actual appearance of values as a percentage
    
    global outcomes
    
    # retrieve unique theoretical sums
    t_unique = outcomes['u_total']
    
    # generates random die rolls in a die_num x roll_num dimension array
    a_sim_die_rolls = np.random.randint(1, DIE_RANGE_END, (die_num, roll_num))
    
    # calculates sum of the dice rolls
    a_sim_die_rsum = np.sum(a_sim_die_rolls, axis=0)
    
    # stores two arrays: one for unique simulated sums, one for frequency of each sum
    a_unique, a_frequency = np.unique(a_sim_die_rsum, return_counts = True)
    
    # stitches two arrays together and stores them in a dictionary
    a_sim_frequency = dict(zip(a_unique, a_frequency))
    
    # prepare an array to store the actual simulation, with default 0
    a_actual = np.zeros(len(t_unique))
    
    # generates an array for the simulation including sums with 0 output
    s = 0
    for dsum in t_unique:
        for key in a_sim_frequency:
            if dsum == key:
                a_actual[s] = round(a_sim_frequency[key] / roll_num * 100, 2)
        s += 1
        
    outcomes['a_actual'] = a_actual
    
    
def generate_percentage_error():
    # generates list of percentage errors
    
    global outcomes
    
    # Percentage Error needs to be absolute
    outcomes['e_percentage'] = abs(outcomes['t_likelihood'] - outcomes['a_actual'])


def display_simulation_results():
    # displays simulation results in tabular form
    
    # creates display array and appends arrays to it
    display_arr = np.empty(0)
    display_arr = np.append(display_arr, outcomes['u_total'])
    display_arr = np.append(display_arr, outcomes['t_likelihood'])
    display_arr = np.append(display_arr, outcomes['a_actual'])
    display_arr = np.append(display_arr, outcomes['e_percentage'])
    
    # determine number of rows for simulation, based on number of dice selected
    row_num = len(outcomes['total']) if die_num == 1 else len(outcomes['u_total'])
    
    # generate matrix of arrays, populating by column instead of row
    display_matrix = np.reshape(display_arr, (row_num, 4), 'F')
    
    # sets row index to empty string
    display_rownames = [''] * row_num
    
    # sets labels for columns
    display_colnames = ['DIE FACE SUM', 'LIKELIHOOD %', 'ACTUAL %', '% ERROR']
    
    # generates a dataframe
    display_dataframe = pd.DataFrame(display_matrix, columns = display_colnames, index = display_rownames)
    
    # converts sum column to an integer
    display_dataframe = display_dataframe.astype({"DIE FACE SUM": int})
    
    #displays the simulation results
    print('\n', display_dataframe)



#-----------------------------------------------------
# Intro Display, User Input and Validation

print('\n-----------------------------------------------------------------')
print('* Enter the number of dice to use, and the number of rolls the')
print('  dice should make.\n')
print('* A summary of the simulation will be generated afterwards.\n')
print('* The number of dice chosen should be between 1 and 8 inclusive.\n')
print('* A larger dice number will increase the time to simulate,')
print('* especially after 6 dice.\n')
print('* Trailing and leading spaces will be removed from your input.\n')
print('* Only positive integers are allowed.')
print('-----------------------------------------------------------------')

#stores user input, trimming leading and trailing whitespaces
die_input = input('   Enter the number of dice to use: ').strip()

# validates dice number input
if len(die_input) == 0:
    print('   Dice input was not entered. Exiting simulation...\n')

# accommodates positive integers and plus in-front the integer
elif (die_input.isnumeric() and die_input.find('.') == -1) or (die_input[0] == '+' and die_input[1:].isnumeric() and die_input[1:].find('.') == -1):
    die_num = int(die_input)
    
    if die_num > 0 and die_num < 9:
        # stores user input, trimming leading and trailing whitespaces
        roll_input = input('   Enter the number of rolls to make: ').strip()
                
        # validates roll number input as well
        if len(roll_input) == 0:
            print('   Roll input was not entered. Exiting simulation...\n')
        
        # accommodates positive integers and plus in front of the integer
        elif (roll_input.isnumeric() and roll_input.find('.') == -1) or (roll_input[0] == '+' and roll_input[1:].isnumeric() and roll_input[1:].find('.') == -1):
            
            roll_num = int(roll_input)
            
            if roll_num > 0:
                # stores total number of outcomes, from the number of dice selected
                events_num = DIE_SIDES ** die_num
                
                # calls to start the simulation process
                run_simulation()
            else: print('   Roll input should be greater than 0. Exiting simulation...\n')
        else:
            print('   Roll input is not valid. Exiting simulation...\n')
    else:
        print('   Dice input should be between 1 and 8, inclusive. Exiting simulation...\n')
else:
    print('   Dice input is not valid. Exiting simulation...\n')
