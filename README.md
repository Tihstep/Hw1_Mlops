## Домашняя работа ML Model API по курсу "Mlops"

Решение подготовил: Тихомиров С.А

Этот проект предоставляет API для управления обучением и использованием машинных моделей . API позволяет обучать модели, делать предсказания, удалять модели и проверять их статус.

### Функционал проекта
Поддержка обучения моделей `Logistic Regression` и `Random Forest` с кастомными гиперпараметрами.

1. **Обучение моделей**

   Ручка `/train` запускает обучение модели на предоставленных данных и возвращает ID обученной модели.

2. **Предсказания**

   Ручка `/predict` позволяет сделать предсказание на данных для конкретной модели по ее ID.

3. **Удаление моделей**

   Ручка `/delete` удаляет модель из системы по ее ID.
   
4. **Список доступных моделей**

   Ручка `/models` возвращает список всех обученных и доступных для использования моделей.

5. **Проверка состояния сервера**

   Ручка `/status` возвращает информацию о состоянии сервера, чтобы удостовериться, что сервер работает корректно.


### Установка и запуск проекта

1. **Склонируйте репозиторий**
   ```bash
   git clone <URL репозитория>
   cd <имя папки репозитория>
   
2. **Установите зависимости**
   ```bash
   pipx install poetry
   poetry install
   
3. **Запуск сервера**
docker-compose up -d

4. **Открытие документации**
Перейдите на http://127.0.0.1:8000/docs для использования Swagger UI, чтобы легко протестировать все эндпоинты API.

Примеры запросов:
- Token Request
```bash
curl -X POST "http://localhost:8000/token" \
    -H "Content-Type: application/json" \
    -d '{"username" : "vertica", "password": "vertica"}'

```
- Train Request
```bash
curl -X POST "http://localhost:8000/train" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer <token>" \
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
        }'
```

- Predict Request
```bash
curl -X POST "http://localhost:8000/predict" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer <token>" \
    -d '{
          "model_id": "<model_od>",
          "data": [[1, 2], [3, 4], [5, 6]]
        }'
```
- Delete Request
```bash
curl -X DELETE "http://localhost:8000/delete" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer <token>" \
    -d '{
          "model_id": "<model_id>"
        }'
```
- Healthcheck Request
```bash
   curl -X GET "http://localhost:8000/status"
```
```bash
- Listing Request
```bash
`curl -X GET "http://localhost:8000/models"
```


##Структура проекта
- fastapi_app
   - `fastapi_app.py`: основной файл приложения FastAPI, в котором определены все эндпоинты API.
   - `model_framework.py`: модуль для управления моделями (обучение, предсказание, удаление, список).
   - `pydantic.py`: модели данных для запросов и ответов, используемые в API.
- grpc_app
   - `grpc_server.py`: основной файл приложения сервера, в котором определена логика обработки запросов grpc.
   - `grpc_client.py`: файл пример использования интерфейса.
   - `message_interface.proto`: protobuf протокол определяющий интерфейс сообщений и методов.
- `dashboard.py`: Файл, формирующий веб-дашборд
- `auth.py`: Файл-аутентификатор

## Альтернативный вариант - grpc.
- Запуск сервера
```bash
   python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. grpc_app/message_interface.proto
```
- Запуск клиента
```bash
   poetry run mlops/grpc_app/grpc_client.py
```


## Запуск дашборда.
```bash
poetry run streamlit run mlops/dashboard.py
```
