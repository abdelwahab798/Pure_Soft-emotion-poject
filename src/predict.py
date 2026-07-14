import torch
import logging
from fastapi import HTTPException,status
from app.schema import Response , Request,class_Names
import torch.nn.functional as F




def predict_text(request:Request,tokenizer,model):
    if not request.text.strip():
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT,
                            detail="we can't accpeted empty text")
    
    try:
        input=tokenizer(
            request.text,
            return_tensors="pt",
            truncation=True
        )

        with torch.no_grad():
            output=model(**input)
            proba=F.softmax(output.logits,dim=1)
            chosen_class_index=proba.argmax(dim=1).item()
            confidence=proba[0][chosen_class_index].item()
            predict_str=class_Names[chosen_class_index]
            
        return Response(
            text=request.text,
            Predict=predict_str,
            confidence=confidence
        )
    
    except Exception as e:
        logging.error("we have error in (predict)",e)



        