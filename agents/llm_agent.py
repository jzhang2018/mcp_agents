# agent/llm_agent.py
# LLM (model) Driven Agent

from openai import OpenAI
from dotenv import load_dotenv
import json

def run_client():
    load_dotenv()
    print("LLM Driven Client starting...")

    client = OpenAI()

    tools_config = [
        {
            "type": "mcp",
            "server_label": "ansible_mcp",
            "server_url": "https://9485c02b8d66.ngrok-free.app/mcp/",
            "require_approval": "never",
        }
    ]

    print("Using tools:", json.dumps(tools_config, indent=2))

    try:
        resp = client.responses.create(
            model="gpt-3.5-turbo",
            tools=tools_config,
            input="Create an ansible playbook that ensures /tmp/foo is present. "
                "Then validate it using the yaml_validator tool. If yaml_validator succeeds, then call ansible_linter tool." \
                "If yaml_validator fails, try to fix it and generate a new playbook. If ansible_linter fails, try to fix it " \
                "and generate a new playbook. Keep trying till it passes both yaml_validator and ansible_linter tools.If they all pass, the " \
                "try tool ansible_dry_run. If ansible_dry_run fails, keep trying from begining till it works."
        )

        # print("Response received:")
        # print(json.dumps(resp.model_dump(), indent=2))
        print(f"Output text: {resp.output_text}")

    except Exception as e:
        print("Exception during OpenAI client call:", e)