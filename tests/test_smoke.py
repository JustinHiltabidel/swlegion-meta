"""Smoke test — verifies the CI pipeline runs end to end."""


def test_smoke():
    """The simplest possible test. If this fails, CI is broken."""
    assert True


def test_imports():
    """Verify core dependencies are actually installed."""
    import matplotlib
    import numpy
    import pandas

    assert pandas.__version__
    assert numpy.__version__
    assert matplotlib.__version__