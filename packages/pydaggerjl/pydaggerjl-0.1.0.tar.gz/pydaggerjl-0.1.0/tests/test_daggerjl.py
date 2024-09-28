import pytest
import numpy as np
from pydaggerjl import daggerjl

def test_auto_init():
    # This should not raise an error
    result = daggerjl.spawn(np.sum, np.array([1, 2, 3]))
    assert daggerjl.is_initialized == True

def test_explicit_init():
    daggerjl.is_initialized = False  # Reset initialization state
    daggerjl.init()
    assert daggerjl.is_initialized == True

def test_spawn_and_fetch():
    task = daggerjl.spawn(np.sum, np.array([1, 2, 3]))
    result = daggerjl.fetch(task)
    assert result == 6

def test_spawn_chaining():
    a = np.array([1, 2, 3])
    b = np.array([4, 5, 6])

    task = daggerjl.spawn(np.add, a, b)
    result = daggerjl.fetch(task)
    assert np.array_equal(result, np.array([5, 7, 9]))

    task2 = daggerjl.spawn(np.add, task, task)
    result2 = daggerjl.fetch(task2)
    assert np.array_equal(result2, np.array([10, 14, 18]))
