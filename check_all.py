#!/usr/bin/env python3
"""Comprehensive check of all 12 .ass subtitle files."""
import re, os

base = "/Users/linquan/works/super-no-ura-subs"
issues = {}

for ep in range(1, 13):
    fn = os.path.join(base, f"EP{ep:02d}.ass")
    with open(fn) as f:
        content = f.read()
        lines = content.split("\n")
    
    ep_issues = []
    
    # 1. Check merged lines
    dialogue_count = 0
    merged_count = 0
    for line in lines:
        if line.startswith("Dialogue:"):
            dialogue_count += 1
        c = line.count("Dialogue:")
        if c > 1:
            merged_count += 1
            ep_issues.append(f"⚠️  {merged_count} merged lines")
            break
    
    # 2. Check all dialogue lines for punctuation and English
    total_dlg = 0
    no_punct = []
    english_words = []
    
    for line in lines:
        if not line.startswith("Dialogue:"):
            continue
        parts = line.split(",", 9)
        if len(parts) != 10:
            continue
        style = parts[4].strip()
        text = parts[9]
        
        # Strip ASS tags
        clean = re.sub(r'\{[^}]*\}', '', text).strip()
        if not clean:
            continue
        
        # Skip Signs, Credits, CreditInfo - they're not dialogue
        if style in ("SIGN", "CREDITS", "CreditInfo"):
            continue
        
        total_dlg += 1
        
        # Check punctuation
        last = clean.rstrip()[-1] if clean.rstrip() else ""
        has_punct = last in "。？！…，" or clean.rstrip().endswith("——") or last in "～~"
        if not has_punct:
            no_punct.append(clean[:50])
        
        # Check for English words in dialogue text (not ASS tags)
        # Only check lines that are mostly Chinese
        if re.search(r'[\u4e00-\u9fff]', clean):  # Has Chinese chars
            # Find English words (3+ letters)
            eng = re.findall(r'\b[a-zA-Z]{3,}\b', clean)
            if eng:
                english_words.append((clean[:50], eng))
    
    if no_punct:
        ep_issues.append(f"❌ {len(no_punct)} dialogues missing punctuation")
        for np in no_punct[:5]:
            ep_issues.append(f"   • {np}")
    
    if english_words:
        ep_issues.append(f"❌ {len(english_words)} lines with English words")
        for text, words in english_words[:5]:
            ep_issues.append(f"   • [{','.join(words)}] {text}")
    
    # 3. Check CreditInfo style
    if "Style: CreditInfo" not in content:
        ep_issues.append("❌ Missing CreditInfo style")
    
    # 4. Check both credits exist
    credit_count = content.count("制作信息")
    if credit_count < 2:
        ep_issues.append(f"❌ Only {credit_count}/2 制作信息 credits")
    
    # 5. Check file structure
    if "[Events]" not in content:
        ep_issues.append("❌ Missing [Events]")
    if "[V4+ Styles]" not in content:
        ep_issues.append("❌ Missing [V4+ Styles]")
    
    # Report
    if ep_issues:
        issues[ep] = ep_issues
        print(f"\n❌ EP{ep:02d} ({total_dlg} dialogues)")
        for iss in ep_issues:
            print(f"  {iss}")
    else:
        print(f"✅ EP{ep:02d} ({total_dlg} dialogues, all clean)")

print(f"\n{'='*50}")
if issues:
    print(f"❌ Issues found in {len(issues)} episodes")
    for ep in sorted(issues.keys()):
        print(f"  EP{ep:02d}: {len(issues[ep])} issue(s)")
else:
    print("✅ All 12 episodes clean!")
