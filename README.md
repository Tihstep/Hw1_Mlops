# Hw1_Mlops

Train Request
curl -X POST "http://localhost:8000/train" \
    -H "Content-Type: application/json" \
    -d '{
          "model_type": "logistic_regression",
          "hyperparameters": {
              "max_iter": 100,
              "solver": "lbfgs"
          },
          "data": {
              "train_data": [[1, 2], [3, 4], [5, 6]],
              "target": [3, 5, 11]
          }
        }'

Predict Request
curl -X POST "http://localhost:8000/predict" \
    -H "Content-Type: application/json" \
    -d '{
          "model_id": "8611571829736123904",
          "data": [[1, 2], [3, 4], [5, 6]]
        }'

Delete Request
curl -X DELETE "http://localhost:8000/delete" \
    -H "Content-Type: application/json" \
    -d '{
          "model_id": "8611571829736123904"
        }'

Healthcheck Request
curl -X GET "http://localhost:8000/status"

Listing Request
curl -X GET "http://localhost:8000/models"