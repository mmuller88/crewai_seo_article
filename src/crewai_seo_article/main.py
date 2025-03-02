#!/usr/bin/env python
import sys
import warnings
import random
from datetime import datetime

from crewai_seo_article.crew import CrewaiSeoArticle

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information


def run():
    """
    Run the crew.
    """
    # Available gauge values from the temperature recommendation table
    gauge_options = ['16', '12', '9', '7', '5', '3']
    product_options = ['T-Shirt', 'Pullover']

    inputs = {
        'Produktname': 'T-Shirt', # random.choice(product_options),
        "Material": "Caschmier",
        # 'Material': '100% Kaschmir',
        # 'Strickart': 'Strickpullover',
        # 'Maschendichte': random.choice(gauge_options),
        # 'Garnfeinheit': '20/22',
        # 'Passform': 'Slim Fit',
        # 'Farbe': 'Schwarz',
        # 'topic': 'AI LLMs',
        # 'current_year': str(datetime.now().year)
    }

    try:
        CrewaiSeoArticle().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "Produktname": "T-Shirt",
        "Material": "Caschmier",
        # "Strickart": "Strickpullover",
        # "Maschendichte": "22 Gauge",
        # "Garnfeinheit": "20/22",
        # "Passform": "Slim Fit",
        # "Farbe": "Schwarz",
        # 'topic': 'AI LLMs',
    }
    try:
        CrewaiSeoArticle().crew().train(n_iterations=int(
            sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")


def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        CrewaiSeoArticle().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")


def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        'Produktname': 'T-Shirt',
        # 'Material': '100% Baumwolle',
        # 'Strickart': 'Strickpullover',
        # 'Maschendichte': '22 Gauge',
        # 'Garnfeinheit': '20/22',
        # 'Passform': 'Slim Fit',
        # 'Farbe': 'Schwarz',
        # "topic": "AI LLMs"
    }
    try:
        CrewaiSeoArticle().crew().test(n_iterations=int(
            sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")
