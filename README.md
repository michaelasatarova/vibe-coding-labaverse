## Prerequisites

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) package manager
- OpenAI API key from https://platform.openai.com/api-keys

## Setup

Copy `.env.example` to `.env` in the subfolder you want to run and fill in your API key:

```bash
cp .env.example <subfolder>/.env
```

## Run

In each subfolder:

```bash
uv run main.py
```
