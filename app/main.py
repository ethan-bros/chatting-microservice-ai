from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, File, Form, HTTPException

from adapter.output.llm_chat_extractor import LLMChatExtractor

load_dotenv()
app = FastAPI()
chat_extractor = LLMChatExtractor()

@app.post("/v1/ai/chat/extract")
async def extract_chat(
    file: UploadFile = File(...),
    partner_info: str = Form(...),
    chat_purpose: str = Form(...)
):
    try:
        contents = await file.read()
        return chat_extractor.extract_from(image=contents)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)