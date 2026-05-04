#!/usr/bin/env python3
"""
make-ppt 엔트리포인트.

사용법:
  python main.py --topic "주제" [--ref 이미지경로] [--slides N] [--output 경로.pptx]
  python main.py --content 내용파일.md [--ref 이미지경로] [--slides N] [--output 경로.pptx]
  python main.py --topic "주제" --preview
"""
import argparse
import json
import sys
from pathlib import Path

from content_generator import generate_content
from layout_analyzer import analyze_layout
from ppt_generator import create_ppt


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="PPT 자동화 에이전트")
    p.add_argument("--topic", help="발표 주제")
    p.add_argument("--content", help="내용 파일 경로 (.txt 또는 .md)")
    p.add_argument("--ref", help="레퍼런스 이미지 로컬 경로")
    p.add_argument("--slides", type=int, default=10, help="슬라이드 수 (기본: 10)")
    p.add_argument("--output", help="출력 .pptx 파일 경로")
    p.add_argument("--preview", action="store_true", help="미리보기")
    p.add_argument("--lang", default="ko", choices=["ko", "en"])
    return p


def print_preview(slide_data: dict) -> None:
    print(f"\n{'=' * 50}")
    print(f"제목: {slide_data.get('title', '')}")
    print(f"{'=' * 50}\n")
    for i, slide in enumerate(slide_data.get("slides", []), 1):
        print(f"[{i}] {slide.get('title', '')}  ({slide.get('type', 'content')})")
        for bullet in slide.get("content", []):
            print(f"    • {bullet}")
        print()


def main() -> None:
    args = build_parser().parse_args()

    if not args.topic and not args.content:
        print("오류: --topic 또는 --content 중 하나는 필요합니다.", file=sys.stderr)
        sys.exit(1)

    print("슬라이드 내용 생성 중...", file=sys.stderr)
    if args.topic:
        slide_data = generate_content(topic=args.topic, slide_count=args.slides, language=args.lang)
    else:
        content_text = Path(args.content).expanduser().read_text(encoding="utf-8")
        slide_data = generate_content(content=content_text, slide_count=args.slides, language=args.lang)

    if args.preview:
        print_preview(slide_data)
        sys.exit(0)

    design_spec = None
    if args.ref:
        print(f"레퍼런스 이미지 분석 중: {args.ref}", file=sys.stderr)
        design_spec = analyze_layout(args.ref)
        print(f"디자인 스펙:\n{json.dumps(design_spec, ensure_ascii=False, indent=2)}", file=sys.stderr)

    print("PPT 파일 생성 중...", file=sys.stderr)
    output_path = create_ppt(slide_data, design_spec=design_spec, output_path=args.output)

    print(f"완료! 슬라이드 {len(slide_data.get('slides', []))}장", file=sys.stderr)
    print(output_path)


if __name__ == "__main__":
    main()
