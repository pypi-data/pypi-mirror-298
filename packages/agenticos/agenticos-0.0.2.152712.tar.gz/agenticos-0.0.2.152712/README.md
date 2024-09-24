# AgenticOS

AgenticOS is a flexible and modular framework designed to help developers deploy and manage AI-driven workflows using agent-based systems. The framework is designed to be LLM-agnostic and core-tech switchable in the future, allowing developers to integrate their preferred agent systems seamlessly.

The goal is to provide a framework that integrates easily into your existing or planned infrastructure, giving you the flexibility to focus on AI task execution without complex setups.


## Installation
Agentic-core is designed to be installed alongside another LLM agent workload orchestration tool. Currently it only supports crew AI.
1. Folow crewai instructions for installation and creating of the project:  
https://docs.crewai.com/getting-started/Installing-CrewAI/  
https://docs.crewai.com/getting-started/Start-a-New-CrewAI-Project-Template-Method/  
2. Install agenticos package using poetry:
```bash
poetry add agenticos
```

## Usage
### Initialization
After adding agenticos to the project you need to init your project as an agentic node"
```bash
agentic init
```
It will generate following files in your project:
```
[app_root]
|-src
  |-agentic
    |-agentic_node.py
    |-agentic_config.yml
```
This configuration should work with out-of the box crew ai project.
### Running
Currentic agentic node may be run only as a standalone HTTP server. Production fastapi mode:
```bash
agentic run
```
or dev fastapi mode:
```bash
agentic run --dev
```