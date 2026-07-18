# Pure Soft — Emotion Detection API

A FastAPI backend that classifies the emotion behind a piece of text using a fine-tuned DistilBERT model. It includes user authentication (JWT-based) and stores each prediction's history in a database tied to the requesting user.

## Overview

The service exposes a `/predict` endpoint that takes a text input and returns the predicted emotion along with a confidence score. Access is protected by a signup/login flow, and every prediction made by an authenticated user is logged to the database for history tracking.

## Features

- **Emotion classification** — predicts one of six emotions from input text: `sadness`, `joy`, `love`, `anger`, `fear`, `surprise`
- **User authentication** — signup and login endpoints with hashed passwords (bcrypt) and JWT access tokens
- **Prediction history** — every prediction is linked to the user's email and stored in the database
- **Two training experiments** — a full fine-tune and a LoRA (parameter-efficient) fine-tune of DistilBERT, benchmarked against each other

## Model

The base model is `distilbert-base-uncased`, fine-tuned for sequence classification (6 classes) on the [`dair-ai/emotion`](https://huggingface.co/datasets/dair-ai/emotion) dataset. Two training strategies were tried and compared:

- **Full fine-tuning** — `expierment/exp1.ipynb`, all model weights updated.
- **LoRA fine-tuning** — `expierment/exp_lora.ipynb`, using [PEFT](https://github.com/huggingface/peft) with `LoraConfig(r=16, lora_alpha=32, target_modules=["q_lin", "v_lin"], lora_dropout=0.05)`, only the adapter layers updated.

Both were trained for 3 epochs on the same dataset/split, evaluated with accuracy and weighted F1.

### Results — Full Fine-tuning (no LoRA)

| Epoch | Training Loss | Validation Loss | Accuracy | F1       |
|-------|---------------|------------------|----------|----------|
| 1     | —             | 0.190573         | 0.9275   | 0.928089 |
| 2     | 0.337740      | 0.142789         | 0.9385   | 0.938855 |
| 3     | 0.337740      | 0.127588         | 0.9425   | 0.942536 |

Training time: **~20 minutes**

### Results — LoRA Fine-tuning

| Epoch | Training Loss | Validation Loss | Accuracy | F1       |
|-------|---------------|------------------|----------|----------|
| 1     | 0.601963      | 0.265424         | 0.9035   | 0.904524 |
| 2     | 0.249926      | 0.189673         | 0.9250   | 0.924814 |
| 3     | 0.181751      | 0.168832         | 0.9325   | 0.932647 |

Training time: **~7 minutes**

### Which one is deployed

The **LoRA model** is the one loaded and served by the FastAPI app (`app/main.py`, via `model_url` in `.env`), not the fully fine-tuned model. It trains roughly 3x faster with a modest ~1-point drop in accuracy/F1 compared to full fine-tuning, which made it the more practical choice for this deployment.

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
│   ├── exp1.ipynb                # Full fine-tuning notebook (no LoRA)
│   └── exp_lora.ipynb            # LoRA fine-tuning notebook — model used in production
├── LICENSE
└── README.md
```

## Tech Stack

- **FastAPI** — web framework
- **PyTorch + Transformers (Hugging Face)** — model loading and inference
- **PEFT (LoRA)** — parameter-efficient fine-tuning of the deployed model
- **SQLAlchemy** — ORM, backed by SQLite
- **Pydantic / pydantic-settings** — schema validation and configuration
- **PyJWT** — access token generation and verification
- **bcrypt** — password hashing

## Setup

1. Clone the repository and install dependencies:
   ```bash
   pip install fastapi uvicorn torch transformers peft sqlalchemy pydantic pydantic-settings pyjwt bcrypt python-multipart
   ```

2. Create a `.env` file in the project root with:
   ```
   model_url=<path or Hugging Face repo id of the fine-tuned LoRA model>
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