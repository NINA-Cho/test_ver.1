---
name: make-ppt
version: 1.0.0
description: |
  주제나 내용을 입력받아 발표용 PPT(.pptx)를 자동으로 생성합니다.
  레퍼런스 이미지를 제공하면 해당 디자인 스타일(색상, 레이아웃, 폰트 비율)을 분석해 적용합니다.
  한국어 기반. PPT 만들어줘, 발표자료 만들어줘, 슬라이드 만들어줘 등의 요청에 사용.
voice-triggers:
  - PPT 만들어줘
  - 발표자료 만들어줘
  - 슬라이드 만들어줘
  - 프레젠테이션 만들어줘
triggers:
  - ppt 생성
  - 발표자료 생성
  - 슬라이드 생성
  - make ppt
allowed-tools:
  - Bash
  - Read
  - AskUserQuestion
---

# make-ppt: PPT 자동화 에이전트

주제 또는 내용을 받아서 발표용 .pptx 파일을 자동 생성합니다.
레퍼런스 이미지(로컬 파일 경로)를 주면 그 이미지의 디자인을 분석해서 적용합니다.

## 시작 전 체크

```bash
cd make-ppt/src
pip install -r requirements.txt
export ANTHROPIC_API_KEY="your-api-key"
```

## 사용 패턴

### A. 주제로 자동 생성
```bash
python main.py --topic "2025년 AI 트렌드" --slides 12 --output ~/Desktop/ai_trend.pptx
```

### B. 내용 파일로 생성
```bash
python main.py --content ./my_content.md --slides 10 --output ~/Desktop/result.pptx
```

### C. 레퍼런스 이미지 + 주제
```bash
python main.py --topic "회사 소개" --ref ~/Desktop/reference.png --slides 10 --output ~/Desktop/company.pptx
```

### D. 레퍼런스 이미지 + 내용 파일
```bash
python main.py --content ./content.md --ref ~/Desktop/style_ref.jpg --slides 15 --output ~/Desktop/result.pptx
```

### 미리보기 (파일 생성 없이 구성 확인)
```bash
python main.py --topic "주제" --slides 10 --preview
```

## Claude가 따라야 할 워크플로우

### 1단계: 정보 수집

다음 정보를 확인하세요 (없는 것만 물어보세요):

```
1 입력 방식
   - 주제만 줄게 → --topic 사용
   - 내용을 직접 줄게 → --content 사용 (파일 경로 받기)

2 레퍼런스 이미지 (선택)
   - 있으면 로컬 파일 경로를 받으세요 (예: ~/Desktop/ref.png)
   - 없으면 기본 스타일로 진행

3 슬라이드 수 (선택, 기본 10장)

4 저장 위치 (선택, 기본 /tmp/)
```

### 2단계: 미리보기로 구성 확인

```bash
python main.py --topic "..." --slides N --preview
```

결과를 사용자에게 보여주고 OK인지 확인하세요.
수정 요청이 있으면 반영해서 다시 미리보기를 보여주세요.

### 3단계: 파일 생성

OK가 나오면:
```bash
python main.py --topic "..." --ref 이미지경로 --slides N --output 출력경로.pptx
```

### 4단계: 결과 전달

- 파일 경로 알려주기
- 슬라이드 수, 적용된 디자인 스펙 요약

## 사용자 첫 안내 문구

```
PPT를 만들어드릴게요! 몇 가지 확인할게요:

1. 입력 방식: 주제를 알려주시면 내용을 자동 생성하거나,
   직접 작성한 내용을 .txt / .md 파일로 주셔도 됩니다.
2. 레퍼런스 이미지: 참고할 디자인 이미지가 있으면
   로컬 파일 경로를 알려주세요. (없으면 기본 스타일 적용)
3. 슬라이드 수: 몇 장으로 만들까요? (기본 10장)
4. 저장 위치: 어디에 저장할까요? (기본 /tmp/)
```

## 오류 처리

| 오류 | 해결 방법 |
|------|-----------|
| ModuleNotFoundError: pptx | pip install python-pptx |
| ANTHROPIC_API_KEY not set | 환경변수 설정 확인 |
| 이미지 파일 없음 | 경로 확인 후 재요청 |
| JSON 파싱 오류 | 자동 재시도 |

## 출력 계약

```
stdout: /tmp/파일명.pptx
stderr: 진행 상황 메시지
종료 코드: 0 성공 / 1 인수 오류 / 2 생성 오류
```
