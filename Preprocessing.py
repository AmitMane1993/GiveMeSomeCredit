import pandas as pd
import numpy as np
import scipy.stats as stats
import configparser
import warnings
warnings.filterwarnings('ignore')

Target = ['SeriousDlqin2yrs']

Percentage = ['RevolvingUtilizationOfUnsecuredLines','DebtRatio']

Real = ['MonthlyIncome']

Numeric_Param = ["NumberOfDependents",
                 "NumberRealEstateLoansOrLines",
                 "NumberOfOpenCreditLinesAndLoans",
                 "age"]

Delay_param = ["NumberOfTime30-59DaysPastDueNotWorse",
               "NumberOfTime60-89DaysPastDueNotWorse",
               "NumberOfTimes90DaysLate"]

interval = (0,18, 25, 35, 60, 110)
cats = ['Child','Student', 'Young', 'Adult', 'Old']

def mark_outliers_zscore(feature, threshold = 3):
    z = np.abs(stats.zscore(feature))
    res = [i for i,j in zip(z.index,z.values) if j >= threshold]
    return res

def debt(df,res):
    a = df.loc[(df.index.isin(res)),'DebtRatio_transformed']
    b = np.exp(df.loc[(df.index.isin(res)),'MonthlyIncome_lg'])-1
    
    for i,j in zip(df.loc[df.index.isin(res),'DebtRatio_transformed'].index,df.loc[df.index.isin(res),'DebtRatio_transformed'].values):
        if b[i]>1:
            df.loc[i,'DebtRatio_transformed'] = j/b[i]
    return df

def Data_Preprocessing(data):
    
    data.loc[data[Delay_param[0]].isin([96,98]),Delay_param[0]] = 0
    data.loc[data[Delay_param[0]].isin([96,98]),Delay_param[1]] = 0
    data.loc[data[Delay_param[0]].isin([96,98]),Delay_param[1]] = 0

    data['Weighted_Delay_sum'] = data[Delay_param[0]]*0.2+\
                                             data[Delay_param[1]]*0.3+\
                                             data[Delay_param[2]]*0.5

    data['age_cat'] = pd.cut(data.age, interval, labels=cats)

    data['MonthlyIncome_lg'] = np.log(data['MonthlyIncome']+1)

    child = 0 #data.loc[data.age_cat=='Child','MonthlyIncome_lg'].median()
    student = data.loc[data.age_cat=='Student','MonthlyIncome_lg'].median()
    young = data.loc[data.age_cat=='Young','MonthlyIncome_lg'].median()
    adult = data.loc[data.age_cat=='Adult','MonthlyIncome_lg'].median()
    old = data.loc[data.age_cat=='Old','MonthlyIncome_lg'].median()

    data.loc[(data.age_cat=='Child')&(data.MonthlyIncome_lg.isna()),'MonthlyIncome_lg'] = 0
    data.loc[(data.age_cat=='Student')&(data.MonthlyIncome_lg.isna()),'MonthlyIncome_lg'] = student
    data.loc[(data.age_cat=='Young')&(data.MonthlyIncome_lg.isna()),'MonthlyIncome_lg'] = young
    data.loc[(data.age_cat=='Adult')&(data.MonthlyIncome_lg.isna()),'MonthlyIncome_lg'] = adult
    data.loc[(data.age_cat=='Old')&(data.MonthlyIncome_lg.isna()),'MonthlyIncome_lg'] = old

    data['MonthlyIncome_nolg_'] = np.exp(data['MonthlyIncome_lg'])-1
    res = mark_outliers_zscore(data.DebtRatio)

    data['DebtRatio_transformed'] = data['DebtRatio']
    
    data = debt(data,res)
    
    data['NumberOfDependentsTR'] = data['NumberOfDependents']
    data.loc[data.NumberOfDependentsTR>=7,'NumberOfDependentsTR'] = 7

    data['NumberRealEstateLoansOrLinesTR'] = data['NumberRealEstateLoansOrLines']
    data.loc[data.NumberRealEstateLoansOrLinesTR>=11,'NumberRealEstateLoansOrLinesTR'] = 11

    data['NumberOfOpenCreditLinesAndLoansTR'] = data['NumberOfOpenCreditLinesAndLoans']
    data.loc[data.NumberOfOpenCreditLinesAndLoansTR>=25,'NumberOfOpenCreditLinesAndLoansTR'] = 25

    data.loc[data.NumberOfDependentsTR.isna(),'NumberOfDependentsTR'] = 0

    age_map = {'Child':0,'Student':1, 'Young':2, 'Adult':3, 'Old':4}
    data.age_cat = data.age_cat.map(age_map)
    
    return data