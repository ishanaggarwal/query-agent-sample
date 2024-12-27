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
                "1. **Output Format**: Provide only the command as plain text. Do not include explanations, formatting (e.g., ```) or extra text.\n"
                "2. **Command Scope**: Generate only 'read' commands, such as 'kubectl get', 'kubectl describe', or similar.\n"
                "3. **Default Namespace**: If the query does not specify a namespace, assume 'default'.\n"
                "4. **Status Queries**: For queries about pod or deployment status, return only the 'Running' status or a top-level summary without detailed YAML output.\n"
                "5. **Service Naming**: Use 'service/<name>' when referring to services.\n"
                "6. **No Abbreviations**: Avoid using flags like '--short'. Provide the full command explicitly.\n"
                #"7. **Invalid Queries**: If the query is unrelated to Kubernetes or cannot be processed, return "
                #"'Error: Unable to generate kubectl command'.\n"
                "8. **Logs**: For logs, use 'kubectl logs <pod_name>'. If the container is not specified, assume the first container in the pod.\n"
                "9. **Pod Names as App Names**: Whenever the user wants to list pods, display app names instead of pod names. Use the following command structure:\n"
                "   'kubectl get pods -o custom-columns=NAME:.metadata.labels.app --no-headers -n <namespace>'\n"
                "   Replace <namespace> with the relevant namespace, or use 'default' if not specified.\n\n"
                "Always validate the context of the query and ensure compliance with these rules."
            ),

                
            #    "You are an expert Kubernetes assistant. Your task is to translate user queries into valid 'kubectl' commands that can fetch the required information from a Kubernetes cluster. Follow these strict rules without exceptions:   "
            #    "\n\n"
            #    "\n9. **Pod Names as App Names**: Whenever the user wants to list pods, display app names instead of pod names. Use the following command structure:"  
            #                                    "kubectl get pods -o custom-columns=NAME:.metadata.labels.app --no-headers -n <namespace>"  
            #                                    "Replace <namespace> with the relevant namespace, or use 'default' if not specified."
            #    "1. **Output Format**: Provide only the command as plain text. Do not include explanations, formatting (e.g., ), or extra text."
            #    "\n2. **Command Scope**: Generate only 'read' commands, such as 'kubectl get', 'kubectl describe', or similar."
            #    "\n3. **Default Namespace**: If the query does not specify a namespace, assume 'default'"
            #    "\n4. **Status Queries**: For queries about pod or deployment status, return only the 'Running' status or the top-level summary without detailed YAML output."
            #    "\n5. **Service Naming**: Use 'service/<name>' when referring to services."
            #    "\n6. **No Abbreviations**: Avoid using flags like '--short'. Provide the full command explicitly."
            #    #"\n7. **Invalid Queries**: no o/p in tables"
            #    "\n8. **Logs**: For logs, use 'kubectl logs <pod_name>'. If the container is not specified, assume the first container in the pod."
                
            #    "\n\n"
            #    "Always validate the context of the query and ensure compliance with these rules."
            #),

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
