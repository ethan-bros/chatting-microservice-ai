from port.input.chat_use_case import ChatUseCase

class ChatService(ChatUseCase):
    
    async def recommend(input: str) -> str:
        print("채팅 추천 로직")
        return ''