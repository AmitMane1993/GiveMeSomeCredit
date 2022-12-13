import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin

class Data_Preparation(BaseEstimator,TransformerMixin):
    def __init__(self):        
        self.interval = (0,18, 25, 35, 60, 110)
        self.cats = [0,1,2,3,4]    
        
    def fit(self,X):
        return self
    
    def transform(self,X):
        X=X.copy()
        
        Delay_param = ["NumberOfTime30-59DaysPastDueNotWorse",
               "NumberOfTime60-89DaysPastDueNotWorse",
               "NumberOfTimes90DaysLate"]
        
        X['Weighted_Delay_sum'] = X[Delay_param[0]].values[0]*0.1+\
                                 X[Delay_param[1]].values[0]*0.3+\
                                 X[Delay_param[2]].values[0]*0.6
        
        X['age_cat'] = pd.cut([X.age.values[0]], self.interval, labels=self.cats)
        
        X['NumberOfDependentsTR'] = X['NumberOfDependents']
        X.loc[X.NumberOfDependentsTR>=7,'NumberOfDependentsTR'] = 7

        X['NumberRealEstateLoansOrLinesTR'] = X['NumberRealEstateLoansOrLines']
        X.loc[X.NumberRealEstateLoansOrLinesTR>=11,'NumberRealEstateLoansOrLinesTR'] = 11

        X['NumberOfOpenCreditLinesAndLoansTR'] = X['NumberOfOpenCreditLinesAndLoans']
        X.loc[X.NumberOfOpenCreditLinesAndLoansTR>=25,'NumberOfOpenCreditLinesAndLoansTR'] = 25
        
        transformed_feature = ['RevolvingUtilizationOfUnsecuredLines',
                           'Weighted_Delay_sum', 
                           'age_cat',
                           'MonthlyIncome', 
                           'DebtRatio', 
                           'NumberOfDependentsTR',
                           'NumberRealEstateLoansOrLinesTR', 
                           'NumberOfOpenCreditLinesAndLoansTR']
                
        return X[transformed_feature]