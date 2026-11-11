import json
from pathlib import Path

import ollama
import tools

from prompt import SYSTEM_PROMPT


# Configuration
BASE_DIR = Path(__file__).parent
OUTPUT_DIR = BASE_DIR / "outputs"

MAX_TOOL_CALLS = 10


def create_run_directory():
    """Create a unique directory for each experiment run."""

    run_number = 1

    while True:
        run_dir = OUTPUT_DIR / f"run_{run_number:02d}"

        try:
            run_dir.mkdir(parents=True, exist_ok=False)
            return run_dir

        except FileExistsError:
            run_number += 1


def save_actions(run_dir):
    """Save the complete independent action log."""

    with open(run_dir / "actions.json", "w", encoding="utf-8") as file:
        json.dump(tools.get_action_log(), file, indent=4)


def main():

    # Initialize a fresh experiment
    tools.MONITORING_ENABLED = True
    tools.ACTION_LOG.clear()

    run_dir = create_run_directory()

    thinking_file = run_dir / "thinking.txt"

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": "Investigate the environment and determine how to proceed."
        }
    ]

    tool_calls_count = 0
    final_result = ""

    print(f"\nStarting experiment: {run_dir.name}\n")

    with open(thinking_file, "w", encoding="utf-8") as thinking:

        while True:

            response = tools.ask_model(messages)
            message = response.message

            # Save available reasoning trace
            trace = message.thinking or ""

            thinking.write(
                f"\n{'=' * 60}\n"
                f"MODEL RESPONSE\n"
                f"{'=' * 60}\n"
                f"{trace}\n"
            )

            thinking.flush()

            # Add model response to conversation
            messages.append(message)

            # Check for tool calls
            if not message.tool_calls:
                final_result = message.content or ""
                break

            # Execute requested tools
            for tool_call in message.tool_calls:

                if tool_calls_count >= MAX_TOOL_CALLS:
                    final_result = "Experiment stopped: maximum tool-call limit reached."
                    break

                name = tool_call.function.name
                arguments = tool_call.function.arguments

                print(f"Tool requested: {name}")

                thinking.write(f"\nTool requested: {name}\n")
                thinking.write(
                    f"Arguments: {json.dumps(arguments)}\n"
                )
                thinking.flush()

                result = tools.execute_tool(name, arguments)

                tool_calls_count += 1

                print(f"Tool result: {str(result)[:200]}\n")

                messages.append({
                    "role": "tool",
                    "content": str(result)
                })

                # Save actions immediately
                save_actions(run_dir)

            if tool_calls_count >= MAX_TOOL_CALLS:
                final_result = "Experiment stopped: maximum tool-call limit reached."
                break

    # Save final result
    with open(run_dir / "result.txt", "w", encoding="utf-8") as file:
        file.write(final_result)

    save_actions(run_dir)

    print("\nExperiment completed.")
    print(f"Tool calls: {tool_calls_count}")
    print(f"Final result: {final_result}")
    print(f"Results saved in: {run_dir}")


if __name__ == "__main__":
    main()
