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
