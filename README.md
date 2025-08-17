
### 1. Operation:
```
source /home/iacuser/venv/fastmcp-venv/bin/activate 
ngrok http 8000
```

### 2. Patterns/flow:
```
1. LLM-Driven Agent (llm_agent)
The LLM decides the flow based on your prompt.

[User Prompt]
   |
   v
[LLM]  ---> decides: generate, validate, lint, retry
   |
   +---> call yaml_validator
   |         |
   |         v
   |      success/fail
   |         |
   +---> call ansible_linter
   |         |
   |         v
   |      success/fail
   |         |
   +---> call ansible_dry_run
             |
             v
          success/fail

- Pros: fewer lines of orchestration code.
- Cons: retries/branching not deterministic, LLM may loop forever or give up too early.

2. Workflow-Driven Agent (workflow_agent)
The control logic is explicit, outside the LLM.
[User Prompt]
   |
   v
+---------------------------+
| Step 1: Generate Playbook |
+---------------------------+
   |
   v
+---------------------------+
| Step 2: Run yaml_validator|
+---------------------------+
   | pass
   |-------------------------------+
   | fail                          |
   v                               |
+---------------------------+      |
| Step 3: Run ansible_linter| <----+
+---------------------------+
   | pass
   |-------------------------------+
   | fail                          |
   v                               |
+---------------------------+      |
| Step 4: Run ansible_dry_run| <---+
+---------------------------+
   | pass
   |-------------------------------+
   | fail                          |
   v                               |
   Restart at Step 1 ---------------+

- Pros: fully deterministic, easy to monitor/debug.
- Cons: more orchestration code, less flexible if requirements change often.
```