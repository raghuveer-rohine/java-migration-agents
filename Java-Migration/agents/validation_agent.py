import subprocess
import re
from pathlib import Path
from agents.rewrite_agent import rewrite_file


JAVA_ERROR_PATTERN = re.compile(
    r'(?P<file>[^:\s]+\.java):\d+:\s+error'
)


def run_gradle_build(project_root: Path) -> tuple[bool, str]:
    result = subprocess.run(
        ["./gradlew", "build"],
        cwd=project_root,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )
    success = result.returncode == 0
    return success, result.stdout


def extract_failed_java_files(build_output: str) -> set[str]:
    files = set()
    for match in JAVA_ERROR_PATTERN.finditer(build_output):
        files.add(match.group("file"))
    return files


def run_validation_agent(
    old_project_root: str,
    new_project_root: str,
    max_iterations: int = 5
):
    old_root = Path(old_project_root)
    new_root = Path(new_project_root)

    print("🔍 Starting Validation Agent")

    for iteration in range(1, max_iterations + 1):
        print(f"\n🔁 Build attempt {iteration}")

        success, output = run_gradle_build(new_root)

        if success:
            print("✅ BUILD SUCCESSFUL")
            return

        print("❌ Build failed, analyzing errors...")

        failed_files = extract_failed_java_files(output)

        if not failed_files:
            print("🚨 Non-Java or unrecoverable error detected")
            print(output)
            return

        for file_path in failed_files:
            new_file = new_root / file_path
            old_file = old_root / file_path

            if not old_file.exists():
                print(f"⚠️ Cannot repair (missing source): {file_path}")
                continue

            print(f"🛠️ Repairing: {file_path}")
            rewrite_file(old_file, new_file)

    print("❌ Max repair attempts reached. Manual intervention needed.")
