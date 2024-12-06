import json
from venv import logger
from confluent_kafka import Producer

from app.adapter.output.messaging.models.content_save_message import ContentSaveMessage
from app.adapter.output.messaging.models.line_component import LineComponent
from app.port.output.message_producer import MessageProducer
from typing import List


class KafkaMessageProducer(MessageProducer):
    def __init__(self, bootstrap_servers: str = "localhost:29092"):
        self.producer = Producer(
            {
                "bootstrap.servers": bootstrap_servers,
                "client.id": "python-producer",
                "acks": "all",
            }
        )
        logger.info("Confluent Kafka producer initialized")

    def delivery_report(self, err, msg):
        if err is not None:
            logger.error(f"Message delivery failed: {err}")
        else:
            logger.info(
                f"Message delivered to {msg.topic()} [{msg.partition()}] at offset {msg.offset()}"
            )

    async def send_content_save_message(
        self, topic: str, content: List[LineComponent]
    ) -> bool:
        try:
            # JSON 직렬화
            save_message = ContentSaveMessage(
                lines=content, conversationId="ed3cecf8-f99f-415a-957d-377fda4c4748"
            )
            message_json = json.dumps(save_message.model_dump())

            # 비동기로 메시지 전송
            self.producer.produce(
                topic, value=message_json.encode("utf-8"), callback=self.delivery_report
            )

            # 메시지 즉시 전송
            self.producer.flush()
            return True

        except Exception as e:
            logger.error(f"Error sending message: {str(e)}")
            return False

    async def close(self):
        try:
            self.producer.flush()
            logger.info("Producer closed successfully")
        except Exception as e:
            logger.error(f"Error closing producer: {str(e)}")
