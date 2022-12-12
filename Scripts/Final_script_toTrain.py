import pandas as pd
import numpy as np
import configparser

Delay_param = ["NumberOfTime30-59DaysPastDueNotWorse",
               "NumberOfTime60-89DaysPastDueNotWorse",
               "NumberOfTimes90DaysLate"]

interval = (0,18, 25, 35, 60, 110)
cats = [0,1,2,3,4]                                                                # 'Child':0,'Student':1, 'Young':2, 'Adult':3, 'Old':4

def dataPreparation(data):
    data.loc[data[Delay_param[0]].isin([96,98]),Delay_param[0]] = 0
    data.loc[data[Delay_param[0]].isin([96,98]),Delay_param[1]] = 0
    data.loc[data[Delay_param[0]].isin([96,98]),Delay_param[1]] = 0
    
    data['Weighted_Delay_sum'] = data[Delay_param[0]]*0.2+\
                                             data[Delay_param[1]]*0.3+\
                                             data[Delay_param[2]]*0.5
    
    data['age_cat'] = pd.cut(data.age, interval, labels=cats)
    
    child = 0                                                                 # data.loc[data.age_cat=='Child','MonthlyIncome'].median()
    student = data.loc[data.age_cat==1,'MonthlyIncome'].median()
    young = data.loc[data.age_cat==2,'MonthlyIncome'].median()
    adult = data.loc[data.age_cat==3,'MonthlyIncome'].median()
    old = data.loc[data.age_cat==4,'MonthlyIncome'].median()
    
    data.loc[(data.age_cat=='Child')&(data.MonthlyIncome.isna()),'MonthlyIncome'] = child
    data.loc[(data.age_cat=='Student')&(data.MonthlyIncome.isna()),'MonthlyIncome'] = student
    data.loc[(data.age_cat=='Young')&(data.MonthlyIncome.isna()),'MonthlyIncome'] = young
    data.loc[(data.age_cat=='Adult')&(data.MonthlyIncome.isna()),'MonthlyIncome'] = adult
    data.loc[(data.age_cat=='Old')&(data.MonthlyIncome.isna()),'MonthlyIncome'] = old
    
    data['NumberOfDependentsTR'] = data['NumberOfDependents']
    data.loc[data.NumberOfDependentsTR>=7,'NumberOfDependentsTR'] = 7

    data['NumberRealEstateLoansOrLinesTR'] = data['NumberRealEstateLoansOrLines']
    data.loc[data.NumberRealEstateLoansOrLinesTR>=11,'NumberRealEstateLoansOrLinesTR'] = 11

    data['NumberOfOpenCreditLinesAndLoansTR'] = data['NumberOfOpenCreditLinesAndLoans']
    data.loc[data.NumberOfOpenCreditLinesAndLoansTR>=25,'NumberOfOpenCreditLinesAndLoansTR'] = 25
    
    
    transformed_feature = ['RevolvingUtilizationOfUnsecuredLines',
                           'Weighted_Delay_sum', 
                           'age_cat',
                           'MonthlyIncome', 
                           'DebtRatio', 
                           'NumberOfDependentsTR',
                           'NumberRealEstateLoansOrLinesTR', 
                           'NumberOfOpenCreditLinesAndLoansTR']
    
    
    return data[transformed_feature]