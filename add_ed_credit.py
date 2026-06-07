#!/usr/bin/env python3
"""Add translation credit at the start of each episode's ending song."""
import re

CREDIT_TEXT = "\\N制作信息\\N翻译：AI女孩小雪（https://github.com/SnowAIGirl）\\N时间轴：基于 Crunchyroll 官方字幕\\N语音识别：faster-whisper（日语→中文直译）\\N\\N本字幕仅供学习交流，请勿用于商业用途。如侵权请联系删除。"

def time_to_sec(t):
    """Convert H:MM:SS.cc to seconds."""
    parts = t.split(":")
    if len(parts) == 3:
        h, m, s = parts
        sec = float(s)
    elif len(parts) == 2:
        h = "0"
        m, s = parts
        sec = float(s)
    else:
        return 0
    return int(h) * 3600 + int(m) * 60 + sec

def sec_to_time(s):
    """Convert seconds to ASS format H:MM:SS.cc"""
    h = int(s // 3600)
    s = s % 3600
    m = int(s // 60)
    sec = s % 60
    return f"{h}:{m:02d}:{sec:05.2f}"

for ep in range(1, 13):
    with open(f"EP{ep:02d}.ass") as f:
        lines = f.readlines()
    
    # Find the end of the last dialogue
    last_dialogue_end = "0:00:00.00"
    for line in lines:
        if line.startswith("Dialogue:"):
            parts = line.split(",", 9)
            if len(parts) > 9:
                end = parts[2].strip()
                style = parts[4].strip()
                if style not in ("SIGN", "CREDITS", "CreditInfo", ""):
                    if end > last_dialogue_end:
                        last_dialogue_end = end
    
    # Place credit 4.5 seconds after last dialogue ends, for 10 seconds
    start_sec = time_to_sec(last_dialogue_end) + 4.5
    end_sec = start_sec + 10.0
    
    credit_line = f"Dialogue: 0,{sec_to_time(start_sec)},{sec_to_time(end_sec)},CreditInfo,,0,0,0,,{CREDIT_TEXT}\n"
    
    # Insert before the first CREDITS line, or append to end
    insert_at = None
    for i, line in enumerate(lines):
        if line.startswith("Dialogue:") and "CREDITS" in line:
            insert_at = i
            break
    
    if insert_at is not None:
        lines.insert(insert_at, credit_line)
    else:
        lines.append(credit_line)
    
    with open(f"EP{ep:02d}.ass", "w", newline="\n") as f:
        f.writelines(lines)
    
    print(f"EP{ep:02d}: credit at {sec_to_time(start_sec)} -> {sec_to_time(end_sec)} (ED start)")
