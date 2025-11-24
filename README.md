# Viber Development Environment

This repository contains a suite of tools for AI-driven software development, including a project scaffolding system (LLM OS), a powerful spec-driven development toolkit (Spec Kit), and a collection of AI agents.

## Table of Contents

- [Viber Development Environment](#viber-development-environment)
  - [Table of Contents](#table-of-contents)
  - [1. LLM OS](#1-llm-os)
    - [Overview](#overview)
    - [Usage](#usage)
  - [2. Spec Kit](#2-spec-kit)
    - [Overview](#overview-1)
    - [Getting Started](#getting-started)
    - [Core Commands](#core-commands)
  - [3. Agents](#3-agents)
    - [Overview](#overview-2)
    - [Available Agents](#available-agents)
      - [`agent.py`](#agentpy)
      - [`general_agent.py`](#general_agentpy)
      - [`lm_studio_agent.py`](#lm_studio_agentpy)
      - [Dynamic Agents](#dynamic-agents)
    - [Running Agents](#running-agents)
  - [4. LanceDB GUI](#4-lancedb-gui)
    - [Overview](#overview-3)
    - [Running the GUI](#running-the-gui)

## 1. LLM OS

### Overview

The LLM OS is a command-line tool for scaffolding and managing software projects. It provides a structured workflow for defining project specifications and implementation plans before writing any code.

### Usage

To create a new project, run the following command from the root of the repository:

```bash
python3 -m projects.llm_os_core.project_cli new "Your Project Name"
```

This will create a new project directory in `projects/` with the following structure:

```
projects/
└── 001-your-project-name/
    ├── checklists/
    ├── plan.md
    └── spec.md
```

*   `spec.md`: A Markdown file for defining the feature specification.
*   `plan.md`: A Markdown file for outlining the implementation plan.

## 2. Spec Kit

### Overview

Spec Kit is a powerful, standalone toolkit for "Spec-Driven Development." It uses AI agents to generate code from specifications, enabling a more predictable and efficient development process. It has its own CLI (`specify`) and a set of slash commands (`/speckit.*`) for interacting with an AI assistant like Gemini.

### Getting Started

To begin using Spec Kit, you first need to initialize it within your project. For detailed instructions, refer to the official documentation in `spec-kit/README.md`.

### Core Commands

Once initialized, you can use the following slash commands with your AI assistant:

*   `/speckit.constitution`: Create or update project governing principles.
*   `/speckit.specify`: Define what you want to build.
*   `/speckit.plan`: Create a technical implementation plan.
*   `/speckit.tasks`: Generate an actionable task list.
*   `/speckit.implement`: Execute all tasks and build the feature.

## 3. Agents

### Overview

This repository includes a variety of AI agents designed to automate different aspects of the development process. These agents can be used for tasks such as managing the RAG system, generating code, and interacting with the Spec Kit.

### Available Agents

#### `agent.py`

A simple command-line interface for interacting with the RAG (Retrieval-Augmented Generation) system.

*   **Commands:**
    *   `init`: Initializes the LanceDB database.
    *   `add <text>`: Adds text to the database.
    *   `search <query>`: Searches the database.

#### `general_agent.py`

A more advanced agent with a wider range of capabilities, including programmatic interaction with the Spec Kit.

#### `lm_studio_agent.py`

An agent responsible for generating embeddings using a local LM Studio instance.

#### Dynamic Agents

The `dynamic_agents/` directory contains a collection of specialized agents for tasks such as:

*   Creating new agents
*   Assigning tasks
*   Monitoring agent performance
*   Scaling agent resources

### Running Agents

To start an agent, run its corresponding Python script from the root of the repository:

```bash
# Example: Start the general agent
venv/bin/python general_agent.py
```

## 4. LanceDB GUI

### Overview

A graphical user interface for interacting with LanceDB databases. It allows you to:

*   Connect to a database.
*   View tables and their contents.
*   Perform vector searches.

### Running the GUI

To launch the GUI, run the following command from the root of the repository:

```bash
venv/bin/python -m projects.llm_os_gui.gui.main_window
```
