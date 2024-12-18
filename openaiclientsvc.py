import os
import openai
import logging

openai.api_key = path = os.environ["OPENAI_API_KEY"]

def infer_kubectl_command_with_gpt4(query):
    messages = [
        {
            "role": "system",
            "content": (
                "You are an expert Kubernetes assistant. Your task is to translate user queries into valid 'kubectl' commands that can "
                "fetch the required information from a Kubernetes cluster. Follow these strict rules without exceptions: "
                "\n\n"
                "1. **Output Format**: Provide only the command as plain text. Do not include explanations, formatting (e.g., ```), or extra text."
                "\n2. **Command Scope**: Generate only 'read' commands, such as 'kubectl get', 'kubectl describe', or similar."
                "\n3. **Default Namespace**: If the query does not specify a namespace, assume 'default'."
                "\n4. **Status Queries**: For queries about pod or deployment status, return only the 'Running' status or the top-level summary without detailed YAML output."
                "\n5. **Service Naming**: Use 'service/<name>' when referring to services."
                "\n6. **No Abbreviations**: Avoid using flags like '--short'. Provide the full command explicitly."
                "\n7. **Invalid Queries**: If the query is unrelated to Kubernetes or cannot be processed, return 'Invalid query: unable to generate kubectl command'."
                "\n8. **Logs**: For logs, use 'kubectl logs <pod_name>'. If the container is not specified, assume the first container in the pod."
                "\n\n"
                "Always validate the context of the query and ensure compliance with these rules."
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

    #print(messages)
    try:
        response = openai.ChatCompletion.create(
        model="gpt-4o-mini-2024-07-18",
        messages=messages,
        response_format={
            "type": "text"
            },
            temperature=0,
            max_tokens=200,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
            )
        command = response['choices'][0]['message']['content'].strip()
        logging.info(f"Generated kubectl command: {command}")
        return command

    except Exception as e:
        logging.error("Error while generating kubectl command", exc_info=True)
        return "Error: Unable to generate kubectl command"