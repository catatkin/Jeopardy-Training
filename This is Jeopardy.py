#!/usr/bin/env python
# coding: utf-8

# # This is Jeopardy!

# #### Project Goals

# To investigate a dataset of _Jeopardy!_ questions and answers. Filter the dataset for topics of interest, compute the average difficulty of those questions, and train to become the next Jeopardy champion!

import pandas as pd
import random

# display full contents of a column:
pd.set_option('display.max_colwidth', None)

# save the csv to df and examine the data
df = pd.read_csv('jeopardy.csv')
print(df.head())
print(df.columns)

# There are spaces at the beginning of the column names. Remove them:
df.columns = df.columns.str.replace(' ', '')
print(df.columns)

# Create a function that checks for a list of words in the Question column of a dataframe:
def questions_filter(dataframe, word_list):
    # Define filter function to return true only if each word in word_list is in x:
    filter = lambda x: all(word in x for word in word_list)
    # Returns the subset of the dataframe that contains every word in word_list
    return dataframe.loc[dataframe['Question'].apply(filter)].reset_index()

# Test the function
filtered_df = questions_filter(df, ['King', 'England'])
# print(filtered_df['Question'])

# Let's create a function to use in cases that we want to find the lowercase versions of words as well:
def case_insensitive_filter(dataframe, word_list):
    filter = lambda x: all(word.lower() in x.lower() for word in word_list)
    return dataframe.loc[dataframe['Question'].apply(filter)].reset_index()

# test the function:
case_insensitive_df = case_insensitive_filter(df, [' lost ', 'heart'])
print(case_insensitive_df['Question'])
# in order to find standalone words, add a space before and after each word in the word list passed to the function

# Create a 'Value_float' column which contains floats instead of strings containing '$' and ',':
df['Value_float'] = df['Value'].apply(lambda x: float(x[1:].replace(',','')) if x != 'None' else 0)
# print(df.head())

# Now we can find the average difficulty of questions that contain the word "King"
def average_difficulty(dataframe, word_list):
    this_df = case_insensitive_filter(dataframe, word_list)
    average = this_df['Value_float'].mean()
    print(this_df['Value_float'])
    return average

word = 'King'
print("Average difficulty of questions that contain the word '{}': $".format(word), int(average_difficulty(df, [word])))

# Find unique answers to the dataset filtered for a word
def unique_answers(dataframe):
    return dataframe['Answer'].value_counts()

# Test function
king_df = case_insensitive_filter(df, ['King'])
print(unique_answers(king_df))

# Create a system to practice answering random questions
def play_game(dataframe):
    random_index = random.randint(0,len(dataframe))
    category = dataframe['Category'].iloc[random_index]
    value = dataframe['Value_float'].iloc[random_index]
    question = dataframe['Question'].iloc[random_index]
    answer = dataframe['Answer'].iloc[random_index]
    print("For ${}, in the category, {}, the question is: {}".format(value, category, question))
    user_input = input("Your answer: ")
    if user_input.lower() == answer.lower():
        print("Correct!")
    else:
        print("Sorry, the correct answer was: {}".format(answer))
        
play_game(df)




