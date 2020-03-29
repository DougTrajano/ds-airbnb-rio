# Airbnb - Rio de Janeiro

![](https://github.com/DougTrajano/ds_airbnb_rio/blob/master/images/airbnb_data.jpg)

Projeto de Data Science com base nos dados do Airbnb (Rio de Janeiro).

O objetivo deste estudo é desenvolver um modelo capaz de atuar em um dos tópicos abaixo:

- Previsão do preço da estadia (*feature* ‘price’);
- **Classificação do room type (*feature* ‘room_type’);**
- Segmentação dos principais assuntos das reviews (*feature* review_scores_rating’).

# Problema escolhido

Foi escolhido desenvolver um classificador capaz de predizer o **room_type** dos anúncios.

# Estratégia de modelagem
> Como foi a definição da sua estratégia de modelagem?

A estratégia escolhida foi converter as features categoricas em numéricas, isso devido a riqueza de informação que a feature `amenities` possui. Para cada feature, uma função interna foi criada, com o objetivo de tratar a peculiaridade de cada uma. Também criamos uma função `processing` que agrupa o tratamento de todas as features.

Todas as funções estão no arquivo: `processing.script.py`

# Definição da função de custo
> Como foi definida a função de custo utilizada?

No algoritmo `Random Forest` foi avaliado dois critérios de construção da árvore, são eles: "gini" e "entropy".

Na avaliação dos hyperparâmetros através do GridSearchCV foi identificado que o critério: `gini` entende melhor os dados e fornece uma acuracidade melhor.

# Critério para seleção do modelo final
> Qual foi o critério utilizado na seleção do modelo final?

A seleção dos modelos ficou em `Logistic Regression` e `Random Forest`, o modelo gerado pelo algoritmo `Random Forest` apresentou um resultado significamente melhor se comparado com o `Logistic Regression.

# Critério utilizado para validação do modelo
> Qual foi o critério utilizado para validação do modelo?
> Por que escolheu utilizar este método?

Para validar o modelo foi utilizado a técnica de validação cruzada em 5 partes. Segue abaixo os resultados obtidos:

Logistic Regression
- Accuracy (cross-validation): 0.88 (+/- 0.08)

Random Forest
- Accuracy (cross-validation): 0.97 (+/- 0.01)

# Evidências de que o modelo é suficientemente bom
> Quais evidências você possui de que seu modelo é suficientemente bom?

O modelo apresentou um bom resultado no conjunto de métricas, conforme é possível ver abaixo, porém, acredito que seria necessário obter um equilíbrio melhor das classes antes de colocá-lo em produção. As classes `Shared room` e `Hotel room` representam juntas, 3% do dataset. Um valor insignificante se comparado com a classe `Private room` que possui 71% do dataset.

**Random Forest - Classification report**

![](https://github.com/DougTrajano/ds_airbnb_rio/blob/master/images/classification_report.png)

---

*Tempo gasto no desenvolvimento deste projeto: 12h30*
