# Pure Soft — Emotion Detection API

A FastAPI backend that classifies the emotion behind a piece of text using a fine-tuned DistilBERT model. It includes user authentication (JWT-based) and stores each prediction's history in a database tied to the requesting user.

## Overview

The service exposes a `/predict` endpoint that takes a text input and returns the predicted emotion along with a confidence score. Access is protected by a signup/login flow, and every prediction made by an authenticated user is logged to the database for history tracking.

## Features

- **Emotion classification** — predicts one of six emotions from input text: `sadness`, `joy`, `love`, `anger`, `fear`, `surprise`
- **User authentication** — signup and login endpoints with hashed passwords (bcrypt) and JWT access tokens
- **Prediction history** — every prediction is linked to the user's email and stored in the database
- **Model training notebook** — includes the full fine-tuning experiment (`expierment/exp1.ipynb`) used to produce the model

## Model

The classification model is a `distilbert-base-uncased` checkpoint fine-tuned on the [`dair-ai/emotion`](https://huggingface.co/datasets/dair-ai/emotion) dataset for sequence classification across six emotion classes. The training pipeline (tokenization, training arguments, and evaluation) is documented in `expierment/exp1.ipynb`.

## Project Structure

```
Pure_Soft-emotion-poject/
├── app/
│   ├── main.py                # FastAPI app entrypoint, loads model/tokenizer at startup
│   ├── schema.py               # Pydantic request/response schemas
│   ├── database/
│   │   ├── config.py           # SQLAlchemy engine/session setup (SQLite)
│   │   └── models.py           # ORM models: Users, Text (predictions)
│   └── routers/
│       ├── model.py            # /predict endpoint
│       └── auth.py             # /sign and /login endpoints
├── src/
│   ├── config.py                # App settings (loaded from .env)
│   ├── predict.py               # Inference logic (tokenize -> model -> softmax)
│   ├── password_token.py        # Password hashing, JWT creation/validation
│   └── user_wrokflow.py         # Signup/login business logic
├── expierment/
│   └── exp1.ipynb               # Model fine-tuning notebook
├── LICENSE
└── README.md
```

## Tech Stack

- **FastAPI** — web framework
- **PyTorch + Transformers (Hugging Face)** — model loading and inference
- **SQLAlchemy** — ORM, backed by SQLite
- **Pydantic / pydantic-settings** — schema validation and configuration
- **PyJWT** — access token generation and verification
- **bcrypt** — password hashing

## Setup

1. Clone the repository and install dependencies:
   ```bash
   pip install fastapi uvicorn torch transformers sqlalchemy pydantic pydantic-settings pyjwt bcrypt python-multipart
   ```

2. Create a `.env` file in the project root with:
   ```
   model_url=<path or Hugging Face repo id of the fine-tuned model>
   SECRET_KEY=<your JWT secret key>
   ```

3. Run the API:
   ```bash
   uvicorn app.main:app --reload
   ```

## API Endpoints

| Method | Endpoint   | Description                                  | Auth required |
|--------|-----------|-----------------------------------------------|----------------|
| POST   | `/sign`   | Register a new user                           | No             |
| POST   | `/login`  | Log in and receive an access token            | No             |
| POST   | `/predict`| Classify the emotion of a given text          | Yes (Bearer token) |

### Example: `/predict`

**Request**
```json
{
  "text": "I can't believe how happy I am today!"
}
```

**Response**
```json
{
  "text": "I can't believe how happy I am today!",
  "Predict": "joy",
  "confidence": 0.98
}
```

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.