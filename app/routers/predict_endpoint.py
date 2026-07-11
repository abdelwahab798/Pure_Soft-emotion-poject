













@app.post("/predict",response_model=Response)
async def predict(request:Request):
    if model is None or tokenizer is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    if not request.text.strip():
        raise HTTPException(status_code=422, detail="Text cannot be empty.")
    try:
        input=tokenizer(
            request.text,
            return_tensors="pt",
            truncation=True
        )

        with torch.no_grad():
            output=model(**input)
            probs=torch.softmax(output.logits,dim=1)
            predict=probs.argmax(dim=1).item()
            confidence = probs[0][predict].item()
            predict_str=class_Names[predict]

        return Response(
                Predict=predict_str,
                confidence=confidence
            )
        
    except Exception as e:
        print("prediction error")
        raise HTTPException(status_code=500, detail=str(e))