#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_html.py — 《AI 大模型不难》构建脚本

将所有 26 课 Markdown 转换为单个精美的 HTML 页面，并可选择生成 PDF。

用法:
    python scripts/build_html.py            # 生成 index.html
    python scripts/build_html.py --pdf      # 生成 index.html + PDF
"""

import os
import re
import sys
import subprocess
from pathlib import Path

# ── 路径配置 ────────────────────────────────────────────
PROJECT_ROOT = Path(__file__).resolve().parent.parent
LESSONS_DIR = PROJECT_ROOT / "lessons"
ASSETS_DIR = PROJECT_ROOT / "assets"
OUTPUT_HTML = PROJECT_ROOT / "index.html"
OUTPUT_PDF = PROJECT_ROOT / "ai-llm-made-easy.pdf"

PART_DIRS = [
    ("part0-intro",     "开篇"),
    ("part1-worldview", "第一部分：世界观 —— 大模型到底是个什么东西"),
    ("part2-engine",    "第二部分：引擎 —— Transformer 里里外外"),
    ("part3-training",  "第三部分：炼金 —— 模型是怎么训出来的"),
    ("part4-engineering","第四部分：落地 —— 大模型的十八般武艺"),
    ("part5-interview", "第五部分：实战 —— 面试现场还原"),
    ("appendix",        "附录"),
]


def ensure_dependencies():
    """确保 markdown 库已安装"""
    try:
        import markdown  # noqa: F401
    except ImportError:
        print("[setup] 正在安装 markdown 库...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "markdown"])
        print("[setup] markdown 安装完成")


def collect_lessons():
    """
    按顺序收集所有课程文件路径。
    返回: [(课号, 文件路径, 所属部分名), ...]
    """
    lessons = []
    for part_dir_name, part_label in PART_DIRS:
        part_path = LESSONS_DIR / part_dir_name
        if not part_path.exists():
            continue
        # 收集该部分下所有 .md 文件，按文件名排序（数字顺序）
        md_files = sorted(part_path.glob("lesson-*.md"), key=lambda p: p.name)
        for md_file in md_files:
            # 从文件名提取课号
            match = re.match(r"lesson-(\d+)", md_file.stem)
            if match:
                lesson_num = int(match.group(1))
                lessons.append((lesson_num, md_file, part_label))
    # 按课号排序（处理 part4 文件乱序问题）
    lessons.sort(key=lambda x: x[0])
    return lessons


def inline_svg_refs(md_text, lesson_path):
    """
    预处理 Markdown 文本：将 ![...](../../assets/xxx.svg) 引用替换为内嵌 SVG。

    参数:
        md_text: 原始 Markdown 文本
        lesson_path: 课程文件的绝对路径（用于解析相对路径）
    返回:
        处理后的 Markdown 文本（SVG 已替换为原始 HTML）
    """
    lesson_dir = lesson_path.parent

    def replace_svg(match):
        alt_text = match.group(1).strip()
        rel_path = match.group(2)
        abs_path = (lesson_dir / rel_path).resolve()
        if abs_path.exists() and abs_path.suffix.lower() == ".svg":
            svg_content = abs_path.read_text(encoding="utf-8")
            # 确保 SVG 具有合适的显示属性
            svg_content = svg_content.replace('width="100%"', '')
            # 去掉 XML 声明和文档类型（如果有）
            svg_content = re.sub(r'<\?xml[^>]+\?>', '', svg_content)
            svg_content = re.sub(r'<!DOCTYPE[^>]+>', '', svg_content)
            return (
                f'<figure class="svg-figure">\n'
                f'{svg_content.strip()}\n'
                f'<figcaption>{alt_text}</figcaption>\n'
                f'</figure>'
            )
        return match.group(0)

    pattern = r'!\[([^\]]*)\]\(([^)]+\.svg)\)'
    return re.sub(pattern, replace_svg, md_text)


def extract_title(md_text):
    """从 Markdown 文本中提取 h1 标题"""
    match = re.search(r'^#\s+(.+)$', md_text, re.MULTILINE)
    return match.group(1).strip() if match else ""


def extract_headings(md_text):
    """
    从 Markdown 文本中提取所有 h1、h2 标题。
    返回: [(级别(1/2), 标题文本, 锚点ID), ...]
    """
    headings = []
    for line in md_text.splitlines():
        m = re.match(r'^(#{1,3})\s+(.+)$', line)
        if m:
            level = len(m.group(1))
            title = m.group(2).strip()
            anchor = title_to_anchor(title)
            headings.append((level, title, anchor))
    return headings


def title_to_anchor(title):
    """将标题文本转换为合法的 HTML 锚点 ID"""
    anchor = title.strip()
    # 保留中文、英文、数字、连字符、空格
    anchor = re.sub(r'[^\w\s\u4e00-\u9fff-]', '', anchor)
    anchor = anchor.strip().replace(' ', '-').replace('_', '-')
    # 移除连续破折号
    anchor = re.sub(r'-{2,}', '-', anchor)
    anchor = anchor.strip('-')
    return anchor.lower()


def build_full_html(lessons_data):
    """
    构建完整的 HTML 文档。

    lessons_data: [(课号, html_body, h1_title, h2_headings, part_label), ...]
    """
    # 收集所有标题用于生成目录
    all_toc_entries = []
    for lesson_num, html_body, h1_title, h2_headings, part_label in lessons_data:
        anchor = f"lesson-{lesson_num}"
        all_toc_entries.append((lesson_num, h1_title, anchor, part_label))
        for level, title, h_anchor in h2_headings:
            if level == 2:
                all_toc_entries.append((lesson_num, title, h_anchor, None))

    # ── 生成目录 HTML ──
    toc_html = build_toc(all_toc_entries)

    # ── 生成正文 HTML ──
    body_html = build_body(lessons_data)

    # ── CSS 样式 ──
    css = get_styles()

    # ── 完整 HTML ──
    total_lessons = len(lessons_data)
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AI 大模型不难 —— 一本让零基础读者也能笑着看懂 Transformer 的开源书</title>
<style>
{css}
</style>
</head>
<body>

<article id="book">

<header class="book-header">
  <h1 class="book-title">AI 大模型不难</h1>
  <p class="book-subtitle">一本让零基础读者也能笑着看懂 Transformer 的开源电子书</p>
  <p class="book-meta">共 {total_lessons} 课 · 五大部分 · 从零到面试通关</p>
</header>

{toc_html}

{body_html}

<footer class="book-footer">
  <p>《AI 大模型不难》—— 开源电子书</p>
  <p>灵感来自鸢尾花书的视觉密度和数字生命卡兹克的叙事温度</p>
  <p><a href="https://github.com/moyai/ai-llm-made-easy" target="_blank">GitHub</a></p>
</footer>

</article>

</body>
</html>"""
    return html


def build_toc(entries):
    """构建目录 HTML"""
    lines = ['<nav id="toc" class="toc">', '<h2 class="toc-title">目录</h2>', '<ol class="toc-list">']

    current_lesson = None
    current_part = None
    # entries: [(lesson_num, title, anchor, part_label_or_None), ...]
    # 首先按照 lesson_num 分组，并跟踪 part 变化

    # 重新组织：先收集每课的 part 信息
    lesson_part_map = {}
    for lesson_num, title, anchor, part_label in entries:
        if part_label is not None:
            lesson_part_map[lesson_num] = part_label

    prev_part = None
    for lesson_num, title, anchor, part_label in entries:
        # 如果是主标题（h1），且进入新 part
        if part_label is not None:
            part = part_label
            if part != prev_part:
                lines.append(f'<li class="toc-part">{part}</li>')
                prev_part = part
            current_lesson = lesson_num
            lines.append(
                f'<li class="toc-lesson">'
                f'<a href="#lesson-{lesson_num}">第 {lesson_num} 课 · {title}</a>'
                f'</li>'
            )
        else:
            # h2 副标题（缩进显示）
            lines.append(
                f'<li class="toc-h2">'
                f'<a href="#{anchor}">{title}</a>'
                f'</li>'
            )

    lines.append('</ol>')
    lines.append('</nav>')
    return '\n'.join(lines)


def build_body(lessons_data):
    """构建正文 HTML"""
    sections = []
    total = len(lessons_data)

    for i, (lesson_num, html_body, h1_title, h2_headings, part_label) in enumerate(lessons_data):
        prev_num = lessons_data[i - 1][0] if i > 0 else None
        next_num = lessons_data[i + 1][0] if i < total - 1 else None

        prev_link = f'<a href="#lesson-{prev_num}">← 上一课</a>' if prev_num is not None else '<span class="nav-disabled">← 上一课</span>'
        next_link = f'<a href="#lesson-{next_num}">下一课 →</a>' if next_num is not None else '<span class="nav-disabled">下一课 →</span>'

        # 调整内部标题的锚点级别
        html_body = adjust_heading_anchors(html_body, lesson_num)

        section = f"""
<section id="lesson-{lesson_num}" class="lesson">
  <div class="lesson-part-label">{part_label}</div>
  {html_body}
  <nav class="lesson-nav">
    {prev_link}
    <a href="#toc" class="nav-center">↑ 目录</a>
    {next_link}
  </nav>
</section>
"""
        sections.append(section)

    return '\n'.join(sections)


def adjust_heading_anchors(html_body, lesson_num):
    """确保 HTML 中的 h1-h3 元素有正确的 ID 属性"""
    html_body = re.sub(
        r'<h2>(.*?)</h2>',
        lambda m: f'<h2 id="{title_to_anchor(m.group(1))}">{m.group(1)}</h2>',
        html_body
    )
    html_body = re.sub(
        r'<h3>(.*?)</h3>',
        lambda m: f'<h3 id="{title_to_anchor(m.group(1))}">{m.group(1)}</h3>',
        html_body
    )
    return html_body


def get_styles():
    """返回完整的 CSS 样式表"""
    return r"""/* ── Reset & Base ─────────────────────────────────────── */
*, *::before, *::after {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

html {
  font-size: 16px;
  scroll-behavior: smooth;
  -webkit-text-size-adjust: 100%;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans SC",
               "PingFang SC", "Microsoft YaHei", "Hiragino Sans GB",
               "Helvetica Neue", Helvetica, Arial, sans-serif;
  font-size: 1rem;
  line-height: 1.8;
  color: #2C2C2A;
  background: #FAFBFC;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

/* ── Book Container ──────────────────────────────────── */
#book {
  max-width: 720px;
  margin: 0 auto;
  padding: 3rem 1.5rem 5rem;
}

/* ── Book Header ──────────────────────────────────────── */
.book-header {
  text-align: center;
  padding: 3rem 0 2rem;
  border-bottom: 2px solid #E8E6DE;
  margin-bottom: 2.5rem;
}

.book-title {
  font-size: 2.4rem;
  font-weight: 700;
  letter-spacing: 0.04em;
  color: #1a1a18;
  margin-bottom: 0.5rem;
}

.book-subtitle {
  font-size: 1.1rem;
  color: #6E6D68;
  margin-bottom: 0.3rem;
}

.book-meta {
  font-size: 0.9rem;
  color: #9A9994;
}

/* ── TOC ──────────────────────────────────────────────── */
.toc {
  background: #FFFFFF;
  border: 1px solid #E8E6DE;
  border-radius: 8px;
  padding: 1.8rem 2rem;
  margin-bottom: 3rem;
}

.toc-title {
  font-size: 1.3rem;
  font-weight: 600;
  color: #1a1a18;
  margin-bottom: 1rem;
  padding-bottom: 0.6rem;
  border-bottom: 1px solid #E8E6DE;
}

.toc-list {
  list-style: none;
}

.toc-part {
  font-size: 0.85rem;
  font-weight: 600;
  color: #9A9994;
  text-transform: none;
  letter-spacing: 0.02em;
  margin-top: 1rem;
  padding: 0.2rem 0 0.1rem;
  border-top: 1px dotted #E8E6DE;
}

.toc-part:first-child {
  margin-top: 0;
  border-top: none;
}

.toc-lesson {
  padding: 0.15rem 0;
}

.toc-lesson a {
  color: #2C2C2A;
  text-decoration: none;
  font-weight: 500;
  font-size: 0.98rem;
  transition: color 0.15s;
}

.toc-lesson a:hover {
  color: #378ADD;
}

.toc-h2 {
  padding: 0.08rem 0 0.08rem 1.8rem;
}

.toc-h2 a {
  color: #6E6D68;
  text-decoration: none;
  font-size: 0.88rem;
  transition: color 0.15s;
}

.toc-h2 a:hover {
  color: #378ADD;
}

/* ── Lesson Sections ──────────────────────────────────── */
.lesson {
  margin-bottom: 3rem;
  padding-top: 1rem;
  border-top: 1px solid #E8E6DE;
}

.lesson:first-of-type {
  border-top: none;
}

.lesson-part-label {
  display: inline-block;
  font-size: 0.78rem;
  font-weight: 600;
  color: #9A9994;
  text-transform: none;
  letter-spacing: 0.04em;
  margin-bottom: 0.8rem;
  padding: 0.2rem 0.6rem;
  background: #F1EFE8;
  border-radius: 3px;
}

/* ── Headings ─────────────────────────────────────────── */
.lesson h1 {
  font-size: 1.7rem;
  font-weight: 700;
  color: #1a1a18;
  line-height: 1.35;
  margin: 0.5rem 0 1.2rem;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid #E8E6DE;
}

.lesson h2 {
  font-size: 1.25rem;
  font-weight: 600;
  color: #2C2C2A;
  margin: 2rem 0 0.8rem;
  padding-left: 0.5rem;
  border-left: 3px solid #378ADD;
}

.lesson h3 {
  font-size: 1.05rem;
  font-weight: 600;
  color: #444;
  margin: 1.5rem 0 0.5rem;
}

/* ── Paragraphs & Inline ──────────────────────────────── */
.lesson p {
  margin: 0 0 1.1rem;
  text-align: justify;
  text-justify: inter-ideograph;
}

.lesson strong {
  font-weight: 600;
  color: #1a1a18;
}

.lesson em {
  font-style: italic;
}

/* ── Links ────────────────────────────────────────────── */
.lesson a {
  color: #378ADD;
  text-decoration: none;
  border-bottom: 1px solid transparent;
  transition: border-color 0.15s;
}

.lesson a:hover {
  border-bottom-color: #378ADD;
}

/* ── Horizontal Rules ─────────────────────────────────── */
.lesson hr {
  border: none;
  border-top: 1px dotted #D4D2C8;
  margin: 2rem 0;
}

/* ── Blockquotes ──────────────────────────────────────── */
.lesson blockquote {
  margin: 1.5rem 0;
  padding: 0.8rem 1.2rem;
  background: #F7F6F1;
  border-left: 3px solid #D4D2C8;
  font-size: 0.95rem;
  color: #555;
}

.lesson blockquote p {
  margin: 0.3rem 0;
}

.lesson blockquote p:last-child {
  margin-bottom: 0;
}

/* ── Code Inline ──────────────────────────────────────── */
.lesson code {
  font-family: "SF Mono", "Fira Code", "Fira Mono", "Roboto Mono",
               "Cascadia Code", "Consolas", "Courier New", monospace;
  font-size: 0.88em;
  background: #F1EFE8;
  color: #C75B39;
  padding: 0.15em 0.35em;
  border-radius: 3px;
}

/* ── Code Blocks ──────────────────────────────────────── */
.lesson pre {
  background: #F1EFE8;
  border: 1px solid #E0DDD3;
  border-radius: 6px;
  padding: 1rem 1.2rem;
  margin: 1.2rem 0;
  overflow-x: auto;
  font-size: 0.88rem;
  line-height: 1.6;
}

.lesson pre code {
  background: none;
  color: #2C2C2A;
  padding: 0;
  font-size: inherit;
}

/* ── Lists ────────────────────────────────────────────── */
.lesson ul,
.lesson ol {
  margin: 0.8rem 0 1.2rem 1.5rem;
}

.lesson li {
  margin-bottom: 0.35rem;
  line-height: 1.7;
}

.lesson li p {
  margin: 0;
}

/* ── Tables ───────────────────────────────────────────── */
.lesson table {
  width: 100%;
  border-collapse: collapse;
  margin: 1.5rem 0;
  font-size: 0.9rem;
}

.lesson thead th {
  background: #F1EFE8;
  color: #2C2C2A;
  font-weight: 600;
  padding: 0.6rem 0.8rem;
  border: 1px solid #E0DDD3;
  text-align: left;
}

.lesson tbody td {
  padding: 0.5rem 0.8rem;
  border: 1px solid #E8E6DE;
}

.lesson tbody tr:nth-child(even) {
  background: #FAFAF8;
}

/* ── SVG Figures ──────────────────────────────────────── */
.svg-figure {
  margin: 2rem 0;
  text-align: center;
  background: #FFFFFF;
  border: 1px solid #E8E6DE;
  border-radius: 8px;
  padding: 1.5rem 1rem;
}

.svg-figure svg {
  max-width: 100%;
  height: auto;
}

.svg-figure figcaption {
  margin-top: 0.8rem;
  font-size: 0.85rem;
  color: #9A9994;
  font-style: italic;
}

/* ── Lesson Navigation ────────────────────────────────── */
.lesson-nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 2.5rem;
  padding: 1rem 0;
  border-top: 1px solid #E8E6DE;
  font-size: 0.92rem;
}

.lesson-nav a {
  color: #378ADD;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.15s;
}

.lesson-nav a:hover {
  color: #185FA5;
}

.lesson-nav .nav-center {
  color: #9A9994;
}

.lesson-nav .nav-center:hover {
  color: #6E6D68;
}

.nav-disabled {
  color: #CCC;
}

/* ── Footer ───────────────────────────────────────────── */
.book-footer {
  text-align: center;
  padding: 3rem 0 2rem;
  margin-top: 3rem;
  border-top: 2px solid #E8E6DE;
  color: #9A9994;
  font-size: 0.88rem;
  line-height: 1.8;
}

.book-footer a {
  color: #378ADD;
  text-decoration: none;
}

/* ── Print Styles ─────────────────────────────────────── */
@media print {
  body {
    background: #FFFFFF;
    color: #000;
    font-size: 12pt;
    line-height: 1.6;
  }

  #book {
    max-width: 100%;
    padding: 0;
    margin: 0;
  }

  .book-header {
    padding: 1rem 0;
    margin-bottom: 1rem;
    border-bottom: 1px solid #000;
  }

  .book-title {
    font-size: 18pt;
  }

  .toc {
    page-break-after: always;
    border: none;
    background: none;
    padding: 1rem 0;
  }

  .toc a {
    color: #000 !important;
  }

  .lesson {
    page-break-before: always;
    border-top: none;
    margin-bottom: 1rem;
  }

  .lesson:first-of-type {
    page-break-before: avoid;
  }

  .lesson h1 {
    font-size: 14pt;
    border-bottom: 1px solid #000;
  }

  .lesson h2 {
    font-size: 12pt;
    border-left: 2px solid #000;
  }

  .lesson-part-label {
    background: none;
    border: 1px solid #000;
  }

  .lesson-nav {
    display: none;
  }

  .svg-figure {
    border: none;
    background: none;
    padding: 1rem 0;
  }

  .lesson pre {
    background: #f5f5f5;
    border: 1px solid #ccc;
  }

  .lesson code {
    background: #f0f0f0;
  }

  .book-footer {
    border-top: 1px solid #000;
    color: #666;
  }

  @page {
    margin: 2cm;
    @bottom-center {
      content: counter(page);
      font-size: 9pt;
      color: #999;
    }
  }
}

/* ── Responsive ───────────────────────────────────────── */
@media (max-width: 768px) {
  #book {
    padding: 1.5rem 1rem 3rem;
  }

  .book-title {
    font-size: 1.8rem;
  }

  .lesson h1 {
    font-size: 1.4rem;
  }

  .lesson h2 {
    font-size: 1.1rem;
  }
}
"""


def convert_md_to_html(md_text):
    """将 Markdown 文本转换为 HTML"""
    import markdown
    return markdown.markdown(
        md_text,
        extensions=[
            'fenced_code',      # 围栏代码块
            'codehilite',       # 代码语法高亮（需要 Pygments）
            'tables',           # 表格支持
        ],
        extension_configs={
            'codehilite': {
                'css_class': 'highlight',
                'guess_lang': True,
            },
        }
    )


def main():
    ensure_dependencies()

    lessons_data = collect_lessons()
    if not lessons_data:
        print("[error] 未找到任何课程文件")
        sys.exit(1)

    print(f"[info] 找到 {len(lessons_data)} 个课程文件")
    for num, path, part in lessons_data:
        print(f"  - 第 {num:2d} 课: {path.relative_to(PROJECT_ROOT)}")

    # 读取并处理每课内容
    processed = []
    for lesson_num, path, part_label in lessons_data:
        print(f"[processing] 第 {lesson_num} 课...")
        md_text = path.read_text(encoding="utf-8")

        # 预处理：嵌入 SVG 图像
        md_text = inline_svg_refs(md_text, path)

        # 提取标题
        h1_title = extract_title(md_text)
        h2_headings = extract_headings(md_text)

        # 转换为 HTML
        html_body = convert_md_to_html(md_text)

        processed.append((lesson_num, html_body, h1_title, h2_headings, part_label))

    # 构建完整 HTML
    print("[build] 正在生成 HTML...")
    full_html = build_full_html(processed)

    OUTPUT_HTML.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_HTML.write_text(full_html, encoding="utf-8")
    print(f"[done] HTML 已生成: {OUTPUT_HTML}")
    print(f"       文件大小: {OUTPUT_HTML.stat().st_size / 1024:.1f} KB")

    # 尝试生成 PDF
    gen_pdf = "--pdf" in sys.argv
    if gen_pdf:
        generate_pdf()


def generate_pdf():
    """使用 Chrome/Edge headless 模式生成 PDF"""
    print("[pdf] 正在生成 PDF...")

    # 尝试找 Chrome 或 Edge
    chrome_paths = [
        "C:/Program Files/Google/Chrome/Application/chrome.exe",
        "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe",
        "C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe",
        "C:/Program Files/Microsoft/Edge/Application/msedge.exe",
    ]

    chrome = None
    for p in chrome_paths:
        if os.path.exists(p):
            chrome = p
            break

    if not chrome:
        print("[pdf] 未找到 Chrome 或 Edge 浏览器")
        print_manual_pdf_instructions()
        return

    try:
        html_url = OUTPUT_HTML.as_uri()
        cmd = [
            chrome,
            "--headless",
            "--disable-gpu",
            "--no-sandbox",
            f"--print-to-pdf={OUTPUT_PDF}",
            "--no-pdf-header-footer",
            html_url,
        ]
        subprocess.run(cmd, check=True, timeout=30, capture_output=True)
        if OUTPUT_PDF.exists():
            print(f"[done] PDF 已生成: {OUTPUT_PDF}")
            print(f"       文件大小: {OUTPUT_PDF.stat().st_size / 1024 / 1024:.1f} MB")
        else:
            print("[pdf] PDF 生成失败，文件未创建")
            print_manual_pdf_instructions()
    except subprocess.TimeoutExpired:
        print("[pdf] PDF 生成超时")
        print_manual_pdf_instructions()
    except Exception as e:
        print(f"[pdf] 生成失败: {e}")
        print_manual_pdf_instructions()


def print_manual_pdf_instructions():
    """打印手动生成 PDF 的说明"""
    print("""
[manual-pdf] 请使用以下任一方式手动生成 PDF:

  方式 1 — 使用浏览器:
    1. 在浏览器中打开 index.html
    2. 按 Ctrl+P 打开打印对话框
    3. 选择「另存为 PDF」
    4. 调整边距和纸张大小
    5. 保存为 ai-llm-made-easy.pdf

  方式 2 — 使用 wkhtmltopdf:
    1. 安装: https://wkhtmltopdf.org/downloads.html
    2. 运行: wkhtmltopdf index.html ai-llm-made-easy.pdf

  方式 3 — 使用 pandoc + LaTeX:
    1. 安装 pandoc 和 LaTeX (推荐 MiKTeX)
    2. 运行: pandoc index.html -o ai-llm-made-easy.pdf --pdf-engine=xelatex -V mainfont="Noto Sans SC"
""")


if __name__ == "__main__":
    main()
