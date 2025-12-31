import re

INPUT_FILE = "output.js"
EXTRACTED_FILE = "extracted.txt"
RESTORED_FILE = "restored.js"
DELIM = "__DELIM__"

with open(EXTRACTED_FILE, "r", encoding="utf-8") as f:
    extracted = f.read().split(DELIM)
pattern = re.compile(r"__QUOTED_(\d+)__")
def replacer(match):
    index = int(match.group(1))
    return extracted[index]
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    data = f.read()
restored = pattern.sub(replacer, data)
with open(RESTORED_FILE, "w", encoding="utf-8") as f:
    f.write(restored)
