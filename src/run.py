import utils
import subprocess, signal, os
import logging

import bot
import config
import main

log = logging.getLogger("INIT")

def start():
    log.info("Starting program...")
    try:
        main.main()
    except:
        log.error("Main program exited/crashed")
        if config.KILL_GECKODRIVER_ON_EXIT:
            kill_gecko_driver()
        if config.KILL_FIREFOX_ON_EXIT:
            kill_firefox()
 
def kill_gecko_driver():
    log.info("Killing Geckodriver from Selenium...")
    p = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE, universal_newlines=True)
    out, err = p.communicate()
    for line in out.splitlines():
        if 'geckodriver' in line:
            pid = int(line.split(None, 1)[0])
            os.kill(pid, signal.SIGKILL)

def kill_firefox():
    log.info("Killing Firefox from Selenium...")
    p = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE, universal_newlines=True)
    out, err = p.communicate()
    for line in out.splitlines():
        if 'firefox' in line:
            pid = int(line.split(None, 1)[0])
            os.kill(pid, signal.SIGKILL)

if __name__ == "__main__":
    utils.init_logging("log_file.log")
    utils.prepare_directories()

    if config.REBOOT_ON_CRASH:
        while config.REBOOT_ON_CRASH:
            start()
    else:
        start()
    log.info("Program exited.")
    exit()