#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `gc3_query` package."""

import pytest

from click.testing import CliRunner

from gc3_query import gc3_query
from gc3_query import cli
from gc3_query.lib.gc3load import test_gc3_query_click_function


@pytest.fixture
def response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')


def test_content(response):
    """Sample pytest test function with the pytest fixture as an argument."""
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string


def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.main)
    assert result.exit_code == 0
    assert "gc3_query.cli.main" in result.output
    help_result = runner.invoke(cli.main, ["--help"])
    assert help_result.exit_code == 0
    assert "--help  Show this message and exit." in help_result.output


def test_gc3_query_click_function():
    from .secrets import username, current_password, new_password

    test_data = TestCase(
        username=username, current_password=current_password, new_password=new_password, env_name="hcmx-test"
    )
    runner = CliRunner()
    result = runner.invoke(
        change_password, args=["-u", username, "-c", current_password, "-n", new_password, "-e", test_data.env_name]
    )
    assert result.exit_code == 0
