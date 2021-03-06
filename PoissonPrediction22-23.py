# Poisson Prediction 2022/23 Premier League Season
# Python
# Author: Ben Johnson
# Date: June 2022

# This program uses the 2021/22 Premier League season
# goalscoring statistics to determine the probable number
# of goals scored in a game, in the 2022/23 season.
# Each team is assigned an attack and defence "strength"
# as well as expected goals (xG) for the desired fixture.
# Using the Poisson Distribution formula we can generate 
# all 36 possible scoreline probabilities with <=10 goals total.
# The program outputs expected goals for each side, scoreline
# probabilities over 7.5% and a table of away goal % and
# home goal % for all permutations.

# imports
import math # for calculations using e and factorial (!)
from tabulate import tabulate # to create the table of permutations

# global variables
HomeGames = 19
TotalGames = 380 
TotalHomeGoals = 575 # total home goals scored PL 2021/22
TotalAwayGoals = 496 # total away goals scored PL 2021/22
ResultList = [] # to store the results of the Poisson formula

# base class definition
class PoissonPrediction():
    
    # initialization method
    # user inputs 4 values here used in the Poisson and xG formulas
    def __init__(self):
        self.Home_score_Home = int(input("\nHow many goals did the home team score at home last season? "))
        self.Away_con_Away = int(input("How many goals did the away team concede away from home last season? "))
        self.Away_score_Away = int(input("How many goals did the away team score away last season? "))
        self.Home_con_Home = int(input("How many goals did the home team concede at home last season? "))
    
    # calculate home team attacking strength
    def HTAS(self):
        temp_1 = TotalHomeGoals / TotalGames 
        temp_2 = round(self.Home_score_Home / HomeGames, 3) 
        HTAS = round(temp_2 / temp_1, 3)
        return HTAS

    # calculate away team defensive strength
    def ATDS(self):
        temp_1 = round(self.Away_con_Away / HomeGames, 3) 
        temp_2 = TotalHomeGoals / TotalGames 
        ATDS = round(temp_1 / temp_2, 3)
        return ATDS

    # calculate away team attacking strength
    def ATAS(self):
        temp_1 = TotalAwayGoals / TotalGames
        temp_2 = round(self.Away_score_Away / HomeGames, 3) 
        ATAS = round(temp_2 / temp_1, 3) 
        return ATAS

    # calculate home team defensive strength
    def HTDS(self):
        temp_1 = round(self.Home_con_Home / HomeGames, 3)
        HTDS = round(temp_1 / (TotalAwayGoals / TotalGames), 3)
        return HTDS
    
    # expected home goals (xG)
    def xHG(self, HTAS, ATDS):
        xHG = round(HTAS * ATDS * (TotalHomeGoals/TotalGames), 2)
        return xHG

    # expected away goals (xG)
    def xAG(self, ATAS, HTDS):
        xAG = round(ATAS * HTDS * (TotalAwayGoals / TotalGames), 2)
        return xAG

    # Poisson Distribution = [ (??^k) * (e^-??) ] / k! 
    # used a nested for loop to calculate the 36 permutations
    def PoissonDistribution(self, xHG, xAG):
        for HomeGoalProb in range(6):
            for AwayGoalProb in range(6):
                var1 = (xHG) ** HomeGoalProb
                var2 = math.e**(-xHG)
                var3 = math.factorial(HomeGoalProb)

                var4 = (xAG) ** AwayGoalProb
                var5 = math.e ** (-xAG)
                var6 = math.factorial(AwayGoalProb)

                HomeChance = round( (var1*var2) / var3, 4)
                AwayChance = round( (var4*var5) / var6, 4)

                ResultChance = round((HomeChance*AwayChance)*100, 2)

                if ResultChance > 7.5:
                    print(HomeGoalProb, "-", AwayGoalProb, "scoreline chance is", ResultChance,"%")

                ResultList.append(ResultChance)

    def PlotResults(self):
        ResultGroups = list(zip(*(iter(ResultList),) * 6))

        print("\n     ---   Away Goals   ---")
        print("0     1     2     3     4     5")
        print(tabulate(ResultGroups))
        print("\n")

# function calls
# create object instance
PP = PoissonPrediction()

# calculate and display expected goals 
# based on attacking / defensive strength
print("\n- - Expected Goals - -\n")
print("Home xG:", end = " ")
print(PP.xHG(PP.HTAS(), PP.ATDS()))
print("Away xG:", end = " ")
print(PP.xAG(PP.ATAS(), PP.HTDS()))

# calculate and display Poisson Distribution for n <= 5 goals for each team
print("\n- - Poisson Distribution - -\n")
PP.PoissonDistribution(PP.xHG(PP.HTAS(), PP.ATDS()), PP.xAG(PP.ATAS(), PP.HTDS()))

# display the predicted Home / Away scorelines
PP.PlotResults()
