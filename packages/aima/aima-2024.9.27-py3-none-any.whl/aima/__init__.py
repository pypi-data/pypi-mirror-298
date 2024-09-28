"""Artificial Intelligence: A Modern Approach (AIMA) by Stuart Russell and Peter Norvig"""
from pathlib import Path
__all__ = ['utils', 'text', 'search', 'probability', 'logic', 'rl']
__all__ = [p.with_suffix('').name for p in Path(__file__).parent.glob('*.py')]
