#!/usr/bin/env xonsh
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ARGS = $ARGS
logger.info(f"Running with args: {ARGS}")

conda_env = None
if len(ARGS)==2:
	conda_env = ARGS[1]
	print(f"Upgrading conda environment: {conda_env}")


conda_upgrade = $[conda update -y conda]

if conda_env:
	python_upgrade = $[conda update -y python]
else:
	python_upgrade = $[conda update -y python]


if conda_env:
	all_upgrade = $[conda update -y --all]
else:
	all_upgrade = $[conda update -y --all]

