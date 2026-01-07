# Java Migration Agent Framework 🚀

This repository contains a **multi-agent AI system** designed to **safely and deterministically migrate Java + Spring Boot projects** (e.g., Java 8 → Java 17, Spring Boot 2.x → 3.x).

Instead of using one large LLM, this project uses **multiple focused agents**, each responsible for a single decision domain.  
Agents communicate via **files and shared state**, not chat — making the system auditable, debuggable, and repeatable.

---

## 🧠 Core Philosophy

- One agent = one responsibility
- Decisions are explicit and persisted
- Code changes are minimal and controlled
- LLMs decide *what* to change, tools do the actual work

This is **agentic AI**, not prompt-driven code generation.

---

### 🔒 Migration Safety Model (IMPORTANT)

This framework follows a **strict reference–copy migration model** to guarantee safety and reversibility.

**Key rule:**

> ⚠️ The original Java project is treated as a **read-only reference** and is **never modified**.

#### How migration works

1. **Base (Reference) Project**

   * Original project (e.g. Java 8 / Spring Boot 2.x)
   * Used only for:

     * Analysis
     * Classification
     * Rewrite reference
   * **Never changed by any agent**

2. **Migration Target Project**

   * A **full copy** of the base project in a separate directory
   * All build upgrades, rewrites, and fixes are applied **only here**
   * This is the project that becomes Java 17 / Spring Boot 3.x

#### Why this matters

* Guarantees **zero risk** to the original codebase
* Allows:

  * Side-by-side comparison
  * Easy rollback
  * Deterministic reruns
* Enables agents to reason safely without fear of corruption

All agents are **contractually bound** to respect this separation.

---

## 🏗️ Agent Architecture

### 1️⃣ Planner Agent
**Responsibility:** Decide *what needs to be done*

- Reads:
    - Project structure
    - Java version
    - Spring Boot version
- Outputs:
    - Migration plan (`migration_plan.json`)
    - Target Java & Spring versions
    - Risk assessment

---

### 2️⃣ Build Migration Agent
**Responsibility:** Make the project buildable on the target Java version

- Updates:
    - `build.gradle`
    - `gradle-wrapper.properties`
- Upgrades:
    - Gradle
    - Spring Boot
    - Dependency versions

---

### 3️⃣ Source Classifier Agent
**Responsibility:** Decide *which source files need changes*

Each Java file is classified as:
- `NO_CHANGE`
- `MINOR_FIX`
- `MAJOR_REWRITE`
- `REMOVE`

Output is a structured JSON map for full visibility.

---

### 4️⃣ Rewrite Agent
**Responsibility:** Rewrite **only what is required**

Strict rules:
- Same package & class name
- Same public APIs
- Java 17 + Spring 3 compatible
- `javax.*` → `jakarta.*`
- No creative refactoring

---

### 5️⃣ Validation / Repair Agent
**Responsibility:** Ensure the project builds

- Runs:
  ```bash
  ./gradlew build

* Feeds compilation errors back to the Rewrite Agent
* Loops until:

    * Build succeeds, or
    * Error is non-recoverable

---

## 🔄 Overall Flow

```text
Planner Agent
      ↓
Build Migration Agent
      ↓
Source Classifier Agent
      ↓
Rewrite Agent
      ↓
Validation Agent
      ↺ (loops on failure)
```

Human intervention is only needed at the end.

---

## 🧩 Project Structure

```text
agents/
  planner_agent.py
  build_agent.py
  classifier_agent.py
  rewrite_agent.py
  validation_agent.py

migration_state/
  migration_plan.json
  classification.json

notebooks/
  migration.ipynb

pyproject.toml
```

---

## ⚙️ Initial Setup

### 1️⃣ Install Python

Ensure Python 3.10+ is installed.

```bash
python --version
```

---

### 2️⃣ Install `uv`

`uv` is used for fast, reproducible dependency management.

```bash
pip install uv
```

---

### 3️⃣ Install Cursor IDE

This project is designed to work seamlessly with **Cursor IDE** for AI-assisted development.

---

### 4️⃣ Sync dependencies

From the project root:

```bash
uv sync
```

This installs all dependencies defined in `pyproject.toml`.

---

### 5️⃣ Select the correct Python environment

1. Open any `.ipynb` file
2. Go to **Kernel → Select Kernel**
3. Choose:

   ```
   python .envs
   ```

---

## ▶️ Running the Migration

⚠️ IMPORTANT:
Always pass the **original project path** as the reference input,
and run all migration steps on a **separately copied project directory**.

Example entry point:

```python
from agents.planner_agent import run_planner_agent

PROJECT_ROOT = "/path/to/java-project"
OUTPUT_PLAN = "migration_state/migration_plan.json"

run_planner_agent(PROJECT_ROOT, OUTPUT_PLAN)
```

Each agent produces structured outputs that are consumed by the next agent in the pipeline.

---

## 🧠 What This Is (and Is Not)

✅ This **is**:

* Deterministic
* Debuggable
* Auditable
* Production-oriented

❌ This is **not**:

* “LLM magically rewrites your code”
* Chat-based code generation
* Uncontrolled refactoring

---

## 🚧 Status

This project is under active development.
The **Source Classifier Agent** is the recommended first extension point.

---

## 📌 Next Steps

* Add CI integration
* Add dry-run mode
* Add rollback support
* Add metrics for migration confidence

---

## 🤝 Contributions

Contributions are welcome.
Focus areas:

* Agent prompts
* Validation strategies
* Edge-case handling

---

**Real migrations need control, not creativity.**
This repo is built with that principle.

```
