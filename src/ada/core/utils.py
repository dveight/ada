import subprocess


def run_command(command):
    """
    Run command and print out stdout in real time.

    Args:
        command (list): list of args that subprocess will run.

    Returns:
        int: poll code.
    """
    process = subprocess.Popen(command, stdout=subprocess.PIPE)
    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            print output.strip()

    rc = process.poll()
    return rc


def is_nuke():
    Returns:
        bool: are we running in a nuke environment

    """
    try:
        import _nuke
        return True
    except ImportError:
        return False


def is_gaffer():
    """
    Are we running inside of the Gaffer environment

    Returns:
        bool: are we running in a gaffer environment

    """
    try:
        import Gaffer
        return True
    except ImportError:
        return False
