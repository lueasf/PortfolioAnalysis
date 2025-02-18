# Analyses de Portefeuilles de l'EDHEC

## Factor
Analyse factorielle avec CAPM (ou MEDAF en Français) et le modèle à 3 facteurs de Fama et French,
sur les données de rendements mensuels de Berkshire Hathaway.
### CAPM

- resample('ME') : moyenne mensuelle
- resample('QE') : moyenne trimestrielle
- resample('YE') : moyenne annuelle

Analyse : 
- alpha = 0.0061 : BH a surperformé le marché de 0.0061 * 12 = 7,32% par an
- beta = 0.5 < 1 : BH est moins volatile que le marché
- p-value > 0.05 : il n'y a pas assez de preuves stats pour dire que alpha est réellement différent de 0.

### Fama French

Rappel :
SMB positif : actif exposé aux petites capitalisations
SMB négatif : actif exposé aux grandes capitalisations

HML positif : actif exposé aux actions de valeur
HML négatif : actif exposé aux actions de croissance

Analyse :
- alpha = 0.0055
- beta = 0.6761 : BH est moins volatile que le marché
- HML : 0.3814 : BH est exposé aux actions de valeur
- SMB : -05023 : BH investit dans des grandes capitalisations (big caps)

>Les valeurs ont changés, ainsi, ajouté ces facteurs changent effectivement les résultats de l'analyse.

## Comp
Les EW et les CW ou VW sont des portefeuilles pondérés par la capitalisation boursière.
- EW : Equal Weighted, chaque action a le même poids
- CW ou VW : Capital Weighted, chaque action a un poids proportionnel à sa capitalisation boursière (Ex: S&P 500)

## Backtest
- Series() est une classe de pandas qui permet de manipuler des séries temporelles

## Black
Le modèle de Black-Litterman est une extension du modèle d'optimisation de portefeuille de Markowitz. Il combine deux sources d'information :
- les redements implicites du marché (les rendements que le "marché" attend pour chaque actif) (issu de Markowitz)
- les vues de l'investisseur

Pour calculer les rendements implicites (pi) à partir des poids de marché (w),
on utilise _The Master Formula_ :
$$\pi = \delta \Sigma w$$, avec :
- $\pi$ : rendements implicites vectoriels
- $\delta$ : aversion au risque de l'invesstisseur
- $\Sigma$ : matrice de variance-covariance des rendements
- $w$ : vecteur des poids d'équilibre du marché ou pondérations de marché

Les rendements implicites sont des rendements objectifs basé sur les poids d'équilibre du marché. Ils représentent donc une vision "neutre" des rendements futurs.

- squeeze() est une méthode de pandas qui est utilisé pour réduire les dimensions d'un objet.
- dot() est une méthode qui permet de faire le produit matriciel entre deux matrices.

ÉTAPES :
1) Calcul des rendements implicites : π=δ⋅Σ⋅wπ=δ⋅Σ⋅w.
2) Ajustement des rendements : μ = π + τΣPT(PτΣPT + Ω)^−1 * (q−Pπ)
3) Ajustement de la covariance : Σ = Σ + τΣ − τΣP^T(PτΣPT + Ω)^−1 * PτΣ
