import json
from pathlib import Path
from llm.llm_factory import get_llm_response
from llm.prompts import source_classification_prompt

def classify_sources(src_root: str, output_file: str):
    results = {}

    for java_file in Path(src_root).rglob("*.java"):
        content = java_file.read_text(encoding="utf-8", errors="ignore")

        prompt = source_classification_prompt(
            str(java_file),
            content[:8000]  # safety limit
        )

        classification = get_llm_response(prompt).strip()
        results[str(java_file)] = classification

        print(f"[CLASSIFIED] {java_file} -> {classification}")

    Path(output_file).parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, "w") as f:
        json.dump(results, f, indent=2)
