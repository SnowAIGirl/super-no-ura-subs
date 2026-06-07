#!/usr/bin/env python3
"""Add proper Chinese punctuation to all .ass subtitle files - fixed version."""
import re, os, subprocess, sys

os.chdir("/Users/linquan/works/super-no-ura-subs")

def add_punct(text):
    """Add appropriate ending punctuation to dialogue text."""
    t = text.strip()
    if not t:
        return text
    if t[-1] in "。？！…":
        return text
    if t[-1] in "，":
        return text
    if t.endswith("——") or t.endswith("——！") or t.endswith("——？") or t.endswith("——）"):
        return text
    if t[-1] in "～~":
        return text
    
    # Question
    if t[-1] in "吗么":
        return text + "？"
    if t.endswith("呢"):
        if any(w in t for w in ["哪儿", "哪里", "怎么", "什么", "谁", "啥"]):
            return text + "？"
        return text + "。"
    
    # Exclamation-like
    if t[-1] in "啊呀啦哦哟":
        if any(w in t for w in ["太", "这么", "那么", "好", "真", "靠", "哇", "我去"]):
            return text + "！"
        return text + "。"
    
    # Common endings
    if t[-1] in "了":
        return text + "。"
    if t[-1] in "吧":
        return text + "。"
    if t[-1] in "的":
        return text + "。"
    
    # Everything else
    return text + "。"


def process_file(filepath):
    with open(filepath, "r", newline="\n") as f:
        lines = f.readlines()
    
    out_lines = []
    changes = 0
    
    for line in lines:
        if not line.startswith("Dialogue:"):
            out_lines.append(line)
            continue
        
        parts = line.split(",", 9)
        if len(parts) != 10:
            out_lines.append(line)
            continue
        
        style = parts[4]
        if style in ("SIGN", "CREDITS", "CreditInfo", ""):
            out_lines.append(line)
            continue
        
        raw_text = parts[9]
        # Strip ASS override tags
        clean = re.sub(r'\{[^}]*\}', '', raw_text).strip()
        
        # Skip ASS effect lines
        if "\\pos" in raw_text or "\\move" in raw_text or "\\t(" in raw_text:
            out_lines.append(line)
            continue
        if not clean:
            out_lines.append(line)
            continue
        
        new_text = add_punct(clean)
        if new_text != clean:
            # Preserve newline that readlines() kept
            ending = "\n" if line.endswith("\n") else ""
            new_line = ",".join(parts[:9]) + "," + new_text + ending
            out_lines.append(new_line)
            changes += 1
        else:
            out_lines.append(line)
    
    with open(filepath, "w", newline="\n") as f:
        f.writelines(out_lines)
    
    return changes


# Process all 12 episodes
for ep in range(1, 13):
    fn = f"EP{ep:02d}.ass"
    if not os.path.exists(fn):
        print(f"SKIP {fn}")
        continue
    changes = process_file(fn)
    print(f"{fn}: {changes} changes")

print("\nDone. All files should be clean now.")
