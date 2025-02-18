import numpy as np
import pandas as pd

import edhec_risk_kit_204 as erk

'''
Backtesting sur les indices de marché.
'''

ind49_rets = erk.get_ind_returns(weighting="vw", n_inds=49)["1974":]
ind49_mcap = erk.get_ind_market_caps(49, weights=True)["1974":]

# On calcule les poids de chaque indice
def weight_ew(r):
    n = len(r.columns)
    return pd.Series(1/n, index=r.columns)

# backtest d'un portefeuille 
def backtest_ws(r, estimating_window=60, weighting=weight_ew):
    pass