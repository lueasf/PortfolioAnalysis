import numpy as np
import pandas as pd
import yfinance as yf
from scipy.spatial import ConvexHull
import matplotlib.pyplot as plt

tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN']
data = yf.download(tickers, start='2020-01-01', end='2025-01-01')['Close']
 
returns = data.pct_change().dropna()
 
num_portfolios = 10000
results = np.zeros((3, num_portfolios)) # array with 3*10k elements. 
# will stock : returns, volatility, sharpe ratio

for i in range(num_portfolios):
    weights = np.random.random(len(tickers))
    weights /= np.sum(weights)  # Normaliser les poids pour qu'ils somment à 1
    portfolio_return = np.sum(returns.mean() * weights) * 252  # Rendement annualisé
    portfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(returns.cov() * 252, weights)))  # Volatilité annualisée
    results[0, i] = portfolio_return
    results[1, i] = portfolio_volatility
    results[2, i] = results[0, i] / results[1, i]  # Ratio de Sharpe (simplifié)

points = np.vstack((results[1], results[0])).T  # Combiner volatilité et rendement
hull = ConvexHull(points)
 
plt.figure(figsize=(10, 6))
plt.scatter(results[1], results[0], c=results[2], cmap='viridis', marker='o', label='Portefeuilles simulés')
plt.plot(points[hull.vertices, 0], points[hull.vertices, 1], 'r--', lw=2, label='Frontière efficiente')
plt.xlabel('Volatilité (Risque)')
plt.ylabel('Rendement')
plt.title('Frontière Efficiente avec Enveloppe Convexe')
plt.colorbar(label='Ratio de Sharpe')
plt.legend()
plt.show()