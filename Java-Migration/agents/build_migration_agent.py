from pathlib import Path
import json
import re
from llm.llm_factory import get_llm_response
from llm.prompts import build_gradle_migration_prompt


def load_plan(plan_path: str) -> dict:
    with open(plan_path, "r") as f:
        return json.load(f)


def upgrade_gradle_wrapper(project_root: Path, gradle_version="8.6"):
    wrapper_file = project_root / "gradle/wrapper/gradle-wrapper.properties"

    if not wrapper_file.exists():
        raise FileNotFoundError("gradle-wrapper.properties not found")

    content = wrapper_file.read_text()

    content = re.sub(
        r"distributionUrl=.*",
        f"distributionUrl=https\\://services.gradle.org/distributions/gradle-{gradle_version}-bin.zip",
        content
    )

    wrapper_file.write_text(content)
    print(f"✅ Gradle wrapper upgraded to {gradle_version}")


def upgrade_build_gradle_llm(project_root: Path, plan: dict):
    build_file = project_root / "build.gradle"
    old_build = build_file.read_text()

    prompt = build_gradle_migration_prompt(old_build, plan)
    new_build = get_llm_response(prompt)

    build_file.write_text(new_build)
    print("✅ build.gradle regenerated via LLM")


def run_build_migration_agent(project_root: str, plan_path: str):
    root = Path(project_root)
    plan = load_plan(plan_path)

    target_java = int(plan["target_java"])
    target_boot = plan["target_spring_boot"]

    print("🔧 Running Build Migration Agent")
    print(f"→ Target Java: {target_java}")
    print(f"→ Target Spring Boot: {target_boot}")

    upgrade_gradle_wrapper(root)
    upgrade_build_gradle_llm(root, plan)

    print("✅ Build migration completed")
