# Road4AI

## Stop Renting Intelligence.

Road4AI is a zero-cost AI operator blueprint for builders who want local-first, CLI-native workflows instead of subscription-heavy dashboards.

Built for indie hackers, technical founders, and engineers who want to own the environment.

## Why Road4AI

Most AI products sell convenience by renting your workflow back to you. You pay monthly for a web UI wrapper, lose control of the environment, and end up with a stack you cannot fully inspect or own.

Road4AI takes the opposite position:

- **Zero-cost-first** by default
- **CLI-native** instead of dashboard-first
- **Local-first** where practical
- **Open-source** and inspectable
- **Safety-conscious** with repo verification built in

## What This Repo Gives You

- A zero-cost infrastructure blueprint in [`SYSTEM.md`](SYSTEM.md)
- The operator thesis in [`manifesto.md`](manifesto.md)
- Visual direction in [`DESIGN.md`](DESIGN.md)
- A Magika-based repository verifier in [`verify_repo.py`](verify_repo.py)

## Repository Verification

This repo includes an AI-powered repository auditor using **Google's Magika**. It scans forked or downloaded repositories to ensure file extensions match their actual content and to flag unexpected binaries before execution.

### Setup

Ensure Magika is installed:

```bash
python3 -m pip install magika
```

### Usage

Run the auditor on any directory:

```bash
python3 verify_repo.py /path/to/repo
```

The script will:

1. Identify the true file type of every file.
2. Flag **mismatches** such as an executable masquerading as a `.txt` file.
3. List all **binaries/executables** found in the codebase.

## Start Here

1. Read [`manifesto.md`](manifesto.md) to understand the Road4AI position.
2. Read [`SYSTEM.md`](SYSTEM.md) to inspect the zero-cost stack.
3. Run [`verify_repo.py`](verify_repo.py) on any repo you plan to trust.

## Who This Is For

Road4AI is for:

- Indie hackers tired of subscription creep
- Technical founders who want leverage without vendor lock-in
- Engineers who prefer terminals over dashboards
- Builders who want systems, not slogans

Road4AI is not for:

- Users looking for a polished consumer AI app
- Teams that want managed convenience over ownership
- Non-technical buyers who do not want to touch the command line

## Directive

The GUI is for consumers. The CLI is for creators.

Clone the repo, inspect the blueprint, and own the environment.
