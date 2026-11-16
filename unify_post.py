import os
import re
from bs4 import BeautifulSoup

# 1. 표준 마스터 스타일 및 공통 레이아웃 템플릿 (post-11 기준 통일 규격)
MASTER_TEMPLATE = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - moduin.kr</title>
    <meta name="description" content="{description}">
    <link rel="canonical" href="https://moduin.kr/{rel_url}">
    <script>
        (function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':new Date().getTime(),event:'gtm.js'}});
        var f=d.getElementsByTagName(s)[0],j=d.createElement(s);j.async=true;j.src='https://www.googletagmanager.com/gtm.js?id='+i;
        f.parentNode.insertBefore(j,f);}})(window,document,'script','dataLayer','GTM-P4TG8SLQ');
    </script>
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-6338218836427787" crossorigin="anonymous"></script>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Apple SD Gothic Neo", "Malgun Gothic", "맑은 고딕", sans-serif;
            background-color: #faf9f7;
            color: #2c3e50;
            line-height: 1.85;
            word-break: keep-all;
        }}
        header {{
            background-color: #ffffff;
            border-bottom: 1px solid #e8e6e1;
            padding: 15px 20px;
            position: sticky;
            top: 0;
            z-index: 100;
        }}
        .nav-inner {{
            max-width: 1000px;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 15px;
        }}
        .logo {{
            font-size: 1.3rem;
            font-weight: 800;
            color: #2c3e50;
            text-decoration: none;
            letter-spacing: -0.5px;
        }}
        .nav-inner nav {{
            display: flex;
            flex-wrap: wrap;
            gap: 18px;
        }}
        .nav-inner nav a {{
            text-decoration: none;
            color: #555555;
            font-weight: 600;
            font-size: 0.95rem;
            transition: color 0.2s;
        }}
        .nav-inner nav a:hover,
        .nav-inner nav a.active {{
            color: #d35400;
        }}
        main {{
            max-width: 880px;
            margin: 40px auto;
            padding: 0 20px;
        }}
        article {{
            background-color: #ffffff;
            border: 1px solid #e8e6e1;
            border-radius: 10px;
            padding: 46px 44px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.03);
            overflow-wrap: anywhere;
        }}
        .category-label, .category-badge {{
            display: inline-block;
            background-color: #f4f1ea;
            color: #d35400;
            font-size: 0.82rem;
            font-weight: 700;
            padding: 4px 12px;
            border-radius: 4px;
            margin-bottom: 14px;
        }}
        h1 {{
            font-size: 1.95rem;
            font-weight: 800;
            color: #212529;
            line-height: 1.38;
            margin-bottom: 12px;
            letter-spacing: -0.6px;
        }}
        .post-meta {{
            font-size: 0.9rem;
            color: #777777;
            padding-bottom: 24px;
            margin-bottom: 28px;
            border-bottom: 1px solid #eeeeee;
        }}
        .disclaimer-box {{
            background-color: #fff9f9;
            border: 1px solid #f5c6cb;
            border-left: 4px solid #c0392b;
            border-radius: 6px;
            padding: 18px 22px;
            margin-bottom: 32px;
            font-size: 0.92rem;
            color: #721c24;
            line-height: 1.7;
        }}
        .disclaimer-box p {{ margin-bottom: 6px; color: #721c24; font-size: 0.92rem; }}
        .disclaimer-box p:last-child {{ margin-bottom: 0; }}
        .toc, .toc-card {{
            background-color: #f9f8f5;
            border: 1px solid #e8e6e1;
            border-left: 4px solid #2c3e50;
            padding: 20px 26px;
            margin-bottom: 38px;
            border-radius: 6px;
        }}
        .toc-title {{
            font-size: 1.02rem;
            font-weight: 800;
            color: #2c3e50;
            margin-bottom: 10px;
        }}
        .toc ul, .toc-list {{
            list-style: none;
            padding-left: 0;
            margin-bottom: 0;
        }}
        .toc li, .toc-list li {{
            margin-bottom: 6px;
            font-size: 0.95rem;
        }}
        .toc a, .toc-list a {{
            color: #495057;
            text-decoration: none;
            font-weight: 500;
        }}
        .toc a:hover, .toc-list a:hover {{
            color: #d35400;
            text-decoration: underline;
        }}
        h2 {{
            font-size: 1.4rem;
            font-weight: 800;
            color: #212529;
            margin: 44px 0 18px 0;
            padding-left: 12px;
            border-left: 4px solid #d35400;
            line-height: 1.4;
        }}
        h3 {{
            font-size: 1.15rem;
            font-weight: 700;
            color: #2c3e50;
            margin: 28px 0 12px 0;
        }}
        p {{
            font-size: 1.02rem;
            color: #343a40;
            margin-bottom: 20px;
        }}
        ul, ol {{
            padding-left: 22px;
            margin-bottom: 26px;
        }}
        li {{
            font-size: 0.99rem;
            color: #343a40;
            margin-bottom: 12px;
            line-height: 1.8;
        }}
        .summary-card {{
            background-color: #fbfbfd;
            border: 1px solid #e9ecef;
            border-radius: 6px;
            padding: 18px 22px;
            margin-bottom: 18px;
        }}
        .summary-card p:last-child {{ margin-bottom: 0; }}
        pre {{
            background: #282c34;
            color: #abb2bf;
            padding: 18px 20px;
            border-radius: 8px;
            overflow-x: auto;
            font-family: Consolas, 'Courier New', monospace;
            font-size: 0.9rem;
            line-height: 1.6;
            margin: 24px 0;
        }}
        code {{
            font-family: Consolas, 'Courier New', monospace;
            background: #f1f3f5;
            color: #c7254e;
            padding: 2px 6px;
            border-radius: 4px;
            font-size: 0.9em;
        }}
        pre code {{ background: transparent; color: inherit; padding: 0; }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 24px 0 34px 0;
            font-size: 0.95rem;
        }}
        th, td {{
            border: 1px solid #dee2e6;
            padding: 14px 16px;
            text-align: left;
            vertical-align: top;
            line-height: 1.65;
        }}
        th {{
            background-color: #f4f1ea;
            color: #2c3e50;
            font-weight: 800;
            width: 28%;
        }}
        td {{
            background-color: #ffffff;
            color: #343a40;
        }}
        .author-box {{
            margin-top: 48px;
            padding: 22px 24px;
            background-color: #f8f9fa;
            border: 1px solid #e9ecef;
            border-left: 4px solid #2c3e50;
            border-radius: 6px;
        }}
        .author-title {{
            font-size: 1rem;
            font-weight: 800;
            color: #212529;
            margin-bottom: 6px;
        }}
        .author-box p {{
            font-size: 0.92rem;
            color: #495057;
            margin-bottom: 0;
            line-height: 1.7;
        }}
        footer {{
            padding: 30px 20px;
            color: #777777;
            font-size: 0.88rem;
            background-color: #f2eee9;
            border-top: 1px solid #e2ded7;
            text-align: center;
            margin-top: 60px;
        }}
        footer a {{
            color: #555555;
            text-decoration: none;
            font-weight: 600;
        }}
        footer a:hover {{ text-decoration: underline; }}
        @media (max-width: 640px) {{
            header {{ position: static; }}
            .nav-inner nav {{ gap: 12px; }}
            main {{ margin: 20px auto; padding: 0 12px; }}
            article {{ padding: 26px 20px; }}
            h1 {{ font-size: 1.55rem; }}
            h2 {{ font-size: 1.25rem; }}
        }}
    </style>
</head>
<body>
    <noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-P4TG8SLQ" height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>

    <header>
        <div class="nav-inner">
            <a href="../index.html" class="logo">moduin.kr</a>
            <nav aria-label="주 메뉴">
                <a href="../about.html">소개</a>
                <a href="../category-automation.html"{active_auto}>AI·업무자동화</a>
                <a href="../category-smartfactory.html"{active_sf}>스마트팩토리</a>
                <a href="../category-wealth.html"{active_wealth}>자산관리·투자</a>
                <a href="../tools/stock-uploader.html" style="color:#d35400; font-weight:700;">배포 도구</a>
                <a href="../privacy.html">개인정보처리방침</a>
            </nav>
        </div>
    </header>

    <main>
        <article>
{article_inner}

            <div class="author-box">
                <div class="author-title">작성자: moduin (제조 IT · 스마트팩토리 시스템 아키텍트)</div>
                <p>20년 이상 제조 현장 MES, PLC 설비 인터페이스, C#/.NET 기반 무인 업무 자동화 파이프라인 및 퀀트 데이터 분석 시스템을 설계·구축해 온 현업 소프트웨어 엔지니어입니다. 실무에서 검증된 아키텍처와 트러블슈팅 경험을 기록합니다.</p>
            </div>
        </article>
    </main>

    <footer>
        <p>© 2026 moduin.kr &amp; PlatformWorks. All Rights Reserved.</p>
        <p style="margin-top: 8px;"><a href="../privacy.html">개인정보처리방침</a> | <a href="../index.html">메인으로 이동</a></p>
    </footer>
</body>
</html>
"""

TARGET_DIRS = ["automation", "smartfactory", "wealth"]

def process_file(filepath, folder):
    with open(filepath, "r", encoding="utf-8") as f:
        html = f.read()

    soup = BeautifulSoup(html, "html.parser")

    # 제목 추출
    h1 = soup.find("h1")
    raw_title = h1.get_text(strip=True) if h1 else "기술 칼럼"
    title = re.sub(r"\s*-\s*moduin\.kr$", "", raw_title)

    # 설명(Description) 추출
    meta_desc = soup.find("meta", attrs={"name": "description"})
    description = meta_desc["content"].strip() if (meta_desc and meta_desc.get("content")) else title

    # 본문 컨테이너 찾기 (<article> 또는 <main class="article-card"> 또는 <div class="container">)
    body_container = soup.find("article")
    if not body_container:
        body_container = soup.find("main", class_="article-card")
    if not body_container:
        body_container = soup.find("div", class_="container")

    if not body_container:
        print(f"[건너뜀 - 본문 영역 미발견] {filepath}")
        return

    # 기존 중복 작성자 박스 및 하단 목록 복귀 버튼 제거 (표준으로 통일하기 위함)
    for old_author in body_container.find_all("div", class_="author-box"):
        old_author.decompose()
    for div in body_container.find_all("div"):
        if "작성자: moduin" in div.get_text():
            div.decompose()
    for back_a in body_container.find_all("a", class_="back-link"):
        back_a.decompose()

    article_inner = "".join(str(child) for child in body_container.contents).strip()

    filename = os.path.basename(filepath)
    rel_url = f"{folder}/{filename}"

    active_auto = ' class="active"' if folder == "automation" else ""
    active_sf = ' class="active"' if folder == "smartfactory" else ""
    active_wealth = ' class="active"' if folder == "wealth" else ""

    final_html = MASTER_TEMPLATE.format(
        title=title,
        description=description,
        rel_url=rel_url,
        active_auto=active_auto,
        active_sf=active_sf,
        active_wealth=active_wealth,
        article_inner=article_inner
    )

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(final_html)
    print(f"[통일 완료] {rel_url}")

if __name__ == "__main__":
    for folder in TARGET_DIRS:
        if not os.path.isdir(folder):
            continue
        for fname in sorted(os.listdir(folder)):
            if fname.startswith("post-") and fname.endswith(".html"):
                process_file(os.path.join(folder, fname), folder)
    print("\n모든 포스트 파일의 HTML/CSS 양식 통일이 완료되었습니다.")
