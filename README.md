# eta-prediction-last-mile

## Português

`eta-prediction-last-mile` é um projeto de previsão de tempo de entrega para a última milha, inspirado em uma pergunta comum de entrevista da DoorDash: **como prever ETA com sinais operacionais e de demanda**.

O projeto compara dois modelos:

- `LinearRegression`
- `RandomForestRegressor`

## Objetivo analítico

O foco aqui é prever `ETA` com um baseline forte e interpretável antes de pensar em modelos mais sofisticados.

Em entrevistas de marketplace, isso é importante porque mostra:

- entendimento dos principais drivers de atraso;
- capacidade de construir benchmark simples;
- leitura correta de erro médio e erro extremo.

## O que o projeto faz

1. gera uma base sintética de entregas;
2. cria features operacionais de ETA;
3. separa treino e teste;
4. compara modelos de regressão;
5. mede erro com:
   - `MAE`
   - `RMSE`
   - `P90 absolute error`

## Features utilizadas

- `distance_km`
- `prep_time_min`
- `courier_wait_min`
- `peak_hour`
- `rainy_weather`
- `stacked_order`

Papel das features:

- `distance_km`
  - proxy principal de deslocamento
- `prep_time_min`
  - tempo de preparação do merchant
- `courier_wait_min`
  - fricção entre chegada do entregador e retirada
- `peak_hour`
  - pressão de demanda
- `rainy_weather`
  - dificuldade operacional
- `stacked_order`
  - efeito de batching sobre ETA

## Técnicas e bibliotecas

- regressão supervisionada
- benchmark entre modelos
- `scikit-learn`
- `csv`
- `json`
- `pathlib`
- `unittest`

## Métricas de avaliação

- `MAE`
- `RMSE`
- `P90 absolute error`

O `P90` é especialmente importante em marketplace porque o usuário sente muito mais os erros de cauda do que a média sozinha.

## Resultados atuais

- `best_model = linear_regression`
- `best_model_mae = 1.1816`
- `best_model_rmse = 1.393`
- `best_model_p90_abs_error = 2.2674`

## Contrato do relatório

O artefato [eta_prediction_report.json](/Users/flaviagaia/Documents/CV_FLAVIA_CODEX/eta-prediction-last-mile/data/processed/eta_prediction_report.json) guarda:

- tamanho de treino e teste
- métricas da baseline linear
- métricas do modelo candidato
- melhor modelo final
- métricas finais usadas para decisão

## Como executar

```bash
python3 main.py
python3 -m unittest discover -s tests -v
python3 -m py_compile main.py src/data_factory.py src/modeling.py tests/test_project.py
```

## Como defender em entrevista

> Para ETA, eu começaria com um benchmark simples e forte, usando distância, tempo de preparo, espera do entregador e contexto operacional. Depois compararia modelos por MAE e P90 error, porque não basta acertar em média: em marketplace, os atrasos extremos também importam.
