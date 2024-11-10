# Домашняя работа ML Model API по курсу "Mlops"

Решение подготовил: Тихомиров С.А

Этот проект предоставляет API для управления обучением и использованием машинных моделей . API позволяет обучать модели, делать предсказания, удалять модели и проверять их статус.

## Функционал проекта

1. **Обучение моделей**
   - Поддержка обучения моделей `Logistic Regression` и `Random Forest` с кастомными гиперпараметрами.
   - Ручка `/train` запускает обучение модели на предоставленных данных и возвращает ID обученной модели.

2. **Предсказания**
   - Ручка `/predict` позволяет сделать предсказание на данных для конкретной модели по ее ID.

3. **Удаление моделей**
   - Ручка `/delete` удаляет модель из системы по ее ID.

4. **Список доступных моделей**
   - Ручка `/models` возвращает список всех обученных и доступных для использования моделей.

5. **Проверка состояния сервера**
   - Ручка `/status` возвращает информацию о состоянии сервера, чтобы удостовериться, что сервер работает корректно.


## Установка и запуск проекта

1. **Склонируйте репозиторий**
   ```bash
   git clone <URL репозитория>
   cd <имя папки репозитория>
   
2. **Установите зависимости**
   ```bash
   pipx install poetry
   poetry install
   
3. **Запуск сервера FastApi**
uvicorn fastapi_app:app --reload

4. **Открытие документации**
Перейдите на http://127.0.0.1:8000/docs для использования Swagger UI, чтобы легко протестировать все эндпоинты API.

uvicorn api.main:app --reload

- Train Request

`curl -X POST "http://localhost:8000/train" \
    -H "Content-Type: application/json" \
    -d '{
          "model_type": "logistic_regression",
          "hyperparameters": {
              "max_iter": 100,
              "solver": "lbfgs"
          },
          "data": {
              "train_data": [[1, 2], [3, 4], [5, 6]],
              "target": [3, 7, 11]
          }
        }'`

- Predict Request

`curl -X POST "http://localhost:8000/predict" \
    -H "Content-Type: application/json" \
    -d '{
          "model_id": "8611571829736123904",
          "data": [[1, 2], [3, 4], [5, 6]]
        }'`

- Delete Request

`curl -X DELETE "http://localhost:8000/delete" \
    -H "Content-Type: application/json" \
    -d '{
          "model_id": "8611571829736123904"
        }'`

- Healthcheck Request

`curl -X GET "http://localhost:8000/status"`

- Listing Request

`curl -X GET "http://localhost:8000/models"`
