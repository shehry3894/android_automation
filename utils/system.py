import os
import subprocess

from utils.logging import print_and_log


def exec_cmd(cmd: str):
    """
    executes cmd and returns the complete output of the cmd.
    """
    print_and_log('\n=== exec_cmd ===')
    print_and_log('execute_cmd_cmd: ' + cmd)
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    out = str(proc.stdout.read())
    print_and_log('execute_cmd_out: ' + out)
    print_and_log('\n===================')
    return out
