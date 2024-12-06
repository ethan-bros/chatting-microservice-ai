import sys
import os
from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, File, HTTPException, Depends


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from app.adapter.output.messaging.producer.kafka_message_producer import (
    KafkaMessageProducer,
)
from app.port.output.message_producer import MessageProducer
from app.adapter.output.ocr_chat_extractor import OCRChatExtractor
from app.adapter.output.llm_chat_extractor import LLMChatExtractor
from app.adapter.output.dto.request.chat_recommend_request import ChatRecommendRequest
from app.adapter.output.llm_chat_analyzer import LLMChatAnalyzer
from app.port.output.chat_analyzer import ChatAnalyzer
from app.port.output.chat_extractor import ChatExtractor

# .env 파일 로드
load_dotenv()

app = FastAPI()


def get_chat_extractor() -> ChatExtractor:
    return LLMChatExtractor()
    # return OCRChatExtractor()


def get_chat_analyzer() -> ChatAnalyzer:
    return LLMChatAnalyzer()


def get_message_producer() -> MessageProducer:
    return KafkaMessageProducer()


@app.post("/v1/ai/chat/recommend")
async def recommend_chat(
    file: UploadFile = File(...),
    chat_extractor: ChatExtractor = Depends(get_chat_extractor),
    # message_producer: MessageProducer = Depends(get_message_producer),
    chat_analyzer: ChatAnalyzer = Depends(get_chat_analyzer),
):
    try:
        image = await file.read()
        contents = chat_extractor.extract_from(image=image)
        # 카프카로 스프링 서버로 부터 받아온다는 가정. 리퀘스트 및 리스폰스 조정 필요
        recom_req = ChatRecommendRequest(
            id="chat01", purpose="친해지기 위함", contents=contents
        )
        return chat_analyzer.recommend_reply_based_on(request=recom_req)

        # await message_producer.send_content_save_message(topic="python-to-kotlin-topic", content=contents)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8100)
