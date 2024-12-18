import subprocess
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s - %(message)s',
                    filename='agent.log', filemode='a')

def execute_command(command):
    """
    Executes a shell command and returns the output.
    """
    logging.info(f"Executing command: {command}")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        logging.error("Error executing command", exc_info=True)
        return "An error occurred while executing the command"
