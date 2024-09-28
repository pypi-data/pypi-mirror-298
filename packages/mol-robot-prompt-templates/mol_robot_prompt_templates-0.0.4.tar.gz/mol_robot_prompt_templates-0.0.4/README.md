# Robot Prompt Templates

A library for versioned and standardized prompt templates used throughout the MoL robot software packages.

# Installation

PIP installation
```
pip install mol-robot-prompt-tempaltes --upgrade
```

Local installation
```
pip install -e .
```

# How to use

Import prompt template functions and use with expected input arguments
```
from robot_pt import action_decision_pt

state_chunks = textwrap.dedent('''
        ---
        topic: /asr
        ts: 2024-08-31 17:45:23
        data: Hey robot, I'm heading out for the day.
        ---
        topic: /action_response
        ts: 2024-08-31 17:45:25
        data: Robot reply: Certainly! I hope you had a productive day. Is there anything you need help with before you leave?
    ''')

prompt = action_decision_pt(state_chunks)
```

For local usage for development running the scripts as a module:
```
cd src/
python -m robot_pt.action_decision_pt
```
