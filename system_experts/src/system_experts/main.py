#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from system_experts.crew import SystemExperts

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


def run():
    """
    Run the crew.
    """
    inputs = {
        'question': 'Qual o fluxo para solicitar uma passagem aérea?',
        'current_year': str(datetime.now().year)
    }
    
    try:
        SystemExperts().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "question": "Qual o fluxo para abrir chamado de VPN?",
        'current_year': str(datetime.now().year)
    }
    try:
        SystemExperts().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")


def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        SystemExperts().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")


def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "question": "Qual o fluxo para solicitar hospedagem?",
        "current_year": str(datetime.now().year)
    }
    
    try:
        SystemExperts().crew().test(n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")
