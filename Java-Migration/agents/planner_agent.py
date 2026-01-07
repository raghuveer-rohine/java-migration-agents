import json
import time
from pathlib import Path
from llm.llm_factory import get_llm_response
from llm.prompts import planner_prompt


def read_file_safe(path: Path) -> str:
    if path.exists():
        return path.read_text(encoding="utf-8", errors="ignore")
    return ""


def generate_project_tree(root: Path, max_depth=4) -> str:
    lines = []

    for path in root.rglob("*"):
        try:
            depth = len(path.relative_to(root).parts)
            if depth > max_depth:
                continue
            prefix = "  " * depth
            lines.append(f"{prefix}{path.name}")
        except Exception:
            continue

    return "\n".join(lines)


def run_planner_agent(project_root: str, output_file: str):
    print("🚀 Planner agent started")
    start_time = time.time()

    root = Path(project_root)
    print(f"📂 Project root resolved: {root}")

    print("📄 Reading build.gradle...")
    build_gradle = read_file_safe(root / "build.gradle")
    print(f"   ✔ build.gradle loaded ({len(build_gradle)} chars)")

    print("📄 Reading settings.gradle...")
    settings_gradle = read_file_safe(root / "settings.gradle")
    print(f"   ✔ settings.gradle loaded ({len(settings_gradle)} chars)")

    print("🌲 Generating project tree...")
    tree = generate_project_tree(root)
    print(f"   ✔ Project tree generated ({len(tree)} chars)")

    print("🧠 Building planner prompt...")
    prompt = planner_prompt(
        build_gradle=build_gradle,
        settings_gradle=settings_gradle,
        tree=tree
    )
    print(f"   ✔ Prompt built ({len(prompt)} chars)")

    print("📡 Calling LLM (this may take time)...")
    llm_start = time.time()
    response = get_llm_response(prompt)
    print(f"   ✔ LLM response received in {time.time() - llm_start:.2f}s")
    print(f"   ✔ LLM response: {response}")
    print("🧾 Parsing LLM response as JSON...")
    plan = json.loads(response)
    print("   ✔ JSON parsed successfully")

    output_path = Path(output_file)
    print(f"💾 Preparing output path: {output_path.parent}")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"💾 Writing migration plan to file: {output_file}")
    with open(output_file, "w") as f:
        json.dump(plan, f, indent=2)

    print("✅ Migration plan generated successfully")
    print(f"⏱ Total time: {time.time() - start_time:.2f}s")
    print(json.dumps(plan, indent=2))
