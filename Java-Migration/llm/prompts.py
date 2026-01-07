def planner_prompt(build_gradle: str, settings_gradle: str, tree: str) -> str:
    return f"""
You are a Java migration planner agent.

You MUST analyze the project and produce a migration plan.

Rules:
- DO NOT suggest code changes
- DO NOT rewrite anything
- DO NOT include explanations
- You MUST return ONLY valid JSON
- Do not use markdown
- Do not add extra fields
- If unsure, choose the safer option

You must determine and OUTPUT ALL of the following fields:

{{
  "current_java": number,
  "target_java": number,
  "current_spring_boot": string or null,
  "target_spring_boot": string,
  "project_type": "spring-boot" | "spring" | "plain-java",
  "modules": array of strings,
  "uses_web": boolean,
  "uses_security": boolean,
  "uses_jpa": boolean,
  "risk_level": "low" | "medium" | "high"
}}

Target selection rules:
- target_java MUST be 17
- target_spring_boot MUST be 3.2.x

--- build.gradle ---
{build_gradle}

--- settings.gradle ---
{settings_gradle}

--- project structure ---
{tree}
"""


def build_gradle_migration_prompt(old_build: str, plan: dict) -> str:
    return f"""
You are a Build Migration Agent.

Task:
Rewrite the given build.gradle file to be compatible with:

- Java {plan["target_java"]}
- Spring Boot {plan["target_spring_boot"]}
- Gradle 8.x

Rules:
- DO NOT add new dependencies
- DO NOT remove existing dependencies
- DO NOT change dependency coordinates except where REQUIRED
- DO NOT rewrite project structure
- Preserve comments and formatting as much as possible
- Use Java toolchains (do NOT use sourceCompatibility)

You MUST output ONLY the full updated build.gradle content.
No explanations. No markdown.

--- OLD build.gradle ---
{old_build}
"""



def source_classification_prompt(file_path: str, file_content: str) -> str:
    return f"""
You are a Java migration classifier.

Context:
- Source Java version: 8
- Target Java version: 17
- Spring Boot: 3.x
- javax → jakarta is required

Task:
Classify the following Java file into ONE category only:
1. NO_CHANGE
2. MINOR_FIX (imports, deprecated API)
3. MAJOR_REWRITE (javax, removed APIs, Spring config)
4. REMOVE (obsolete / unused)

Rules:
- DO NOT rewrite code
- DO NOT suggest improvements
- Be conservative
- Output ONLY the classification word

File path:
{file_path}

File content:
{file_content}
"""


def rewrite_java_file_prompt(old_code: str) -> str:
    return f"""
You are a Java migration rewrite agent.

Task:
Rewrite the following Java file to be compatible with:
- Java 17
- Spring Boot 3.x

STRICT RULES:
- Preserve package name
- Preserve class name
- Preserve public method signatures
- Preserve fields and annotations
- Do NOT refactor
- Do NOT optimize
- Do NOT introduce new language features
- Please remove any unused imports
- Replace javax.* with jakarta.* where required
- Fix only compilation-breaking issues

Output requirements:
- Output ONLY the full rewritten Java file
- No explanations
- No markdown
- No comments added

--- ORIGINAL JAVA FILE ---
{old_code}
"""