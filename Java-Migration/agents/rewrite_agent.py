import json
from pathlib import Path
from llm.llm_factory import get_llm_response
from llm.prompts import rewrite_java_file_prompt


def load_json(path: str) -> dict:
    with open(path, "r") as f:
        return json.load(f)


def extract_package_and_class(java_code: str):
    package_line = None
    class_name = None

    for line in java_code.splitlines():
        if line.strip().startswith("package "):
            package_line = line.strip()
        if " class " in line:
            class_name = line.strip()
            break

    return package_line, class_name


def rewrite_file(old_file: Path, new_file: Path):
    old_code = old_file.read_text(encoding="utf-8", errors="ignore")

    prompt = rewrite_java_file_prompt(old_code)
    new_code = get_llm_response(prompt)

    # ---- Safety checks ----
    old_pkg, old_class = extract_package_and_class(old_code)
    new_pkg, new_class = extract_package_and_class(new_code)

    if not new_code.strip():
        raise RuntimeError(f"Rewrite failed (empty output): {old_file}")

    if old_pkg and old_pkg not in new_code:
        raise RuntimeError(f"Package mismatch in {old_file}")

    if old_class and old_class.split("{")[0] not in new_code:
        raise RuntimeError(f"Class name mismatch in {old_file}")

    # Write rewritten file
    new_file.parent.mkdir(parents=True, exist_ok=True)
    new_file.write_text(new_code, encoding="utf-8")

    print(f"✍️ Rewritten: {old_file.name}")


def run_rewrite_agent(
    old_project_root: str,
    new_project_root: str,
    classification_path: str
):
    classification = load_json(classification_path)

    old_root = Path(old_project_root)
    new_root = Path(new_project_root)

    for file_path, decision in classification.items():
        if decision != "MAJOR_REWRITE":
            continue

        old_file = Path(file_path)

        # Map old path → new project path
        relative_path = old_file.relative_to(old_root)
        new_file = new_root / relative_path

        rewrite_file(old_file, new_file)

    print("✅ Rewrite Agent completed")
