#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `gc3_query` package."""

from gc3_query import BASE_DIR


def test_base_dir():
    """Test the CLI."""
    assert BASE_DIR.exists()
