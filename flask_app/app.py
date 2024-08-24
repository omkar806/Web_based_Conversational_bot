
from flask import Flask, request,jsonify
import os
import google.generativeai as genai
import utils as ut
# Load environment variables from .env file

app = Flask(__name__)

@app.route('/query', methods=['POST'])
def query():
    """
    Handles the POST request to '/query'. Extracts the query from the request,
    processes it through the search, concatenate, and generate functions,
    and returns the generated answer.
    """
    if request.is_json:
        # If the content type is application/json
        query = request.json.get('query')
    # get the data/query from streamlit app
    print("Received query: ", query)
    
    # Step 1: Search and scrape articles based on the query
    print("Step 1: searching articles")
    articles=ut.search_articles(query)
    # Step 2: Concatenate content from the scraped articles
    print("Step 2: concatenating content")
    extracted_content = ut.fetch_article_content(articles)
    # Step 3: Generate an answer using the LLM
    print("Step 3: generating answer")
    llm_response = ut.generate_answer(extracted_content,query)
    # return the jsonified text back to streamlit
    return jsonify({"answer": llm_response})

if __name__ == '__main__':
    app.run(host='localhost', port=5001)
