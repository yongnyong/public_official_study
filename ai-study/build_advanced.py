"""Build an offline reader for the controlled study Markdown files."""
from pathlib import Path
import html
import re

ROOT = Path(__file__).resolve().parent
FILES = ['11-2027-exam-plan.md', '12-advanced-syllabus.md', '13-advanced-problems.md']

def inline(s):
    s = html.escape(s)
    s = re.sub(r'`([^`]+)`', r'<code>\1</code>', s)
    s = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', s)
    def link(m):
        url = m[2]
        if url in FILES:
            url = '#part' + str(FILES.index(url))
        elif url.endswith('.md'):
            url = 'https://github.com/yongnyong/public_official_study/blob/main/' + url
        return '<a href="' + url + '">' + m[1] + '</a>'
    return re.sub(r'\[([^\]]+)\]\(([^)]+)\)', link, s)

def render(source):
    out, table, listing, fenced = [], False, False, False
    for line in source.splitlines():
        if line.startswith('```'):
            out.append('</code></pre>' if fenced else '<pre><code>')
            fenced = not fenced
            continue
        if fenced:
            out.append(html.escape(line) + '\n')
            continue
        if not line.startswith('|') and table:
            out.append('</table></div>'); table = False
        is_list = bool(re.match(r'^(- |\d+\. )', line))
        if not is_list and listing:
            out.append('</ul>'); listing = False
        if line.startswith('|'):
            cells = line.strip('|').split('|')
            if all(re.fullmatch(r'\s*:?-+:?\s*', c) for c in cells):
                continue
            tag = 'td' if table else 'th'
            if not table:
                out.append('<div class="scroll"><table>'); table = True
            out.append('<tr>' + ''.join(f'<{tag}>{inline(c.strip())}</{tag}>' for c in cells) + '</tr>')
        elif is_list:
            if not listing:
                out.append('<ul>'); listing = True
            out.append('<li>' + inline(re.sub(r'^(- |\d+\. )', '', line)) + '</li>')
        elif line.startswith(('<details>', '</details>', '<summary>')):
            out.append(line)
        elif line.startswith('#'):
            level = min(len(line) - len(line.lstrip('#')), 6)
            out.append(f'<h{level}>' + inline(line[level:].strip()) + f'</h{level}>')
        elif line.strip() == '---':
            out.append('<hr>')
        elif line.strip():
            out.append('<p>' + inline(line) + '</p>')
    if listing: out.append('</ul>')
    if table: out.append('</table></div>')
    return '\n'.join(out)

def main():
    content = ''.join(f'<section id="part{i}">{render((ROOT/name).read_text(encoding="utf-8"))}</section>' for i, name in enumerate(FILES))
    page = '''<!doctype html><html lang="ko"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>2027 준비 · 심화 학습실</title>
<style>body{margin:0;background:#f3f5fa;color:#192539;font:17px/1.85 system-ui,sans-serif}main{max-width:1000px;margin:auto;padding:24px}nav{background:#142f4b;padding:18px;position:sticky;top:0;z-index:1;display:flex;gap:22px;flex-wrap:wrap}nav a{color:white}section{background:white;padding:32px;margin:24px 0;border-radius:16px;scroll-margin-top:100px}h1,h2,h3{line-height:1.45}h2{margin-top:38px;color:#184f70}a{color:#075a91}table{border-collapse:collapse;width:100%;font-size:15px}td,th{border:1px solid #ccd6df;padding:12px;text-align:left}th{background:#edf4f8}.scroll{overflow:auto}details{border:1px solid #b8cbd8;border-radius:10px;padding:18px;margin:20px 0}summary{cursor:pointer;font-weight:bold;color:#075a91}code{background:#eef2f5;padding:2px 5px}pre{overflow:auto;background:#eef2f5;padding:18px}button{padding:9px;cursor:pointer}@media(max-width:650px){main{padding:8px}section{padding:18px}body{font-size:16px}}@media print{nav,button{display:none}section{padding:0;break-before:page}}</style>
<nav><a href="#part0">2027 시험 기준</a><a href="#part1">추가 공부 범위</a><a href="#part2">심화문제 6개</a><a href="study-workbook.html">기초 교재</a></nav><main><p>기초를 이미 아는 학습자용 · 문제는 자체 제작이며 공식 기출이 아닙니다.</p><button onclick="document.querySelectorAll('details').forEach(d=>d.open=true)">해설 모두 펼치기</button>''' + content + '</main></html>'
    (ROOT/'advanced-2027.html').write_text(page, encoding='utf-8')
    print('Built advanced-2027.html')

if __name__ == '__main__':
    main()
