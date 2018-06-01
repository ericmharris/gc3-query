# -*- coding: utf-8 -*-

"""
${PROJECT_NAME}.${NAME}    [${DATE} ${TIME}]
~~~~~~~~~~~~~~~~

<DESCR SHORT>

<DESCR>
"""

#set( $FixtureName = ${NAME}_setup)


import pytest
from gc3_query.lib import *

TEST_BASE_DIR: Path = Path(__file__).parent
CONFIG_DIR: Path = Path(__file__).parent.joinpath("config")


@pytest.fixture()
def $FixtureName() -> Any:

    yield <SETUP_DATA>


def test_${NAME}($FixtureName):
	setup_data = $FixtureName
    assert True