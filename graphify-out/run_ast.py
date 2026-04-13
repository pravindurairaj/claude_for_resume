import json
from graphify.extract import collect_files, extract
from pathlib import Path

detect = json.loads(Path("graphify-out/.graphify_detect.json").read_text())
code_files = [Path(f) for f in detect.get("files", {}).get("code", [])]
print(f"Extracting AST from {len(code_files)} code files...")
result = extract(code_files)
Path("graphify-out/.graphify_ast.json").write_text(json.dumps(result, indent=2))
print(f"AST: {len(result['nodes'])} nodes, {len(result['edges'])} edges")
