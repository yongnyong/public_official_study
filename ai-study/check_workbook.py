"""교재의 실행 예제와 계산 결과를 확인한다: python check_workbook.py"""
import contextlib
import io
import math
import sqlite3
from pathlib import Path
import re
import build_workbook as book

expected = {
    0: '(80.0, 266.6666666666667)',
    1: '[9, 8, 7]',
    2: '1 0.6 5.76\n2 1.08 3.6864\n3 1.464 2.359296',
    4: "{'A': 0, 'B': 1, 'C': 1, 'D': 2}",
}
for index, output in expected.items():
    stream = io.StringIO()
    with contextlib.redirect_stdout(stream):
        exec(book.lessons[index]['code'], {})
    assert stream.getvalue().strip() == output, index

db = sqlite3.connect(':memory:')
db.executescript('''
CREATE TABLE student(id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE enrollment(student_id INTEGER, course TEXT, score REAL);
INSERT INTO student VALUES (1,'민수'),(2,'지연');
INSERT INTO enrollment VALUES (1,'AI',80),(1,'DB',90),(2,'AI',100);
''')
sql = book.lessons[5]['code'].split(';')
assert sorted(db.execute(sql[0]).fetchall()) == [('AI', 90.0), ('DB', 90.0)]
assert len(db.execute(sql[1]).fetchall()) == 3
assert len(book.questions) == 20
assert all(len(q[3]) == len(q[5]) and 0 <= q[4] < len(q[3]) for q in book.questions)
assert math.isclose(math.exp(1/math.sqrt(2))/(math.exp(1/math.sqrt(2))+1), 0.6697615493266569)

root = Path(__file__).parent
for doc in root.glob('*.md'):
    for target in re.findall(r'\]\(([^)]+\.md)\)', doc.read_text(encoding='utf-8')):
        if not target.startswith('https://'):
            assert (root / target).exists(), (doc.name, target)
print('PASS: Python examples, SQL examples, attention calculation, quiz structure, document links')
