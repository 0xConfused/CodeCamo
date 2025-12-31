import re

INPUT_FILE = "input.txt"
OUTPUT_FILE = "output.txt"
LIST_FILE = "extracted.txt"
patterns = [
		re.compile(r"('(?:\\.|[^'\\\n])*')"),
		re.compile(r'("(?:\\.|[^"\\\n])*")'),
		re.compile(r'(`(?:\\.|[^`\\])*`)', re.DOTALL),
]
extracted = []

def make_replacer():
		def repl(m):
				extracted.append(m.group(1))
				return f"__QUOTED_{len(extracted)-1}__"
		return repl

with open(INPUT_FILE, "r", encoding="utf-8") as f:
		data = f.read()
for pat in patterns:
		data = pat.sub(make_replacer(), data)
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
		f.write(data)
with open(LIST_FILE, "w", encoding="utf-8") as f:
		f.write("\n".join(extracted))
