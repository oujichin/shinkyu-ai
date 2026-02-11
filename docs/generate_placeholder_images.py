#!/usr/bin/env python3
"""
美しいプレースホルダー画像をSVG形式で生成するスクリプト
依存ライブラリ不要
"""

from pathlib import Path

# 画像保存先ディレクトリ
IMAGES_DIR = Path(__file__).parent / "images"
IMAGES_DIR.mkdir(exist_ok=True)

# 画像定義
IMAGES = [
    {"filename": "hero-bg.jpg", "width": 1920, "height": 1080, "gradient": ["#2C5F8D", "#1a4564"], "text": "Hero Background", "icon": "🏥"},
    {"filename": "problem-therapist.jpg", "width": 1200, "height": 800, "gradient": ["#666", "#999"], "text": "Problem Therapist", "icon": "😔"},
    {"filename": "profile-toyoda.jpg", "width": 800, "height": 800, "gradient": ["#2C5F8D", "#4A90E2"], "text": "Toyoda Profile", "icon": "👨‍⚕️"},
    {"filename": "story-sunset.jpg", "width": 1200, "height": 800, "gradient": ["#E59B3C", "#D4A574"], "text": "Story Sunset", "icon": "🌅"},
    {"filename": "5-layers-diagram.jpg", "width": 1000, "height": 800, "gradient": ["#2C5F8D", "#E59B3C"], "text": "5 Layers Diagram", "icon": "📊"},
    {"filename": "mind-flow-diagram.jpg", "width": 1000, "height": 600, "gradient": ["#4A90E2", "#2C5F8D"], "text": "Mind Flow", "icon": "→"},
    {"filename": "counseling-illustration.jpg", "width": 1000, "height": 800, "gradient": ["#D4A574", "#E59B3C"], "text": "Counseling", "icon": "💬"},
    {"filename": "before-after-comparison.jpg", "width": 1200, "height": 600, "gradient": ["#666", "#4A90E2"], "text": "Before/After", "icon": "⚡"},
    {"filename": "case1-stage1.jpg", "width": 800, "height": 600, "gradient": ["#E59B3C", "#F0A040"], "text": "Case 1 - Stage 1", "icon": "😊"},
    {"filename": "case1-stage2.jpg", "width": 800, "height": 600, "gradient": ["#666", "#888"], "text": "Case 1 - Stage 2", "icon": "🌧️"},
    {"filename": "case1-stage3.jpg", "width": 800, "height": 600, "gradient": ["#888", "#4A90E2"], "text": "Case 1 - Stage 3", "icon": "😢"},
    {"filename": "case1-stage4.jpg", "width": 800, "height": 600, "gradient": ["#4A90E2", "#D4A574"], "text": "Case 1 - Stage 4", "icon": "💫"},
    {"filename": "case1-stage5.jpg", "width": 800, "height": 600, "gradient": ["#D4A574", "#FFD700"], "text": "Case 1 - Stage 5", "icon": "🌟"},
    {"filename": "case2-symptoms.jpg", "width": 800, "height": 600, "gradient": ["#8B4513", "#A0522D"], "text": "Case 2 - Symptoms", "icon": "😰"},
    {"filename": "case2-assessment.jpg", "width": 800, "height": 600, "gradient": ["#2C5F8D", "#4A90E2"], "text": "Case 2 - Assessment", "icon": "🔍"},
    {"filename": "case2-future.jpg", "width": 800, "height": 600, "gradient": ["#4A90E2", "#87CEEB"], "text": "Case 2 - Future", "icon": "✨"},
    {"filename": "course-materials.jpg", "width": 1200, "height": 800, "gradient": ["#F8F9FA", "#E8EAED"], "text": "Course Materials", "icon": "📚"},
    {"filename": "online-learning.jpg", "width": 1200, "height": 800, "gradient": ["#4A90E2", "#2C5F8D"], "text": "Online Learning", "icon": "💻"},
    {"filename": "diverse-therapists.jpg", "width": 1200, "height": 600, "gradient": ["#2C5F8D", "#4A90E2"], "text": "Diverse Therapists", "icon": "👥"},
    {"filename": "toyoda-message.jpg", "width": 800, "height": 1000, "gradient": ["#2C5F8D", "#1a4564"], "text": "Toyoda Message", "icon": "💭"},
    {"filename": "therapist-patient-handshake.jpg", "width": 1200, "height": 800, "gradient": ["#D4A574", "#E59B3C"], "text": "Handshake", "icon": "🤝"},
    {"filename": "bright-future.jpg", "width": 1200, "height": 800, "gradient": ["#FFD700", "#FFA500"], "text": "Bright Future", "icon": "🌞"},
    {"filename": "final-message-bg.jpg", "width": 1920, "height": 1080, "gradient": ["#2C5F8D", "#1a4564"], "text": "Final Message", "icon": "🎯"},
]


def generate_svg_placeholder(image_data):
    """
    SVGプレースホルダーを生成
    """
    filename = image_data["filename"]
    width = image_data["width"]
    height = image_data["height"]
    gradient = image_data["gradient"]
    text = image_data.get("text", "")
    icon = image_data.get("icon", "📷")

    # SVGテンプレート
    svg_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="grad{filename}" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:{gradient[0]};stop-opacity:1" />
      <stop offset="100%" style="stop-color:{gradient[1]};stop-opacity:1" />
    </linearGradient>
  </defs>
  <rect width="{width}" height="{height}" fill="url(#grad{filename})" />
  <text x="{width/2}" y="{height/2 - 20}" font-family="Arial, sans-serif" font-size="48" fill="white" text-anchor="middle" opacity="0.8">
    {icon}
  </text>
  <text x="{width/2}" y="{height/2 + 40}" font-family="Arial, sans-serif" font-size="24" fill="white" text-anchor="middle" opacity="0.6">
    {text}
  </text>
  <text x="{width/2}" y="{height/2 + 70}" font-family="Arial, sans-serif" font-size="16" fill="white" text-anchor="middle" opacity="0.5">
    {width} × {height}
  </text>
</svg>'''

    return svg_content


def main():
    """
    メイン処理
    """
    print("="*80)
    print("SVG Placeholder Generator")
    print(f"Total images to generate: {len(IMAGES)}")
    print(f"Output directory: {IMAGES_DIR}")
    print("="*80)

    success_count = 0

    for i, image_data in enumerate(IMAGES, 1):
        filename = image_data["filename"]
        print(f"\n[{i}/{len(IMAGES)}] Generating: {filename}")

        # SVGファイル名に変更
        svg_filename = filename.replace('.jpg', '.svg')
        output_path = IMAGES_DIR / svg_filename

        # SVG生成
        svg_content = generate_svg_placeholder(image_data)

        # ファイル保存
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(svg_content)

        print(f"✓ Successfully created: {output_path}")
        success_count += 1

    # 結果サマリー
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    print(f"Total: {len(IMAGES)}")
    print(f"Success: {success_count}")
    print("\n✓ All SVG placeholders generated successfully!")
    print("="*80)


if __name__ == "__main__":
    main()
