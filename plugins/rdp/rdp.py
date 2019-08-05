#TEMPLATE VERSION 1.0

##############################################
#SECTION 0 - DEFAULT IMPORTS (DO NOT CHANGE)
#############################################

import sys
import os
sys.path.append(os.path.join(os.getcwd(), "..", "..", "misc"))
import colors
sys.path.append(os.path.join(os.getcwd(), "..", "..", "src"))
import requires
from var import global_vars
import subprocess


###########################
#SECTION 1 - IMPORTS
###########################
# try:
#     import rdpy    #HERE
# except ModuleNotFoundError:
#     colors.PrintColor("WARN", "Unable to find 'rdpy', install?")   #HERE
#     ans = input("[Y/N] ")
#     if ans.lower() == "y":
#         requires.install('rdpy')   #HERE
#         import rdpy
#     else:
#         colors.PrintColor("FAIL", "'<new_module_here>' is a dependency!")   #HERE
#         input()

###########################
#SECTION 2 - ABOUT
###########################
name = ""
description = '''
The <example> plugin helps with probing the ssh authentication service to determine valid credentials.\
This is a simple plugin that comes with the default 'broot' framework.
'''
author = ""
version = "1.0"
art = """


"""
banner = '''
{}
{}
Author:  {}
Version: {}'''.format(art,name,author,version)
print(banner)

#############################
#SECTION 3 - PLUGIN COMMANDS
#############################

#This is an example, you do not necessarily need extra commands.  Replace the below with your own
plugin_cmds = {
    "test": {
            "Command": "test",
            "Help": "Print information related to the subsequent key-word.",
            "Sub-Cmds": ["commands", "plugins", "options", "loaded-plugin", "creds", "sequence"],
            "Usage": "test <sub-cmd>",
            "Alias": None
        },
}

#function to define what to do with the new commands
def parse_plugin_cmds(commands):
    cmds = commands.split(" ")
    if cmds[0] == "test":
        print("success!")
    pass

#############################
#SECTION 4 - PLUGIN VARIABLES
#############################

#This is an example, variables must have a unique name
plugin_vars = {
    'try-backdoor': {
        "Name": "Try-Backdoor",
        "Value": False,
        "Type": 'Boolean',
        "Default": False,
        "Help": "This option will try to determine if sticky keys or other backdoors will open a command prompt",
        "Example": "True"
    },
    'rdp-bin': {
        "Name": "RDP-Bin",
        "Value": None,
        "Type": 'String',
        "Default": None,
        "Help": "Options are: rdesktop xfreerdp",
        "Example": "xfreerdp"
    },
    'rdp-path': {
        "Name": "RDP-Path",
        "Value": None,
        "Type": 'String',
        "Default": None,
        "Help": "This is auto filled with a common binary/exe path.  You may still change it.",
        "Example": r"C:\Users\root\Documents\RDP\freerdp.exe"
    },
    'proxy-ip': {
        "Name": "Proxy-IP",
        "Value": None,
        "Type": 'String',
        "Default": None,
        "Help": "The IP of your proxy server",
        "Example": "10.0.0.4"
    },
    'proxy-protocol': {
        "Name": "Proxy-Protocol",
        "Value": None,
        "Type": 'String',
        "Default": None,
        "Help": "The options here are socks4 socks5 http",
        "Example": "socks5"
    },
    'proxy-port': {
        "Name": "Proxy-Port",
        "Value": 8080,
        "Type": 'Integer',
        "Default": 8080,
        "Help": "The listening port for the proxy service",
        "Example": "9050"
    }

}

#############################
#SECTION 5 - MAIN
#############################
#This function does the main exection of the brutefore method and MUST BE HERE
def run(target, username, password):
    verbose = global_vars['verbose']['Value']
    attempt = "Target:{} Username:{} Password:{}".format(target, username, password)
    success = False
    if os.name == 'nt':
        colors.PrintColor("WARN","Windows is not supported at this time!")
        return
    rdp_bin = plugin_vars['rdp-bin']['Value']
    rdp_path = plugin_vars['rdp-path']['Value']
    proxy_proto = plugin_vars['proxy-protocol']['Value']
    proxy_port = plugin_vars['proxy-port']['Value']
    proxy_ip = plugin_vars['proxy-ip']['Value']
    if rdp_bin == "rdesktop":
        if rdp_path is None or "rdesktop" not in rdp_path:
            plugin_vars['rdp-path']['Value'] = "/usr/bin/rdesktop"
            rdp_bin = plugin_vars['rdp-path']['Value']
    elif rdp_bin == "xfreerdp":
        if rdp_path is None or "xfreerdp" not in rdp_path:
            plugin_vars['rdp-path']['Value'] = "/usr/bin/xfreerdp"
            rdp_bin = plugin_vars['rdp-path']['Value']
        cmd = "{b} /v:{t} /u:{u} /p:{p} /client-hostname:{h} /cert-ignore +auth-only".format(b=rdp_bin,t=target,u=username,p=password,h=target)
        if proxy_ip is not None:
            append = "/proxy:{}://{}:{}".format(proxy_proto,proxy_ip,proxy_port)
            cmd = cmd + " " + append
        result = subprocess.run(cmd.split(), capture_output=True)
        if "AUTHENTICATION_FAILED" in result.stderr:
            success = False
            if verbose:
                colors.PrintColor("INFO", "Failed Authentication --> {}".format(attempt))
        elif "proxy: failed" in result.stderr:
            success = False
            colors.PrintColor("FAIL", "Proxy Connection Error!")
            return success
        success = True

    return success