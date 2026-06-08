#!/usr/bin/env python3
import re

with open("EP11.ass") as f:
    content = f.read()

# Replace "What?。" with "什么？" only on Dialogue lines
old = 'What?。'
new = '什么？'
content = content.replace(old, new)

with open("EP11.ass", "w") as f:
    f.write(content)

# Verify
with open("EP11.ass") as f:
    lines = f.readlines()

dialogue_lines = sum(1 for l in lines if l.startswith("Dialogue:"))
dialogue_occurrences = sum(l.count("Dialogue:") for l in lines)

print(f"Dialogue lines starting with 'Dialogue:': {dialogue_lines}")
print(f"Total 'Dialogue:' occurrences: {dialogue_occurrences}")
print(f"Clean: {'✅' if dialogue_lines == dialogue_occurrences else '❌'}")

if "What?" in content:
    print("❌ Still has 'What?'")
else:
    print("✅ Replaced 'What?' with '什么？'")
