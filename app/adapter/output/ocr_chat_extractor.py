import cv2
import numpy as np
import easyocr
import re
from difflib import get_close_matches

from app.port.output.chat_extractor import ChatExtractor


class OCRChatExtractor(ChatExtractor):
    def __init__(self):
        self.reader = easyocr.Reader(["ko", "en"])
        self.common_chat_words = [
            "ㅋㅋ",
            "ㅎㅎ",
            "어어",
            "음",
            "아",
            "오",
            "네",
            "응",
            "야",
            "뭐해",
            "안녕",
        ]

    def preprocess_image(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        denoised = cv2.fastNlMeansDenoising(gray, h=10)
        # 대비 향상
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        enhanced = clahe.apply(denoised)
        return enhanced

    def detect_speech_bubbles(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        closed = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)
        contours, _ = cv2.findContours(
            closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )

        bubbles = []
        for contour in contours:
            if cv2.contourArea(contour) > 1000:
                x, y, w, h = cv2.boundingRect(contour)
                bubbles.append((x, y, w, h))

        return bubbles

    def extract_text(self, image, bubble):
        x, y, w, h = bubble
        roi = image[y : y + h, x : x + w]
        preprocessed = self.preprocess_image(roi)
        # 이미지 크기 확대
        scaled = cv2.resize(
            preprocessed, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC
        )
        result = self.reader.readtext(scaled)
        text = " ".join([item[1] for item in result])
        return self.postprocess_text(text)

    def postprocess_text(self, text):
        # 특수문자 처리 (일부 특수문자 유지)
        text = re.sub(r"[^\w\s가-힣ㄱ-ㅎㅏ-ㅣ!?.,]", "", text)
        # 자음/모음 연속 처리
        text = re.sub(r"([ㄱ-ㅎㅏ-ㅣ])\1+", r"\1", text)
        # 반복되는 문자 처리 (한글 완성형 문자 제외)
        text = re.sub(r"([^가-힣])\1{2,}", r"\1\1", text)
        # 'ㅋ', 'ㅎ' 등의 반복 처리 (최대 3번까지 허용)
        text = re.sub(r"(ㅋ|ㅎ)\1{3,}", r"\1\1\1", text)
        # 띄어쓰기 정규화
        text = re.sub(r"\s+", " ", text)
        text = text.strip()
        return self.correct_common_mistakes(text)

    def correct_common_mistakes(self, text):
        words = text.split()
        corrected_words = []
        for word in words:
            matches = get_close_matches(word, self.common_chat_words, n=1, cutoff=0.6)
            if matches:
                corrected_words.append(matches[0])
            else:
                corrected_words.append(word)
        return " ".join(corrected_words)

    def is_valid_text(self, text):
        if len(text) < 2:
            return False
        if re.match(r"^[a-zA-Z0-9]+$", text):
            return len(text) > 3
        return True

    def determine_speaker(self, x, w, img_width):
        bubble_center = x + w / 2
        if bubble_center > img_width * 0.6:
            return "나"
        elif bubble_center < img_width * 0.4:
            return "상대방"
        else:
            return "나" if x + w > img_width / 2 else "상대방"

    def extract_from(self, image: bytes):
        nparr = np.frombuffer(image, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        bubbles = self.detect_speech_bubbles(img)

        chat_log = []
        for i, bubble in enumerate(bubbles):
            x, y, w, h = bubble
            text = self.extract_text(img, bubble)
            if text and self.is_valid_text(text):
                speaker = self.determine_speaker(x, w, img.shape[1])
                chat_log.append({"order": i + 1, "speaker": speaker, "content": text})

        # y 좌표로 정렬하되, 같은 y 좌표일 경우 x 좌표로 정렬
        chat_log.sort(
            key=lambda x: (bubbles[x["order"] - 1][1], bubbles[x["order"] - 1][0])
        )

        # order 재할당
        for i, chat in enumerate(chat_log):
            chat["order"] = i + 1

        return chat_log
