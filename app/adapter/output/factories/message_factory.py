import base64
from langchain_core.messages import HumanMessage

from app.adapter.output.dto.image_message_parameter import ImageMessageParameter
from app.adapter.output.dto.message_paremeter import MessageParameter


class MessageFactory:
    @staticmethod
    def get_message(param: MessageParameter) -> HumanMessage:
        if isinstance(param, ImageMessageParameter):
            base64_image = base64.b64encode(param.image).decode('utf-8')
            return HumanMessage(content=[
                    {
                        "type" : "text",
                        "text" : f"{param.question}",
                    },
                    {
                        "type" : "image_url",
                        "image_url" : {
                            "url" : f"data:image/jpeg;base64,{base64_image}",
                            "default" : "auto",
                        }
                    }

                ])
        else:
            return MessageParameter()