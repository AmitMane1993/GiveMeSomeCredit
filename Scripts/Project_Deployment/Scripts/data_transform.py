import pandas as pd

Delay_param = ["NumberOfTime30-59DaysPastDueNotWorse",
               "NumberOfTime60-89DaysPastDueNotWorse",
               "NumberOfTimes90DaysLate"]

interval = (0,18, 25, 35, 60, 110)
cats = [0,1,2,3,4]                                                                # 'Child':0,'Student':1, 'Young':2, 'Adult':3, 'Old':4

def dataPreparation(data):
    data['Weighted_Delay_sum'] = data[Delay_param[0]].values[0]*0.2+\
                                 data[Delay_param[1]].values[0]*0.3+\
                                 data[Delay_param[2]].values[0]*0.5
    
    data['age_cat'] = pd.cut([data.age.values[0]], interval, labels=cats)
        
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