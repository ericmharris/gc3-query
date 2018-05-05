from prettyprinter import pprint as pp
from json import loads
from pathlib import Path

$GC3_QUERY_HOME = Path(__file__).parent
print('Configuring xonsh for gc3-query: {}'.format($GC3_QUERY_HOME))
# $GC3_QUERY_HOME = GC3_QUERY_HOME


def _pretty_print_json(args=None, stdin=None):
    """
[root@eharris-lnxobi-01:master ~]# ppj opc -f json compute instance list $OPC_IDENT_CONTAINER
args: ['opc', '-f', 'json', 'compute', 'instance', 'list', '/Compute-587626604']
stdin: None
[root@eharris-lnxobi-01:master ~]#

    """
    print('args: {}'.format(args))
    print('stdin: {}'.format(stdin))
aliases['ppj'] = _pretty_print_json


def _pretty_print_psm_data(args=None, stdin=None):
    pp(psm_data)
aliases['ppp'] = _pretty_print_psm_data


aliases['dev'] = r'cd $DEVEL_DIR'
aliases['Gh'] = r'cd $DEVEL_DIR/gc3-query/gc3_query'





if 'win' in sys.platform:

    mongodb_bin = Path(r'C:\Program Files\MongoDB\Server\3.6\bin')
    if mongodb_bin.exists():
        $PATH.append(mongodb_bin)

    # aliases['dev'] = r'cd $DEVEL_DIR'
    # aliases['Gh'] = r'cd $DEVEL_DIR/gc3-query/gc3_query'
    aliases['show_interfaces'] = r'netsh interface ipv4 show subinterface'
    # aliases['test_ping'] = r'ping -t -n 20 8.8.8.8'
    # aliases['inip'] = r'python.exe ~/Dropbox/Development/iniparser/bin/inip.py'
    # aliases['fautil'] = r'python.exe ~/Dropbox/Development/fadmin/bin/fautil.py'


    # # If Git is installed, add to $PATH and use some included GNU utils
    # _gp = Path($(which git.exe).strip())
    # if not _gp.exists():
    #     _gpstr = [r'C:\Program Files\Git', r'C:\Apps\Git']
    #     _gps = [ Path(r).joinpath('bin/git.exe') for r in _gpstr if Path(r).joinpath('bin/git.exe').exists()]
    #     _gp = _gps[0] if _gps else None
    # if _gp:
    #     # WindowsPath('C:/Apps/Git/bin')
    #     GIT_PATH  = _gp.parent.parent
    #     if str(GIT_PATH/'bin') not in $PATH:
    #         $PATH.append(str(GIT_PATH/'bin'))
    #     # aliases['find'] = GIT_PATH.joinpath('usr/bin/find.exe').as_posix()
    #     del GIT_PATH
    # del _gp

    # # Check to see if putty exists and add it to PATH if it's not already there
    # PUTTY_PATH  = r'C:\Program Files (x86)\PuTTY'
    # if os.path.exists(PUTTY_PATH) and not any([('putty' in p.lower()) for p in $PATH]):
    #     $PATH.append(PUTTY_PATH)
    # del PUTTY_PATH


#  Linux/Unix
if 'linux' in sys.platform:

    aliases['dev'] = r'cd $DEVEL_DIR'
    aliases['Ih'] = r'cd $DEVEL_DIR/iniparser'

    aliases['Ih']   = r'cd $INIP_HOME'
    aliases['Ihe']  = r'cd $INIP_HOME/etc'

    # aliases['pycharm']  = r'/bin/nohup /opt/pycharm/bin/pycharm.sh all> /dev/null &'


# print('Running test opc command')
# pp(loads($(opc -f json compute instance list $OPC_IDENT_CONTAINER))["result"])

print('\nConfigured for opc/psm')
