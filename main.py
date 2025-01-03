import logging
from flask import Flask, request, jsonify
from pydantic import BaseModel, ValidationError
from coreenginesvc import handle_query

# Configure logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s - %(message)s',
                    filename='agent.log', filemode='a')

app = Flask(__name__)

class QueryResponse(BaseModel):
    query: str
    answer: str

@app.route('/query', methods=['POST'])
def create_query():
    try:
        # Extract query from request
        request_data = request.json
        query = request_data.get('query')

        # Log the query
        logging.info(f"Received query: {query}")

        # Handle the query
        answer = handle_query(query)

        # Log the response
        logging.info(f"Generated answer: {answer}")

        # Create the response model
        response = QueryResponse(query=query, answer=answer)
        return jsonify(response.model_dump())

    except ValidationError as e:
        logging.error(f"Validation error: {e}")
        return jsonify({"error": e.errors()}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
