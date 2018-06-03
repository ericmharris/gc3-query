import sys
from pathlib import Path

import cookiecutter
import cookiecutter.main
import cookiecutter.config
# from cookiecutter.main import cookiecutter
# from cookiecutter import main, atoml_cfg
from prettyprinter import pprint, pformat

if __name__ == '__main__':
    print("\n\n********** Pre-Generation Hook Running **********")
    cc_user_config = cookiecutter.config.get_user_config()
    cc_default_ctx = cc_user_config.get('default_context')
    print("cc_user_config=")
    pprint(cc_user_config)
    print("********** Pre-Generation Hook Ended **********\n\n")
