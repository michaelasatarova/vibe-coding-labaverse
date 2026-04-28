import subprocess


def call_claude(prompt: str) -> str:
    """Call the claude CLI and return its response text."""
    result = subprocess.run(
        ["claude", "--print"],
        input=prompt,
        capture_output=True,
        text=True,
        timeout=120,
    )
    if result.returncode != 0:
        raise RuntimeError(f"Claude CLI error: {result.stderr or result.stdout or '(no output)'}")
    return result.stdout.strip()
