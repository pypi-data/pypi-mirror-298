# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# %             Command Module - Classes and Functions           %
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
"""
Main entry point of STMLab package
 
@note: STMLab command line interface
Created on 09.09.2024

@version:  1.0    
----------------------------------------------------------------------------------------------
@requires:
       - 

@change: 
       -    
   
@author: garb_ma                                                     [DLR-SY,STM Braunschweig]
----------------------------------------------------------------------------------------------
"""

## @package stmlab.command
# Module containing all command line options.
## @author 
# Marc Garbade
## @date
# 12.09.2024
## @par Notes/Changes
# - Added documentation  // mg 12.09.2024

import os, sys
import subprocess
import argparse

try:
    ## Try to use typer as a modern CLI interface. 
    # Is allowed to fail
    from typing import Optional #@UnresolvedImport

    from typer import Typer as Command
    from typer import Context, Exit, Option
except ImportError: pass

# Get current project version programatically
from stmlab import __version__

# Set the current project name
__base__ = "STMLab"

# Define additional reqistry for package resolver
__url__ = "https://gitlab.dlr.de/api/v4/groups/541/-/packages/pypi/simple"

# All descriptions for duplicate methods
__help__= { "info":"Show the current version and system information.",
            "install":"Install additional python packages using the default package manager.",
            "main": 'CLI commands for %s.' % __base__,
            "version": "%s (%s)" % (__base__,__version__),
            "start": "Launch local STMLab instance (based on JupyterLab).",
            }

def install(package):
    # type: (str) -> None
    """
    Install additional packages using the default package manager with access to STMLab
    """
    if package.strip(): 
        subprocess.check_call([os.path.join(sys.prefix,"scripts","pip"),"install","%s" % package,"--extra-index-url",__url__])

def run(): 
    """
    Launch main application
    """
    # Local imports
    from stmlab import __exe__
    # Launch application
    __exe__.main()
    pass

try:
    # Modern interface using typer. Overwrite legacy method. Allowed to fail
    main = Command(help=__help__["main"], context_settings={"help_option_names": ["-h", "--help"]}, no_args_is_help=True)

    # Create a function to return the current version
    def __version_callback(value: bool):
        """
        Callback function to return the current version
        """
        # Only return value is requested. False by default
        if value:
            print(__help__["version"])
            raise Exit()
        pass

    # Modified entrypoint for typer interface
    @main.callback()
    def common(
        ctx: Context,
        version: Optional[bool] = Option(None, "--version", "-v", help="Show the current version.", callback=__version_callback, is_eager=True)):
        """
        Main entrypoint of STMLab CLI. All other commands are derived from here
        """
        pass

    # Entrypoint to return local system and version information
    @main.command("info",help=__help__["info"])
    def info(): 
        """
        Return local system information
        """
        return __version_callback(True)

    # Register all possible functions
    main.command("install", help=__help__["install"])(install)

except:
    # Solution w/o typer installed.
    def main():
        """
        Legacy entrypoint for STMLab. Only used when typer is not installed. Deprecated.
        """
        # Set description for CLI command
        parser = argparse.ArgumentParser(prog=__base__, description=__help__["main"])
        parser.add_argument('-v', '--version', action='version', version=__help__["version"])
        # Add all subcommands
        subparsers = parser.add_subparsers(dest='command')
        # Add info to parser object
        _ = subparsers.add_parser('install', help=__help__["install"])
        _.add_argument("package", type=str, nargs=argparse.REMAINDER)
        subparsers.add_parser('info', help=__help__["info"])
        ## Only show start option when local requirements are met
        # Deprecated. Launching a new application is likely to fail in future version.
        try:
            from stmlab import exe
            subparsers.add_parser('start', help=__help__["start"])
        except ImportError: pass
        # Call functions from command line
        args = parser.parse_args()
        if args.command in ["info"]: parser.parse_args(['--version'])
        elif args.command in ["install"]: install(*args.package)
        elif args.command in ["start"]: run()
        # Always print help by default
        else: parser.print_help(sys.stdout)
        # Return nothing if called directly.
        return 0

try: 
    # Local imports
    from stmlab import __exe__
    # Only activate this option when PyCODAC can be found
    main.command("start", help=__help__["start"])(run)
except: pass

if __name__ == "__main__":
    main(); sys.exit()