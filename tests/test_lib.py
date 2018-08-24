#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `gc3_query` package."""

from gc3_query.lib import gc3_cfg


def test_base_dir():
    """Test the CLI."""
    assert BASE_DIR.exists()
