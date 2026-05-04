"""레퍼런스 이미지 분석 모듈 - Claude 비전으로 디자인 스펙 추출."""
import base64
import json
from pathlib import Path
import anthropic

MEDIA_TYPE_MAP = {
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".png": "image/png",
    ".gif": "image/gif",
    ".webp": "image/webp",
}

ANALYSIS_PROMPT = (
    "이 PPT 슬라이드 이미지를 분석해서 디자인 속성을 추출해주세요.\n\n"
    "분석 항목:\n"
    "- 배경 색상 (RGB 헥스 코드)\n"
    "- 주요 강조색 (포인트 컬러)\n"
    "- 보조색\n"
    "- 제목 텍스트 색상\n"
    "- 본문 텍스트 색상\n"
    "- 레이아웃 타입: centered / left-aligned / two-column / image-right / image-left / full-image 중 하나\n"
    "- 제목 위치: top / center / bottom 중 하나\n"
    "- 폰트 크기 비율 (제목:본문, 예: 2.5:1)\n"
    "- 디자인 스타일: minimal / bold / corporate / creative / dark / light 중 하나\n"
    "- 특이사항\n\n"
    "반드시 JSON만 출력하세요 (설명 없이):\n"
    "{\n"
    '  "background_color": "#FFFFFF",\n'
    '  "accent_color": "#0066CC",\n'
    '  "secondary_color": "#F0F0F0",\n'
    '  "title_color": "#1A1A1A",\n'
    '  "body_color": "#333333",\n'
    '  "layout_type": "left-aligned",\n'
    '  "title_position": "top",\n'
    '  "font_ratio": "2.5:1",\n'
    '  "style": "corporate",\n'
    '  "notes": ""\n'
    '}'
)


def analyze_layout(image_path: str) -> dict:
    """로컬 이미지 파일을 읽어 디자인 스펙 dict를 반환."""
    client = anthropic.Anthropic()
    path = Path(image_path).expanduser().resolve()

    if not path.exists():
        raise FileNotFoundError(f"이미지 파일을 찾을 수 없습니다: {path}")

    media_type = MEDIA_TYPE_MAP.get(path.suffix.lower(), "image/png")
    image_data = base64.standard_b64encode(path.read_bytes()).decode("utf-8")

    message = client.messages.create(
        model="claude-opus-4-7",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": media_type,
                            "data": image_data,
                        },
                    },
                    {"type": "text", "text": ANALYSIS_PROMPT},
                ],
            }
        ],
    )

    response_text = message.content[0].text
    start = response_text.find("{")
    end = response_text.rfind("}") + 1
    return json.loads(response_text[start:end])
