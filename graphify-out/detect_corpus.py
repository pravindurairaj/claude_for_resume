import json
from graphify.detect import detect
from pathlib import Path

result = detect(Path("."))
Path("graphify-out/.graphify_detect.json").write_text(json.dumps(result, indent=2))
files = result.get("files", {})
total = result.get("total_files", 0)
words = result.get("total_words", 0)
print(f"Total files : {total}")
print(f"Total words : {words:,}")
for cat, lst in files.items():
    if lst:
        exts = sorted(set(Path(f).suffix for f in lst))
        print(f"  {cat:<8}: {len(lst):3} files  {' '.join(exts)}")
skipped = result.get("skipped_sensitive", [])
if skipped:
    print(f"Skipped (sensitive): {len(skipped)} files")
