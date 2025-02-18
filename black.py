import numpy as np
from numpy.linalg import inv
import pandas as pd
from scipy.optimize import minimize

'''
Introduction au modèle de l'allocation d'actif de Black-Litterman.
'''

# transforme un vecteur en colonne
def as_colvec(x):
    if (x.ndim == 2):
        return x
    else:
        return np.expand_dims(x, axis=1)
    
# print(as_colvec(np.array([1, 2, 3]))) # [[1], [2], [3]] en colonne

# renvoie les rendements implicites selon The Master Formula
# sigma.dot(w) donne un DataFrame et squeeze() le transforme en Series
def implied_returns(delta, sigma, w):
    ir = delta * sigma.dot(w).squeeze() # to get a series from a 1-column dataframe
    ir.name = 'Implied Returns'
    return ir

sigma = pd.DataFrame([[0.1], [0.2], [0.3]])  # DataFrame (3,1)
w = pd.Series([1])  # Vecteur poids
delta = 2


# renvoie cette formule : $$\Omega = diag(P (\tau \Sigma) P^T) $$
def proportional_prior(sigma, tau, p):
    helit_omega = p.dot(tau * sigma).dot(p.T) # avec p.T = p.transpose()
    return pd.DataFrame(np.diag(np.diag(helit_omega.values)),index=p.index, columns=p.index)


# renvoie les rendements ajustés et la matrice de covariance ajustée
def bl(w_prior, sigma_prior, p, q,
                omega=None,
                delta=2.5, tau=.02):
    '''
    sigma_prior: matrice de covariance des rendements
    p : matrice des vues de l'investisseur
    q : vecteur des prévisions de l'investisseur
    '''
    if omega is None:
        omega = proportional_prior(sigma_prior, tau, p)
  
    N = w_prior.shape[0] 
    K = q.shape[0] 

    # étape 1 : calcul des rendements implicites avec The Master Formula
    pi = implied_returns(delta, sigma_prior,  w_prior) 

    sigma_prior_scaled = tau * sigma_prior   

    # étape 2 : ajustement des rendements espérés
    mu_bl = pi + sigma_prior_scaled.dot(p.T).dot(inv(p.dot(sigma_prior_scaled).dot(p.T) + omega).dot(q - p.dot(pi).values))

    # étape 3 : ajustement de la mat de cov
    sigma_bl = sigma_prior + sigma_prior_scaled - sigma_prior_scaled.dot(p.T).dot(inv(p.dot(sigma_prior_scaled).dot(p.T) + omega)).dot(p).dot(sigma_prior_scaled)
    return (mu_bl, sigma_bl)


# Avec cette fonction on peut donc grace à la matrice de cov, 
# calculer le portefeuille optimal.


# Exemple avec ces valeurs :

# Rendements attendus ajustés (8% pour l'actif 1, 12% pour l'actif 2, qui semble plus attractif)
mu_bl = pd.Series([0.08, 0.12])  
sigma_bl = pd.DataFrame([[0.03, 0.03], [0.03, 0.08]])  # mat co avec 0.03 la variance de l'actif 1 < 0.08 la variance de l'actif 2
# >> actif 1 est moins risqué et moins rentable que l'actif 2

n_actifs = len(mu_bl)

# sharpe ratio avec un taux sans risque de 2% (l'actif doit rapporter plus que 2% pour être intéressant)
def neg_sharpe(weights, mu, sigma, risk_free=0.02):
    port_return = np.dot(weights, mu) # rendement du portefeuille
    port_volatility = np.sqrt(weights.T @ sigma @ weights) # volatilité du portefeuille
    return -(port_return - risk_free) / port_volatility

ctrs = {'type': 'eq', 'fun':lambda w: np.sum(w) -1} # on investit tout l'argent
bornes = [(0, 1) for _ in range(n_actifs)]

init_weights = np.array([1/n_actifs] * n_actifs) # poids initiaux 50 50

res = minimize(neg_sharpe, init_weights, args=(mu_bl, sigma_bl), constraints=ctrs, bounds=bornes)
optimal_weights = res.x
print(optimal_weights)  # [0.60146761 0.39853239]

# Analyse : 60% de l'argent doit être investi dans l'actif 1 et 39% dans l'actif 2