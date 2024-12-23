import streamlit as st
import requests

st.title("ML Model Dashboard")

action = st.sidebar.selectbox("Select action", ["token", "train", "predict", "list", "delete", "healthcheck"])

if action == "token":
    username = st.text_input("Enter username", placeholder="vertica")
    password = st.text_input("Enter password", placeholder="vertica")

    if st.button("Get Token"):
        response = requests.post("http://localhost:8000/token", json={
            "username": username,
            "password": password
        })
        st.write(response.json())
    


if action == "train":
    model_type = st.selectbox("Select model type", ["logistic_regression", "random_forest"], index=None,
    placeholder="Choose or lose...")
    hyperparameters = st.text_input("Enter hyperparameters (JSON format)", placeholder="{...}")
    data = st.text_input("Enter data", placeholder="'target' : [...], 'train_data' : [[...]]")
    token = st.text_input("Enter your access token", placeholder="Bearer token")

    if st.button("Train Model"):
        headers = {
                    "Authorization": f"Bearer {token}"
                }
        response = requests.post("http://localhost:8000/train", json={
            "model_type": model_type,
            "hyperparameters": eval(hyperparameters),
            "data": eval(data)
        }, headers=headers)
        st.write(response.json())

if action == "predict":
    models = requests.get("http://localhost:8000/models").json()
    model_id = st.selectbox("Select model type", models,  index=None,
    placeholder="Choose or lose...")
    data = st.text_input("Enter data", placeholder="{[[...]]}")
    token = st.text_input("Enter your access token", placeholder="Bearer token")

    if st.button("Predict"):
        headers = {
                    "Authorization": f"Bearer {token}"
                }
        response = requests.post("http://localhost:8000/predict", json={
            "model_id": str(model_id),
            "data": eval(data)
        }, headers=headers)
        st.write(response.json())


if action == "delete":
    models = requests.get("http://localhost:8000/models").json()
    model_id = st.selectbox("Select model type", models)
    token = st.text_input("Enter your access token", placeholder="Bearer token")


    if st.button("Delete model"):
        headers = {
                    "Authorization": f"Bearer {token}"
            }
        response = requests.delete("http://localhost:8000/delete", json={
            "model_id": model_id
        }, headers=headers)
        st.write(response.json())

if action == "list":
    response = requests.get("http://localhost:8000/models")
    st.write(response.json())

if action == "healthcheck":
    st.write(requests.get("http://localhost:8000/status").json())

