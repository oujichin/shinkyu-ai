#!/usr/bin/env python3
"""
Gemini API を使用して画像を生成するスクリプト
モデル: gemini-3-pro-image-preview
"""

import os
import json
import time
import urllib.request
import urllib.parse
import urllib.error
from pathlib import Path

# .envファイルを直接読み込み
def load_env():
    env_path = Path(__file__).parent / '.env'
    env_vars = {}
    if env_path.exists():
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    env_vars[key.strip()] = value.strip()
    return env_vars

env_vars = load_env()

# APIキーを取得
API_KEY = env_vars.get('GEMINI_API')
if not API_KEY:
    raise ValueError("GEMINI_API key not found in .env file")

# 画像保存先ディレクトリ
IMAGES_DIR = Path(__file__).parent / "images"
IMAGES_DIR.mkdir(exist_ok=True)

# Gemini API エンドポイント
# gemini-2.5-flash-image を使用
API_ENDPOINT = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-image:generateContent?key={API_KEY}"

# 画像生成プロンプトのリスト
IMAGE_PROMPTS = [
    {
        "filename": "hero-bg.jpg",
        "prompt": "A warm and inviting acupuncture treatment room with soft natural light streaming through windows. A patient lying peacefully on a treatment bed while a compassionate therapist stands beside them with a gentle expression. Warm tones, professional medical setting, blurred background effect, photorealistic style, 1920x1080 resolution.",
        "size": "1920x1080"
    },
    {
        "filename": "problem-therapist.jpg",
        "prompt": "A Japanese therapist looking worried and stressed, sitting at a desk with elbows on the table, hand on forehead. Medical charts and papers scattered on the desk. Light coming from a window creating a sense of solitude. Monochrome or desaturated colors, photorealistic style, 1200x800 resolution.",
        "size": "1200x800"
    },
    {
        "filename": "profile-toyoda.jpg",
        "prompt": "Professional portrait of a Japanese male acupuncturist in his 40s named Toyoda. Warm and gentle smile, wearing white medical coat or clean professional attire. Chest-up shot against a clean white background or subtle treatment room background. Conveys warmth and trustworthiness, photorealistic style, 800x800 resolution, square format.",
        "size": "800x800"
    },
    {
        "filename": "story-sunset.jpg",
        "prompt": "Silhouette of a lone therapist standing by a window at sunset. Beautiful orange and purple sunset visible through the window. Figure in contemplation, conveying both solitude and determination. Cinematic photography style, dramatic lighting, 1200x800 resolution.",
        "size": "1200x800"
    },
    {
        "filename": "5-layers-diagram.jpg",
        "prompt": "Infographic diagram showing 5 layers of the mind in a pyramid structure. From surface to deep: 1) Cognitive distortions (thinking patterns), 2) Schema (unconscious negative self-image), 3) Meta-cognition (ability to view oneself objectively), 4) Psychological tunnel vision (lack of mental space), 5) Self-acceptance (accepting oneself as is). Arrows connecting layers showing relationships. Clean modern design, blue and orange color scheme, simple and clear, 1000x800 resolution.",
        "size": "1000x800"
    },
    {
        "filename": "mind-flow-diagram.jpg",
        "prompt": "Flowchart diagram showing the flow of mental processes: Cognition → Emotion → Mental distress → Autonomic nervous system disruption → Physical symptoms. Each stage with brief explanatory text. Arrows showing the flow. Clean infographic style, blue and orange color scheme, simple and clear, 1000x600 resolution.",
        "size": "1000x600"
    },
    {
        "filename": "counseling-illustration.jpg",
        "prompt": "Gentle illustration of a Japanese therapist and patient facing each other. The patient has tears in her eyes while speaking, therapist listening with compassion and kindness. Warm colors, soft artistic style, conveys emotional release and trust, illustrated or soft photographic style, 1000x800 resolution.",
        "size": "1000x800"
    },
    {
        "filename": "before-after-comparison.jpg",
        "prompt": "Before and after comparison image split in two halves. LEFT: Dark mood, therapist and patient with strained expressions, feeling disconnected. RIGHT: Bright mood, therapist and patient smiling and engaged in conversation. Arrow showing transformation from left to right. Illustrated or photo composite style, 1200x600 resolution.",
        "size": "1200x600"
    },
    {
        "filename": "case1-stage1.jpg",
        "prompt": "Japanese woman in her late 20s with an unnaturally bright smile but eyes that don't match the smile. Expression conveys tension and forced cheerfulness. Soft illustration or photographic style, 800x600 resolution.",
        "size": "800x600"
    },
    {
        "filename": "case1-stage2.jpg",
        "prompt": "Dark-toned abstract illustration showing a young child being scolded. Heavy and oppressive mood representing a difficult past. Monochrome or sepia tone, artistic illustration style, 800x600 resolution.",
        "size": "800x600"
    },
    {
        "filename": "case1-stage3.jpg",
        "prompt": "Three-stage facial expression transformation of a Japanese woman shown side by side: 1) Bright smile, 2) Tense expression, 3) Tears flowing. Comic or illustration style showing emotional progression, 800x600 resolution.",
        "size": "800x600"
    },
    {
        "filename": "case1-stage4.jpg",
        "prompt": "Japanese woman speaking through tears while therapist watches over her kindly. Light streaming in creating bright tones. Conveys sense of emotional liberation. Soft illustration or photographic style, 800x600 resolution.",
        "size": "800x600"
    },
    {
        "filename": "case1-stage5.jpg",
        "prompt": "Japanese woman with clear, hopeful expression walking forward. Bright colors and composition conveying hope. Light spreading in the background. Illustrated or cinematic photographic style, 800x600 resolution.",
        "size": "800x600"
    },
    {
        "filename": "case2-symptoms.jpg",
        "prompt": "Japanese woman in her 30s-40s with pained expression. Visual effects showing nausea, palpitations, and anxiety. Ripple-like effects emanating from the body representing discomfort. Dark color tones, illustration style, 800x600 resolution.",
        "size": "800x600"
    },
    {
        "filename": "case2-assessment.jpg",
        "prompt": "Diagram showing mental structure. Center shows 'I have no value' schema. Arrows radiating outward showing cognitive distortions. Text around the diagram reading 'I don't know my true self' and 'I don't know my value'. Infographic style, blue and orange color scheme, 800x600 resolution.",
        "size": "800x600"
    },
    {
        "filename": "case2-future.jpg",
        "prompt": "Japanese woman in her 30s-40s with bright hopeful expression, sitting at a desk studying. Atmosphere full of hope. Soft illustration or photographic style, 800x600 resolution.",
        "size": "800x600"
    },
    {
        "filename": "course-materials.jpg",
        "prompt": "Flat lay photograph of course materials. Laptop, tablet, printed textbook, worksheets, and pen neatly arranged on clean white background. Shot from above, clean and professional educational setting, 1200x800 resolution.",
        "size": "1200x800"
    },
    {
        "filename": "online-learning.jpg",
        "prompt": "Person viewing an online course on laptop or tablet. Screen shows instructor teaching. Textbooks and notebook visible nearby. Bright natural light, clean desk setting. Focus on hands and study materials, photorealistic style, 1200x800 resolution.",
        "size": "1200x800"
    },
    {
        "filename": "diverse-therapists.jpg",
        "prompt": "Group of diverse Japanese healthcare professionals including acupuncturists and therapists. Various ages and genders, all in clean white coats with bright expressions. Professional atmosphere, photorealistic style, 1200x600 resolution.",
        "size": "1200x600"
    },
    {
        "filename": "toyoda-message.jpg",
        "prompt": "Japanese male acupuncturist in his 40s with serious or gentle smile. Arms crossed or relaxed posture. Background is treatment room or naturally lit interior. Conveys trustworthiness and warmth, photorealistic portrait style, 800x1000 resolution, vertical format.",
        "size": "800x1000"
    },
    {
        "filename": "therapist-patient-handshake.jpg",
        "prompt": "Japanese therapist and patient shaking hands with smiles. Warm lighting conveying trust and connection. Background blurred, focus on the people. Photorealistic style, 1200x800 resolution.",
        "size": "1200x800"
    },
    {
        "filename": "bright-future.jpg",
        "prompt": "Bright treatment room with Japanese therapist confidently engaging with smiling patient. Sunlight streaming through windows conveying hope. Photorealistic style, 1200x800 resolution.",
        "size": "1200x800"
    },
    {
        "filename": "final-message-bg.jpg",
        "prompt": "Treatment room interior with warm light streaming in, or silhouette of therapist walking forward. Composition conveying hope. Blurred background suitable for text overlay. Cinematic photography style, 1920x1080 resolution.",
        "size": "1920x1080"
    }
]


def generate_image(prompt_data, retry=3):
    """
    Gemini APIを使用して画像を生成
    """
    filename = prompt_data["filename"]
    prompt = prompt_data["prompt"]
    size = prompt_data.get("size", "1024x1024")

    print(f"\n{'='*80}")
    print(f"Generating: {filename}")
    print(f"Prompt: {prompt[:100]}...")
    print(f"Size: {size}")

    # リクエストボディ（Gemini API形式）
    request_body = {
        "contents": [{
            "parts": [{
                "text": f"Generate an image: {prompt}"
            }]
        }],
        "generationConfig": {
            "response_mime_type": "image/jpeg"
        }
    }

    for attempt in range(retry):
        try:
            print(f"Attempt {attempt + 1}/{retry}...")

            # APIリクエスト
            req = urllib.request.Request(
                API_ENDPOINT,
                data=json.dumps(request_body).encode('utf-8'),
                headers={
                    "Content-Type": "application/json"
                }
            )

            with urllib.request.urlopen(req, timeout=60) as response:
                response_data = json.loads(response.read().decode('utf-8'))

                # Gemini APIのレスポンスから画像データを取得
                if "candidates" in response_data and len(response_data["candidates"]) > 0:
                    candidate = response_data["candidates"][0]

                    if "content" in candidate and "parts" in candidate["content"]:
                        parts = candidate["content"]["parts"]

                        for part in parts:
                            # インラインデータ（Base64）の場合
                            if "inlineData" in part:
                                import base64
                                inline_data = part["inlineData"]
                                if "data" in inline_data:
                                    image_bytes = base64.b64decode(inline_data["data"])

                                    # 画像を保存
                                    output_path = IMAGES_DIR / filename
                                    with open(output_path, "wb") as f:
                                        f.write(image_bytes)

                                    print(f"✓ Successfully saved: {output_path}")
                                    return True
                            # テキストレスポンスの場合（画像生成失敗の可能性）
                            elif "text" in part:
                                print(f"✗ Text response received: {part['text'][:100]}")

                print(f"✗ No image data in response. Response structure: {list(response_data.keys())}")

        except urllib.error.HTTPError as e:
            error_body = e.read().decode('utf-8')
            print(f"✗ HTTP Error {e.code}: {error_body}")
        except Exception as e:
            print(f"✗ Exception occurred: {str(e)}")

        if attempt < retry - 1:
            wait_time = (attempt + 1) * 2
            print(f"Waiting {wait_time} seconds before retry...")
            time.sleep(wait_time)

    print(f"✗ Failed to generate {filename} after {retry} attempts")
    return False


def main():
    """
    メイン処理
    """
    print("="*80)
    print("Gemini API Image Generation Script")
    print(f"Model: gemini-2.5-flash-image")
    print(f"Total images to generate: {len(IMAGE_PROMPTS)}")
    print(f"Output directory: {IMAGES_DIR}")
    print("="*80)

    success_count = 0
    failed_list = []

    for i, prompt_data in enumerate(IMAGE_PROMPTS, 1):
        print(f"\n[{i}/{len(IMAGE_PROMPTS)}]")

        # 既に画像が存在する場合はスキップ
        output_path = IMAGES_DIR / prompt_data["filename"]
        if output_path.exists():
            print(f"⊘ Skipping {prompt_data['filename']} (already exists)")
            success_count += 1
            continue

        # 画像生成
        if generate_image(prompt_data):
            success_count += 1
        else:
            failed_list.append(prompt_data["filename"])

        # API制限を避けるため、少し待機
        if i < len(IMAGE_PROMPTS):
            time.sleep(2)

    # 結果サマリー
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    print(f"Total: {len(IMAGE_PROMPTS)}")
    print(f"Success: {success_count}")
    print(f"Failed: {len(failed_list)}")

    if failed_list:
        print("\nFailed images:")
        for filename in failed_list:
            print(f"  - {filename}")
    else:
        print("\n✓ All images generated successfully!")

    print("="*80)


if __name__ == "__main__":
    main()
