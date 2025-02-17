import pandas as pd
import numpy as np
import edhec_risk_kit_201 as ed
import statsmodels.api as sm

'''
Analyse factorielle avec CAPM (ou MEDAF en Français) et le modèle à 3 facteurs de Fama et French,
sur les données de rendements mensuels de Berkshire Hathaway.
'''

brka_d = pd.read_csv('data/brka_d_ret.csv', parse_dates= True, index_col=0)
print(brka_d.head())

brka_m = brka_d.resample('ME').apply(ed.compound).to_period('M')
print(brka_m.head())

brka_m.to_csv('data/brka_m_ret.csv') 

# On charge les variables explicatives (facteurs)
fff = ed.get_fff_returns()
print(fff.head())
# fff : Mkt-RF (endemenet excédentaire du marché Rmk - Rf), SMB (Small Minus Big) et HML (High Minus Low) et RF (Risk Free rate)

# Utilisons CAPM : R_{brka,t} - R_{f,t} = \alpha + \beta(R_{mkt,t} - R_{f,t}) + epsilon_t
# Rendement excé de BH = alpha + beta * rendement excé du marché + erreur
# rappel : alpha est la perf ajusté du risque, beta est la sensibilité au marché

# On peut faire une décomposition factoriell avec une : regréssion linéaire de 1990 à 2012
brka_excess = brka_m["1990":"2012-05"] - fff.loc["1990":"2012-05", ['RF']].values # R_{brka,t} - R_{f,t} = rendement excédentaire de Berkshire Hathaway
mkt_excess = fff.loc["1990":"2012-05", ['Mkt-RF']] # R_{mkt,t} - R_{f,t} = rendement excédentaire du marché
exp_var = mkt_excess.copy() 
exp_var['Constant'] = 1 # alpha

# OLS : Ordinary Least Squares (Moindres Carrés Ordinaires)
lm = sm.OLS(brka_excess, exp_var).fit()  
print(lm.summary()) 


'''
Ajout des facteurs SMB et HML de Fama et French
'''
exp_var["Value"] = fff.loc["1990":"2012-05",['HML']]
exp_var["Size"] = fff.loc["1990":"2012-05",['SMB']]

lm2 = sm.OLS(brka_excess, exp_var).fit()
print(lm2.summary())
