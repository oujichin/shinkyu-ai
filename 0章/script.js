// ===================================
// スムーススクロール
// ===================================
document.querySelectorAll('a.smooth-scroll').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const targetId = this.getAttribute('href');

        if (targetId === '#top') {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        } else {
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                const headerOffset = 80;
                const elementPosition = targetElement.getBoundingClientRect().top;
                const offsetPosition = elementPosition + window.pageYOffset - headerOffset;

                window.scrollTo({
                    top: offsetPosition,
                    behavior: 'smooth'
                });
            }
        }
    });
});

// ===================================
// ページトップボタンの表示/非表示
// ===================================
const pageTopButton = document.getElementById('pageTop');

window.addEventListener('scroll', () => {
    if (window.pageYOffset > 300) {
        pageTopButton.classList.add('show');
    } else {
        pageTopButton.classList.remove('show');
    }
});

// ===================================
// フォームバリデーション
// ===================================
const applicationForm = document.getElementById('applicationForm');

if (applicationForm) {
    applicationForm.addEventListener('submit', function(e) {
        e.preventDefault();

        // 基本的なバリデーション
        const name = document.getElementById('name').value.trim();
        const furigana = document.getElementById('furigana').value.trim();
        const email = document.getElementById('email').value.trim();
        const phone = document.getElementById('phone').value.trim();
        const occupation = document.getElementById('occupation').value.trim();
        const privacy = document.getElementById('privacy').checked;

        // エラーメッセージのリセット
        clearErrors();

        let hasError = false;

        // お名前チェック
        if (name === '') {
            showError('name', 'お名前を入力してください');
            hasError = true;
        }

        // ふりがなチェック
        if (furigana === '') {
            showError('furigana', 'ふりがなを入力してください');
            hasError = true;
        } else if (!/^[ぁ-んー\s]+$/.test(furigana)) {
            showError('furigana', 'ひらがなで入力してください');
            hasError = true;
        }

        // メールアドレスチェック
        if (email === '') {
            showError('email', 'メールアドレスを入力してください');
            hasError = true;
        } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
            showError('email', '正しいメールアドレスを入力してください');
            hasError = true;
        }

        // 電話番号チェック
        if (phone === '') {
            showError('phone', '電話番号を入力してください');
            hasError = true;
        } else if (!/^[0-9\-]+$/.test(phone)) {
            showError('phone', '正しい電話番号を入力してください');
            hasError = true;
        }

        // 職業/資格チェック
        if (occupation === '') {
            showError('occupation', '職業/資格を入力してください');
            hasError = true;
        }

        // プライバシーポリシーチェック
        if (!privacy) {
            showError('privacy', 'プライバシーポリシーに同意してください');
            hasError = true;
        }

        // エラーがなければ送信確認
        if (!hasError) {
            if (confirm('この内容で送信してよろしいですか？')) {
                // 実際の送信処理（PHPなどのバックエンドへ）
                // この部分は実際の環境に合わせて実装してください

                // デモ用: サンクスページへ遷移またはメッセージ表示
                alert('お申し込みありがとうございます。\n3営業日以内に、振込先情報をメールでお送りいたします。');
                applicationForm.reset();
            }
        } else {
            // エラーがある場合、最初のエラー要素までスクロール
            const firstError = document.querySelector('.error-message');
            if (firstError) {
                firstError.previousElementSibling.previousElementSibling.scrollIntoView({
                    behavior: 'smooth',
                    block: 'center'
                });
            }
        }
    });
}

function showError(fieldId, message) {
    const field = document.getElementById(fieldId);
    const formGroup = field.closest('.form-group');

    // エラーメッセージ要素の作成
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.style.color = '#d32f2f';
    errorDiv.style.fontSize = '0.875rem';
    errorDiv.style.marginTop = '0.5rem';
    errorDiv.textContent = message;

    // フィールドの枠を赤くする
    field.style.borderColor = '#d32f2f';

    // エラーメッセージを挿入
    formGroup.appendChild(errorDiv);
}

function clearErrors() {
    // すべてのエラーメッセージを削除
    document.querySelectorAll('.error-message').forEach(error => {
        error.remove();
    });

    // すべてのフィールドの枠色をリセット
    document.querySelectorAll('.form-input, .form-textarea').forEach(field => {
        field.style.borderColor = '';
    });
}

// ===================================
// スクロールアニメーション（フェードイン）
// ===================================
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

// アニメーション対象の要素を設定
document.querySelectorAll('.problem-item, .story-item, .method-pillar, .change-card, .case-stage, .course-chapter, .future-card, .faq-item').forEach(element => {
    element.style.opacity = '0';
    element.style.transform = 'translateY(30px)';
    element.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    observer.observe(element);
});

// ===================================
// ヘッダーの背景色変更（スクロール時）
// ===================================
const header = document.querySelector('.header');
let lastScroll = 0;

window.addEventListener('scroll', () => {
    const currentScroll = window.pageYOffset;

    if (currentScroll > 100) {
        header.style.boxShadow = '0 4px 15px rgba(0, 0, 0, 0.15)';
    } else {
        header.style.boxShadow = '0 2px 10px rgba(0, 0, 0, 0.1)';
    }

    lastScroll = currentScroll;
});

// ===================================
// 画像の遅延読み込み（Lazy Loading）
// ===================================
if ('loading' in HTMLImageElement.prototype) {
    // ブラウザがネイティブの遅延読み込みをサポートしている場合
    const images = document.querySelectorAll('img[loading="lazy"]');
    images.forEach(img => {
        img.src = img.dataset.src;
    });
} else {
    // サポートしていない場合はIntersectionObserverを使用
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.remove('lazy');
                imageObserver.unobserve(img);
            }
        });
    });

    const images = document.querySelectorAll('img.lazy');
    images.forEach(img => imageObserver.observe(img));
}

// ===================================
// FAQのアコーディオン機能（オプション）
// ===================================
document.querySelectorAll('.faq-question').forEach(question => {
    question.addEventListener('click', () => {
        const answer = question.nextElementSibling;
        const isOpen = answer.style.display === 'block';

        // すべての回答を閉じる
        document.querySelectorAll('.faq-answer').forEach(ans => {
            ans.style.display = 'none';
        });

        // クリックされた質問の回答を開く/閉じる
        if (!isOpen) {
            answer.style.display = 'block';
        }
    });
});

// 最初の質問は開いた状態にする
if (document.querySelector('.faq-answer')) {
    document.querySelector('.faq-answer').style.display = 'block';
}

// ===================================
// console.log（デバッグ用）
// ===================================
console.log('Tメソッド講座 LP - JavaScript loaded successfully');
