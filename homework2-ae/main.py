#!/usr/bin/env python3
"""Agent Orchestration — Supervisor Pattern.

A supervisor agent coordinates specialized subagents (Search, Code, Writer)
via an explicit control loop. The supervisor decides which subagent to call
next, constructs a task, collects the result, and repeats until it has
enough information to produce a final answer.

Key Characteristics:
- Hierarchical structure (supervisor leads)
- Supervisor explicitly chooses which subagent to call next
- Each subagent runs in its own isolated context
- Subagents report results back to the supervisor only
- No direct communication between subagents
- Structured output drives the supervisor's decisions

Usage:
    python3 main.py
"""

import json
import re
import sys

from claude_cli import call_claude


# ── Agent definitions ────────────────────────────────────────────────────────

class AgentDefinition:
    """Holds the configuration for a single agent."""

    def __init__(self, description: str, prompt: str):
        self.description = description
        self.prompt = prompt


# ── Subagents ────────────────────────────────────────────────────────────────

def run_subagent(agent_name: str, defn: AgentDefinition, task: str) -> str:
    """Run a subagent in its own isolated context and return its response."""
    print(f"\n{'-'*40}")
    print(f"Subagent: {agent_name}")
    print(f"{'-'*40}")

    prompt = f"""You are a {defn.description}.

{defn.prompt}

Your supervisor has assigned you this task:
{task}

Complete this task and report your findings."""

    result = call_claude(prompt)
    print(f"  {agent_name}: {result}")
    return result


# ── Supervisor team ──────────────────────────────────────────────────────────

class SupervisorTeam:
    """Manages a team of agents under a supervisor with an explicit control loop.

    Each iteration the supervisor returns a structured decision: either
    delegate to a subagent (with a constructed task) or finish with a
    final answer. Subagents never communicate directly with each other.
    """

    MAX_ITERATIONS = 10

    def __init__(
        self,
        supervisor_name: str,
        supervisor_definition: AgentDefinition,
        team_agents: dict,
    ):
        self.supervisor_name = supervisor_name
        self.supervisor_definition = supervisor_definition
        self.team_agents = team_agents

    def _supervisor_decide(self, context: str) -> dict:
        """Ask the supervisor to make a structured decision."""
        agent_names_list = ", ".join(self.team_agents.keys())

        prompt = f"""{self.supervisor_definition.prompt}

{context}

You MUST respond with ONLY a JSON code block — no other text before or after it.

To delegate to a subagent:
```json
{{"action": "delegate", "delegate_to": "<one of: {agent_names_list}>", "task": "<specific task>"}}
```

To return the final answer:
```json
{{"action": "finish", "answer": "<complete final answer for the user>"}}
```"""

        response = call_claude(prompt)

        # Extract JSON from ```json ... ``` block
        match = re.search(r"```json\s*(\{.*?\})\s*```", response, re.DOTALL)
        if match:
            try:
                parsed = json.loads(match.group(1))
            except json.JSONDecodeError as exc:
                raise ValueError(f"Supervisor returned invalid JSON: {exc}\nRaw: {response}") from exc
        else:
            # Fallback: find raw JSON object
            start = response.find("{")
            end = response.rfind("}") + 1
            if start == -1 or end == 0:
                raise ValueError(f"No JSON found in supervisor response: {response}")
            try:
                parsed = json.loads(response[start:end])
            except json.JSONDecodeError as exc:
                raise ValueError(f"Supervisor returned invalid JSON: {exc}\nRaw: {response}") from exc

        action = parsed.get("action")
        if action == "finish":
            print(f"Supervisor output: {parsed.get('answer', '')}")
        elif action == "delegate":
            print(f"Supervisor output: delegating to '{parsed.get('delegate_to')}' — {parsed.get('task', '')}")

        return parsed

    def execute(self, initial_task: str) -> str:
        """Execute the supervisor pattern with the initial task.

        The supervisor loops: decide → delegate → collect → repeat.
        Ends when the supervisor chooses action='finish' or MAX_ITERATIONS is reached.
        """
        team_info = "\n".join([
            f"- {name}: {defn.description}"
            for name, defn in self.team_agents.items()
        ])
        agent_names_list = ", ".join(self.team_agents.keys())

        history = f"Task to accomplish:\n{initial_task}"

        for iteration in range(1, self.MAX_ITERATIONS + 1):
            print(f"\n{'='*60}")
            print(f"Supervisor: {self.supervisor_name} (iteration {iteration}/{self.MAX_ITERATIONS})")
            print(f"{'='*60}")

            context = f"""You are a supervisor managing a team of specialized agents.

Your responsibility: {self.supervisor_definition.description}

Your team members (delegate to any by name):
{team_info}

{history}

Decide your next step: delegate to one of ({agent_names_list}) or finish."""

            structured_result = self._supervisor_decide(context)

            if structured_result.get("action") == "finish":
                answer = structured_result.get("answer", "")
                print(f"\n>>> Supervisor finished after {iteration} iteration(s).")
                return answer

            agent_name = structured_result.get("delegate_to", "")
            task = structured_result.get("task", "")

            if agent_name not in self.team_agents:
                history += f"\n\nError: Unknown agent '{agent_name}'. Available: {agent_names_list}"
                continue

            subagent_result = run_subagent(agent_name, self.team_agents[agent_name], task)

            history += (
                f"\n\nYou delegated to '{agent_name}' with task: {task}"
                f"\nResult from {agent_name}:\n{subagent_result}"
            )

        print(f"\n>>> Max iterations ({self.MAX_ITERATIONS}) reached.")
        return history


# ── Demo ─────────────────────────────────────────────────────────────────────

def run(user_task: str):
    print("\n" + "="*60)
    print("ORCHESTRATION DEMO — Supervisor Pattern")
    print("="*60)

    supervisor = AgentDefinition(
        description="Orchestrator that breaks down tasks and delegates to the right specialist",
        prompt=(
            "You are an orchestrator managing a team of specialists. "
            "Break down the user's task, delegate to the right subagent, "
            "and produce a final, polished answer."
        ),
    )

    team = {
        "search_agent": AgentDefinition(
            description="Research agent — returns 3-4 concise bullet points of key facts",
            prompt=(
                "You are a research agent. Given a query, return 3-4 short bullet points "
                "of key facts. Be concise and factual."
            ),
        ),
        "code_agent": AgentDefinition(
            description="Coding agent — writes a short, clean Python snippet",
            prompt=(
                "You are a coding agent. Write a short, clean Python code snippet "
                "that solves the given task. Include a brief comment explaining what it does."
            ),
        ),
        "writer_agent": AgentDefinition(
            description="Writer agent — synthesizes raw content into a clear human-friendly summary",
            prompt=(
                "You are a writer agent. Take raw research or technical content and turn it "
                "into a clear, concise, human-friendly summary in 3-4 sentences."
            ),
        ),
    }

    team_instance = SupervisorTeam("orchestrator", supervisor, team)
    result = team_instance.execute(user_task)

    print("\n" + "="*60)
    print("FINAL ANSWER:")
    print("="*60)
    print(result)


if __name__ == "__main__":
    tasks = [
        "What is quantum computing and why does it matter?",
        "Write a Python function to calculate compound interest",
    ]

    if len(sys.argv) > 1:
        run(" ".join(sys.argv[1:]))
    else:
        for task in tasks:
            run(task)
            print()
