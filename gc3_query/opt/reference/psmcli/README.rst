******************************************************
Oracle Platform Service Manager Command Line Interface
******************************************************

Prerequisite
*************
Python 3.3+

    .. code-block :: c
        
        # Verify Python 3.3+
        $ python ?-version
        Python 3.4.3

PSM Client Installation
***********************

    .. code-block :: c
    
        $ sudo -H pip/pip3 install -U psmcli-1.1.2.zip

It does following -

 - Install missing Python package dependencies (if any) from *requests*, *colorama* and *keyring*.
 - Download and install psm client.
 - Create a symlink */bin/psm* to the main executable.

PSM Client Setup
****************
Before using psm client, complete the setup using *psm setup* command.
