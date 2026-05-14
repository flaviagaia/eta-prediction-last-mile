# eta-prediction-last-mile

## Português

### Visão geral

`eta-prediction-last-mile` é um projeto de previsão de tempo de entrega para última milha focado em estimar ETA usando sinais operacionais e de demanda.

O projeto compara dois modelos:

- `LinearRegression`
- `RandomForestRegressor`

### Objetivo analítico

O foco é construir um baseline forte e interpretável antes de pensar em modelos mais sofisticados.

Isso mostra:

- entendimento dos drivers de atraso;
- capacidade de benchmark simples;
- leitura correta de erro médio e erro extremo.

### Features utilizadas

- `distance_km`
- `prep_time_min`
- `courier_wait_min`
- `peak_hour`
- `rainy_weather`
- `stacked_order`

Papel das features:

- `distance_km`
  - deslocamento
- `prep_time_min`
  - tempo de preparo do merchant
- `courier_wait_min`
  - fricção entre chegada e retirada
- `peak_hour`
  - pressão operacional
- `rainy_weather`
  - dificuldade de execução
- `stacked_order`
  - efeito de batching

### Métricas de avaliação

- `MAE`
- `RMSE`
- `P90 absolute error`

O `P90` é importante porque o usuário sente os atrasos de cauda com muito mais intensidade do que a média sozinha.

### Técnicas e bibliotecas

- regressão supervisionada
- benchmark entre modelos
- `scikit-learn`
- `csv`
- `json`
- `pathlib`
- `unittest`

### Contrato do relatório

O artefato [eta_prediction_report.json](data/processed/eta_prediction_report.json) guarda:

- tamanho de treino e teste
- métricas da baseline linear
- métricas do modelo candidato
- melhor modelo final
- métricas finais usadas na decisão

### Resultados atuais

- `best_model = linear_regression`
- `best_model_mae = 1.1816`
- `best_model_rmse = 1.393`
- `best_model_p90_abs_error = 2.2674`

### Arquivos principais

- [main.py](main.py)
- [src/data_factory.py](src/data_factory.py)
- [src/modeling.py](src/modeling.py)
- [tests/test_project.py](tests/test_project.py)

### Como executar

```bash
python3 main.py
python3 -m unittest discover -s tests -v
python3 -m py_compile main.py src/data_factory.py src/modeling.py tests/test_project.py
```


## English

### Overview

`eta-prediction-last-mile` is a last-mile ETA prediction project focused on estimating delivery ETA using operational and demand signals.

The project compares two models:

- `LinearRegression`
- `RandomForestRegressor`

### Analytical objective

The focus is to build a strong and interpretable baseline before moving to more sophisticated models.

This shows:

- understanding of delay drivers;
- ability to build a simple benchmark;
- correct reading of average and tail error.

### Features used

- `distance_km`
- `prep_time_min`
- `courier_wait_min`
- `peak_hour`
- `rainy_weather`
- `stacked_order`

### Evaluation metrics

- `MAE`
- `RMSE`
- `P90 absolute error`

`P90` matters because users feel tail delays much more strongly than average error alone.

### Techniques and libraries

- supervised regression
- model benchmarking
- `scikit-learn`
- `csv`
- `json`
- `pathlib`
- `unittest`

### Report contract

The artifact [eta_prediction_report.json](data/processed/eta_prediction_report.json) stores:

- train/test size
- linear baseline metrics
- candidate model metrics
- best final model
- final decision metrics

### Current results

- `best_model = linear_regression`
- `best_model_mae = 1.1816`
- `best_model_rmse = 1.393`
- `best_model_p90_abs_error = 2.2674`

### Main files

- [main.py](main.py)
- [src/data_factory.py](src/data_factory.py)
- [src/modeling.py](src/modeling.py)
- [tests/test_project.py](tests/test_project.py)

### How to run

```bash
python3 main.py
python3 -m unittest discover -s tests -v
python3 -m py_compile main.py src/data_factory.py src/modeling.py tests/test_project.py
```
