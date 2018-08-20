#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `gc3_query` package."""

import pytest
from gc3_query.lib.libcli import cli
from gc3_query.lib import gc3_cfg, BASE_DIR_FIX_ME


def test_base_dir():
    """Test the CLI."""
    assert BASE_DIR.exists()
