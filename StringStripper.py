import re

INPUT_FILE = "input.js"
OUTPUT_FILE = "output.js"
EXTRACTED_FILE = "extracted.txt"
DELIM = "__DELIM__"

patterns = [
    re.compile(r"'(?:\\.|[^'\\\n])*'"),
    re.compile(r'"(?:\\.|[^"\\\n])*"'),
    re.compile(r'`(?:\\.|[^`\\])*`', re.DOTALL),
]
extracted = []

def make_replacer():
    def repl(m):
        extracted.append(m.group(0))
        return f"__QUOTED_{len(extracted)-1}__"
    return repl
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    data = f.read()
for pat in patterns:
    data = pat.sub(make_replacer(), data)
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write(data)
with open(EXTRACTED_FILE, "w", encoding="utf-8") as f:
    f.write(DELIM.join(extracted))
