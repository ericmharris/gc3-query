#from prettyprinter import pprint as pp
# from pprint import pprint as pp
from json import loads
from pathlib import Path

$BASE_DIR = Path(__file__).parent
print('Configuring xonsh for gc3-query: {}'.format($BASE_DIR))
# $BASE_DIR = BASE_DIR


# def _pretty_print_json(args=None, stdin=None):
#     """
# [root@eharris-lnxobi-01:master ~]# ppj opc -f json compute instance list $OPC_IDENT_CONTAINER
# args: ['opc', '-f', 'json', 'compute', 'instance', 'list', '/Compute-587626604']
# stdin: None
# [root@eharris-lnxobi-01:master ~]#

#     """
#     print('args: {}'.format(args))
#     print('stdin: {}'.format(stdin))
# aliases['ppj'] = _pretty_print_json


# def _pretty_print_psm_data(args=None, stdin=None):
#     pp(psm_data)
# aliases['ppp'] = _pretty_print_psm_data


aliases['dev'] = r'cd $DEVEL_DIR'
aliases['Gh'] = r'cd $DEVEL_DIR/gc3-query/gc3_query'

aliases['Ghb'] = r'cd $DEVEL_DIR/gc3-query/gc3_query/bin'
aliases['Ghe'] = r'cd $DEVEL_DIR/gc3-query/gc3_query/etc'
aliases['Ghl'] = r'cd $DEVEL_DIR/gc3-query/gc3_query/lib'
aliases['Ghs'] = r'cd $DEVEL_DIR/gc3-query/gc3_query/sbin'

aliases['Gho'] = r'cd $DEVEL_DIR/gc3-query/gc3_query/opt'
aliases['Ghor'] = r'cd $DEVEL_DIR/gc3-query/gc3_query/opt/reference'
aliases['Ghot'] = r'cd $DEVEL_DIR/gc3-query/gc3_query/opt/templates'
aliases['Ghotc'] = r'cd $DEVEL_DIR/gc3-query/gc3_query/opt/templates/cookiecutter'

aliases['Ghv'] = r'cd $DEVEL_DIR/gc3-query/gc3_query/var'
aliases['Ghvm'] = r'cd $DEVEL_DIR/gc3-query/gc3_query/var/mongodb'
aliases['Ghvmc'] = r'cd $DEVEL_DIR/gc3-query/gc3_query/var/mongodb/config'
aliases['Ghvml'] = r'cd $DEVEL_DIR/gc3-query/gc3_query/var/mongodb/logs'
aliases['Ghvms'] = r'cd $DEVEL_DIR/gc3-query/gc3_query/var/mongodb/scripts'
aliases['Ghvs'] = r'cd $DEVEL_DIR/gc3-query/gc3_query/var/scratchpad'

#### gc3atoml aliases
aliases['GA'] = r'gc3atoml'
aliases['GAp'] = r'gc3atoml print'
aliases['GAe'] = r'gc3atoml export'
aliases['GAee'] = r'gc3atoml export --editor'



if 'win' in sys.platform:

    for p in [r'C:\Program Files\MongoDB\Server\3.6\bin',
             r'C:\tools\MongoDB\Server\3.6\bin']:
        mongodb_bin_dir = Path(p)
        if mongodb_bin_dir.exists():
            s = str(mongodb_bin_dir)
            print(f"Appending {s} to PATH")
            $PATH.append(s)

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
