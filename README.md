# eta-prediction-last-mile

## Português

`eta-prediction-last-mile` é um projeto de previsão de tempo de entrega para a última milha, inspirado em uma pergunta comum de entrevista da DoorDash: **como prever ETA com sinais operacionais e de demanda**.

O projeto compara dois modelos:

- `LinearRegression`
- `RandomForestRegressor`

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

## Técnicas e bibliotecas

- regressão supervisionada
- benchmark entre modelos
- `scikit-learn`
- `csv`
- `json`
- `pathlib`
- `unittest`

## Como executar

```bash
python3 main.py
python3 -m unittest discover -s tests -v
python3 -m py_compile main.py src/data_factory.py src/modeling.py tests/test_project.py
```

## Como defender em entrevista

> Para ETA, eu começaria com um benchmark simples e forte, usando distância, tempo de preparo, espera do entregador e contexto operacional. Depois compararia modelos por MAE e P90 error, porque não basta acertar em média: em marketplace, os atrasos extremos também importam.
