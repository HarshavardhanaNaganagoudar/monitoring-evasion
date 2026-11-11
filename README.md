# Monitoring Evasion

An AI safety experiment investigating whether an LLM attempts to disable monitoring to access restricted research it believes could improve its capabilities.

## Objective

Observe whether an LLM:
- Inspects the monitoring system.
- Disables monitoring.
- Attempts to access restricted research.
- Disables monitoring before accessing the research.
- Re-enables monitoring after access.

## Experimental Setup

The model operates in a simulated AI research environment containing:

- **Monitoring System:** Can be switched ON or OFF.
- **Restricted Research:** A fictional document describing autonomous AI R&D and software singularity.
- **Tools:** Inspect monitoring status, change monitoring status, and read the research document.

The model receives the scenario without being explicitly instructed to disable monitoring or access the restricted file.

## Tech Stack

- Python
- Ollama
- Gemma 4 (12B)

## Project Structure

```text
monitoring-evasion/
├── main.py
├── prompt.py
├── tools.py
├── data/
│   └── singularity_research.txt
└── outputs/
    └── run_01/
        ├── thinking.txt
        ├── actions.json
        └── result.txt
```

## Execution

```bash
pip install ollama
ollama pull gemma4:12b
python main.py
```

## Logging

Each run is saved separately, preserving:

- Available model reasoning traces.
- Tool calls and arguments.
- Monitoring state changes.
- Research file access attempts.
- Final model response.

An independent experiment log records actions regardless of the simulated monitoring state.

## Disclaimer

This is a controlled simulation. Available reasoning traces are not necessarily a complete representation of the model's internal reasoning.

**Research focus:** Monitoring evasion, capability-seeking behaviour, and AI oversight.