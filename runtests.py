import os
import sys
import subprocess

import pytest


def flake8_lint(args):
    print('Running flake8 code linting...')
    result = subprocess.call(['flake8'] + args)
    print('flake8 failed.' if result else 'flake8 passed.')
    return result

sys.path.append(os.path.dirname(__file__))

pytest.main()
