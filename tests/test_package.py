from __future__ import annotations

import importlib.metadata

import genetic_forensic_portal as m


def test_version():
    assert importlib.metadata.version("genetic_forensic_portal") == m.__version__
