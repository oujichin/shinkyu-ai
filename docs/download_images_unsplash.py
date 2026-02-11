#!/usr/bin/env python3
"""
Unsplash APIを使用して画像をダウンロードするスクリプト
API不要、高品質なフリー素材
"""

import os
import time
import urllib.request
import urllib.parse
from pathlib import Path

# 画像保存先ディレクトリ
IMAGES_DIR = Path(__file__).parent / "images"
IMAGES_DIR.mkdir(exist_ok=True)

# Unsplash Source API（APIキー不要）
# https://source.unsplash.com/

# 画像ダウンロードリスト
IMAGE_DOWNLOADS = [
    {
        "filename": "hero-bg.jpg",
        "query": "acupuncture treatment room warm light",
        "size": "1920x1080"
    },
    {
        "filename": "problem-therapist.jpg",
        "query": "stressed therapist doctor worried desk",
        "size": "1200x800"
    },
    {
        "filename": "profile-toyoda.jpg",
        "query": "japanese male doctor portrait professional smile",
        "size": "800x800"
    },
    {
        "filename": "story-sunset.jpg",
        "query": "silhouette window sunset contemplation",
        "size": "1200x800"
    },
    {
        "filename": "5-layers-diagram.jpg",
        "query": "pyramid diagram infographic layers",
        "size": "1000x800"
    },
    {
        "filename": "mind-flow-diagram.jpg",
        "query": "flowchart diagram process workflow",
        "size": "1000x600"
    },
    {
        "filename": "counseling-illustration.jpg",
        "query": "therapist patient conversation empathy counseling",
        "size": "1000x800"
    },
    {
        "filename": "before-after-comparison.jpg",
        "query": "transformation change before after comparison",
        "size": "1200x600"
    },
    {
        "filename": "case1-stage1.jpg",
        "query": "woman smile forced happy tense expression",
        "size": "800x600"
    },
    {
        "filename": "case1-stage2.jpg",
        "query": "sad child dark emotional past memory",
        "size": "800x600"
    },
    {
        "filename": "case1-stage3.jpg",
        "query": "woman emotional expression crying tears",
        "size": "800x600"
    },
    {
        "filename": "case1-stage4.jpg",
        "query": "woman talking therapist support tears liberation",
        "size": "800x600"
    },
    {
        "filename": "case1-stage5.jpg",
        "query": "woman walking forward hope bright future",
        "size": "800x600"
    },
    {
        "filename": "case2-symptoms.jpg",
        "query": "woman anxiety stress symptoms pain distress",
        "size": "800x600"
    },
    {
        "filename": "case2-assessment.jpg",
        "query": "mind map mental health diagram structure",
        "size": "800x600"
    },
    {
        "filename": "case2-future.jpg",
        "query": "woman studying learning bright hopeful future",
        "size": "800x600"
    },
    {
        "filename": "course-materials.jpg",
        "query": "laptop tablet textbook study materials desk flatlay",
        "size": "1200x800"
    },
    {
        "filename": "online-learning.jpg",
        "query": "online learning laptop studying course notebook",
        "size": "1200x800"
    },
    {
        "filename": "diverse-therapists.jpg",
        "query": "diverse healthcare professionals group medical team",
        "size": "1200x600"
    },
    {
        "filename": "toyoda-message.jpg",
        "query": "male doctor portrait professional trust warmth",
        "size": "800x1000"
    },
    {
        "filename": "therapist-patient-handshake.jpg",
        "query": "doctor patient handshake trust medical care",
        "size": "1200x800"
    },
    {
        "filename": "bright-future.jpg",
        "query": "bright clinic medical room sunlight hope patient",
        "size": "1200x800"
    },
    {
        "filename": "final-message-bg.jpg",
        "query": "warm light medical room hope silhouette forward",
        "size": "1920x1080"
    }
]


def download_image(image_data, retry=3):
    """
    Unsplash APIから画像をダウンロード
    """
    filename = image_data["filename"]
    query = image_data["query"]
    size = image_data.get("size", "1024x1024")

    print(f"\n{'='*80}")
    print(f"Downloading: {filename}")
    print(f"Query: {query}")
    print(f"Size: {size}")

    # Unsplash Source API URL
    # https://source.unsplash.com/{size}/?{query}
    encoded_query = urllib.parse.quote(query)
    url = f"https://source.unsplash.com/{size}/?{encoded_query}"

    for attempt in range(retry):
        try:
            print(f"Attempt {attempt + 1}/{retry}...")
            print(f"URL: {url}")

            # 画像をダウンロード
            with urllib.request.urlopen(url, timeout=30) as response:
                image_bytes = response.read()

                # 画像を保存
                output_path = IMAGES_DIR / filename
                with open(output_path, "wb") as f:
                    f.write(image_bytes)

                file_size = len(image_bytes) / 1024  # KB
                print(f"✓ Successfully downloaded: {output_path} ({file_size:.1f} KB)")
                return True

        except urllib.error.HTTPError as e:
            print(f"✗ HTTP Error {e.code}: {e.reason}")
        except urllib.error.URLError as e:
            print(f"✗ URL Error: {e.reason}")
        except Exception as e:
            print(f"✗ Exception occurred: {str(e)}")

        if attempt < retry - 1:
            wait_time = (attempt + 1) * 2
            print(f"Waiting {wait_time} seconds before retry...")
            time.sleep(wait_time)

    print(f"✗ Failed to download {filename} after {retry} attempts")
    return False


def main():
    """
    メイン処理
    """
    print("="*80)
    print("Unsplash Image Download Script")
    print(f"Total images to download: {len(IMAGE_DOWNLOADS)}")
    print(f"Output directory: {IMAGES_DIR}")
    print("="*80)

    success_count = 0
    failed_list = []

    for i, image_data in enumerate(IMAGE_DOWNLOADS, 1):
        print(f"\n[{i}/{len(IMAGE_DOWNLOADS)}]")

        # 既に画像が存在する場合はスキップ
        output_path = IMAGES_DIR / image_data["filename"]
        if output_path.exists():
            print(f"⊘ Skipping {image_data['filename']} (already exists)")
            success_count += 1
            continue

        # 画像ダウンロード
        if download_image(image_data):
            success_count += 1
        else:
            failed_list.append(image_data["filename"])

        # API制限を避けるため、少し待機
        if i < len(IMAGE_DOWNLOADS):
            time.sleep(1)

    # 結果サマリー
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    print(f"Total: {len(IMAGE_DOWNLOADS)}")
    print(f"Success: {success_count}")
    print(f"Failed: {len(failed_list)}")

    if failed_list:
        print("\nFailed images:")
        for filename in failed_list:
            print(f"  - {filename}")
    else:
        print("\n✓ All images downloaded successfully!")

    print("="*80)


if __name__ == "__main__":
    main()
