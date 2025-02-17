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
Les EW et les CW sont des portefeuilles pondérés par la capitalisation boursière.
- EW : Equal Weighted, chaque action a le même poids
- CW : Capital Weighted, chaque action a un poids proportionnel à sa capitalisation boursière (Ex: S&P 500)

Analyse :
