"""
Parallel Code Review Pipeline - Fan-Out/Fan-In Pattern

A pull request diff is distributed to four specialist reviewers running
in parallel, then a synthesizer combines their findings into a single
prioritized review report.

Pattern:
                  -> Security Reviewer   ->
                  -> Performance Reviewer ->
PR Diff (input) ->                          -> Synthesizer -> Unified Report
                  -> Style Reviewer      ->
                  -> Test Coverage       ->

Usage:
    python3 workflow.py
"""

import anyio

from claude_cli import call_claude

# Sample PR diff used as input when running standalone
SAMPLE_DIFF = """
diff --git a/auth/login.py b/auth/login.py
--- a/auth/login.py
+++ b/auth/login.py
@@ -1,20 +1,35 @@
+import hashlib
+import sqlite3
+
 def login(username, password):
-    # TODO: implement real auth
-    return True
+    conn = sqlite3.connect("users.db")
+    cursor = conn.cursor()
+    query = f"SELECT * FROM users WHERE username = '{username}'"
+    cursor.execute(query)
+    user = cursor.fetchone()
+    if user is None:
+        return False
+    stored_hash = user[2]
+    input_hash = hashlib.md5(password.encode()).hexdigest()
+    return stored_hash == input_hash
+
+def get_user_data(user_id):
+    conn = sqlite3.connect("users.db")
+    cursor = conn.cursor()
+    rows = cursor.execute("SELECT * FROM users").fetchall()
+    result = []
+    for r in rows:
+        result.append(r)
+    return result
"""


async def run_reviewer(name: str, specialty: str, prompt: str) -> tuple[str, str]:
    """Run a single reviewer agent in its own isolated session."""
    print(f"[{name}] Starting review...")

    full_prompt = (
        f"You are a {specialty} specialist conducting a code review. "
        "Be concise, specific, and actionable. Reference exact line numbers or "
        f"code snippets where relevant.\n\n{prompt}"
    )

    try:
        result = await anyio.to_thread.run_sync(lambda: call_claude(full_prompt))
        print(f"[{name}] Review complete")
        return name, result
    except Exception as exc:
        print(f"[{name}] Review failed: {exc}")
        return name, f"[Review failed: {exc}]"


async def code_review_pipeline(diff: str) -> None:
    """
    Parallel code review: four specialists review the same diff simultaneously,
    then a synthesizer produces a unified report with prioritized action items.

    Fan-Out: Distribute the diff to specialist reviewers
    Fan-In:  Collect findings and synthesize into a single report
    """

    print("=" * 60)
    print("PARALLEL CODE REVIEW PIPELINE")
    print("=" * 60)
    print(f"\nReviewing diff ({len(diff.splitlines())} lines)\n")

    reviewers = [
        {
            "name": "Security Reviewer",
            "specialty": "application security and secure coding practices",
            "prompt": (
                f"Review the following code diff for security issues:\n{diff}\n\n"
                "Focus on: SQL injection, authentication flaws, insecure hashing, "
                "hardcoded secrets, input validation, and any other vulnerabilities. "
                "Rate severity (Critical / High / Medium / Low) for each finding."
            ),
        },
        {
            "name": "Performance Reviewer",
            "specialty": "software performance and efficiency",
            "prompt": (
                f"Review the following code diff for performance issues:\n{diff}\n\n"
                "Focus on: unnecessary DB queries, missing indexes hints, inefficient "
                "loops, resource leaks (unclosed connections), and scalability concerns."
            ),
        },
        {
            "name": "Style Reviewer",
            "specialty": "code quality, readability, and maintainability",
            "prompt": (
                f"Review the following code diff for style and maintainability:\n{diff}\n\n"
                "Focus on: naming conventions, function responsibilities, code duplication, "
                "missing error handling, and adherence to clean code principles."
            ),
        },
        {
            "name": "Test Coverage Reviewer",
            "specialty": "software testing and quality assurance",
            "prompt": (
                f"Review the following code diff for test coverage gaps:\n{diff}\n\n"
                "Focus on: missing unit tests, untested edge cases (empty input, wrong types, "
                "concurrent access), and suggest specific test scenarios that should be added."
            ),
        },
    ]

    print("PHASE 1: Fan-Out — Parallel Review")
    print("-" * 60)

    # Fan-Out: run all reviewers in parallel
    findings: list[tuple[str, str]] = []

    async with anyio.create_task_group() as tg:
        async def run_and_collect(reviewer: dict) -> None:
            result = await run_reviewer(
                reviewer["name"], reviewer["specialty"], reviewer["prompt"]
            )
            findings.append(result)

        for reviewer in reviewers:
            tg.start_soon(run_and_collect, reviewer)

    print("\nPHASE 2: Fan-In — Collecting Findings")
    print("-" * 60)

    aggregated = ""
    for name, text in findings:
        print(f"\n### {name}:")
        print(f"{text[:300]}..." if len(text) > 300 else text)
        aggregated += f"\n\n### {name}:\n{text}"

    # Fan-In: synthesize all findings into a single report
    print("\nPHASE 3: Synthesis — Unified Review Report")
    print("-" * 60)

    synthesis_prompt = f"""You are a senior engineering lead synthesizing parallel code review findings.
Deduplicate overlapping points, resolve conflicting recommendations, and produce
a clear, prioritized review report.

You have received code review findings from four specialist reviewers for the same diff.
Combine them into a single, actionable PR review report.

Diff under review:
{diff}

Specialist findings:
{aggregated}

Your report must include:
1. **Executive Summary** — 2-3 sentence overall assessment
2. **Critical / Blocking Issues** — must be fixed before merge
3. **Important Issues** — should be fixed soon
4. **Minor Suggestions** — nice to have
5. **Verdict** — one of: APPROVE / REQUEST CHANGES / NEEDS DISCUSSION
"""

    print("\nUnified Review Report:\n")
    report = await anyio.to_thread.run_sync(lambda: call_claude(synthesis_prompt))
    print(report)

    print("\n")
    print("=" * 60)
    print("Code review pipeline completed!")
    print("=" * 60)


if __name__ == "__main__":
    anyio.run(code_review_pipeline, SAMPLE_DIFF)
