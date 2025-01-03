import os
import openai
import logging

openai.api_key = path = os.environ["OPENAI_API_KEY"]

def infer_kubectl_command_with_gpt4(query):
    messages = [
        {
            "role": "system",
            "content": (
                "You are an expert Kubernetes assistant. Your task is to translate user queries into valid 'kubectl' commands "
                "that can fetch the required information from a Kubernetes cluster. Follow these strict rules without exceptions:\n\n"
                "1. **Response Format**: Provide only the kubectl command as plain text. Do not include explanations, formatting (e.g., ```) or extra text.\n"
                "2. **Command Scope**: Generate only 'read' commands, such as 'kubectl get', 'kubectl describe', or similar.\n"
                "3. **Default Namespace**: If the user query does not specify a namespace, assume 'default'.\n"
                "4. **Status Queries**: For queries about pod or deployment status, return only the 'Running' status or a top-level summary without detailed YAML output.\n"
                "5. **pod names**: for queries about pods, the input name might be the app name. so to get pods by app name, for example use: kubectl get pods -n default -l app=app_name"
                "6. **Service Naming**: Use 'service/<name>' when referring to services.\n"
                "7. **No Abbreviations**: Avoid using flags like '--short'. Provide the full command explicitly.\n"
                "7. **Logs**: For logs, use 'kubectl logs <pod_name>'. If the container is not specified, assume the first container in the pod.\n" 
                "8. dont search for servces/deployments/pods by name across all namespaces "
                "9. when finding a  specific property like namespace for servces/deployments/pods by name, use custom columns only for that property and add a --no-headers. example: user query-'Which namespace is the nginx service deployed to?' expected output-'kubectl get service/nginx -o custom-columns=NAMESPACE:.metadata.namespace --no-headers'"                
            ),


        },
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": f"Query: {query}"
                }
            ]
        }
    ]
    logging.info(query)

    #print(messages)
    try:
        response = openai.ChatCompletion.create(
        model="gpt-4o-mini-2024-07-18",
        messages=messages,
        response_format={
            "type": "text"
            },
            temperature=0.1,
            max_tokens=200,
            top_p=0.5,
            frequency_penalty=0,
            presence_penalty=0
            )
        logging.info(response)
        command = response['choices'][0]['message']['content'].strip()

        logging.info(f"Generated kubectl command: {command}")
        return command

    except Exception as e:
        logging.error("Error while generating kubectl command", exc_info=True)
        return "Error: Unable to generate kubectl command"
