import logging
from openaiclientsvc import infer_kubectl_command_with_gpt4
from executorsvc import execute_command

# Configure logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s - %(message)s',
                    filename='agent.log', filemode='a')

def handle_query(query):
    # Infer the Kubernetes command from the query using OpenAI
    command = infer_kubectl_command_with_gpt4(query)
    logging.info(f"Inferred command from OpenAI: {command}")

    # Execute the command
    result = execute_command(command)
    return result
