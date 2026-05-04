"""슬라이드 내용 생성 모듈 - 주제 또는 원문에서 슬라이드 구조를 생성."""
import json
import anthropic


def generate_content(
    topic: str = None,
    content: str = None,
    slide_count: int = 10,
    language: str = "ko",
) -> dict:
    """topic 또는 content 중 하나를 받아 슬라이드 JSON 구조를 반환."""
    client = anthropic.Anthropic()
    lang_label = "한국어" if language == "ko" else "영어"

    if topic:
        prompt = (
            f"주제: {topic}\n"
            f"슬라이드 수: {slide_count}장\n"
            f"언어: {lang_label}\n\n"
            "위 주제로 발표용 PPT 슬라이드 구성을 JSON 형식으로 만들어주세요.\n"
            "- 첫 번째 슬라이드는 type: title\n"
            "- 마지막 슬라이드는 type: closing\n"
            "- 중간 섹션 구분은 type: section\n"
            "- 나머지는 type: content\n"
            "- 각 content 슬라이드의 bullet은 3~5개\n"
            "- 반드시 JSON만 출력 (설명 없이)\n\n"
            "{\n"
            '  "title": "발표 제목",\n'
            '  "slides": [\n'
            '    {\n'
            '      "type": "title",\n'
            '      "title": "슬라이드 제목",\n'
            '      "content": ["부제목 또는 설명"],\n'
            '      "notes": ""\n'
            '    }\n'
            '  ]\n'
            '}'
        )
    else:
        prompt = (
            "다음 내용을 발표용 PPT 슬라이드로 구성해주세요.\n\n"
            f"--- 내용 시작 ---\n{content}\n--- 내용 끝 ---\n\n"
            f"슬라이드 수: {slide_count}장\n"
            f"언어: {lang_label}\n\n"
            "- 첫 번째 슬라이드는 type: title\n"
            "- 마지막 슬라이드는 type: closing\n"
            "- 중간 섹션 구분은 type: section\n"
            "- 나머지는 type: content\n"
            "- 각 content 슬라이드의 bullet은 3~5개\n"
            "- 반드시 JSON만 출력 (설명 없이)\n\n"
            "{\n"
            '  "title": "발표 제목",\n'
            '  "slides": [\n'
            '    {\n'
            '      "type": "title",\n'
            '      "title": "슬라이드 제목",\n'
            '      "content": ["부제목 또는 설명"],\n'
            '      "notes": ""\n'
            '    }\n'
            '  ]\n'
            '}'
        )

    message = client.messages.create(
        model="claude-opus-4-7",
        max_tokens=4096,
        messages=[{"role": "user", "content": prompt}],
    )

    response_text = message.content[0].text
    start = response_text.find("{")
    end = response_text.rfind("}") + 1
    return json.loads(response_text[start:end])
