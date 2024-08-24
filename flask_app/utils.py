import os
import requests
import json
import google.generativeai as genai

# Load API keys from environment variables
SERPER_API_KEY = os.getenv('X-API-KEY')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

def search_articles(query:str):
    """
    Searches for articles related to the query using Serper API.
    Returns a list of dictionaries containing article URLs, headings, and text.
    """
    articles = None
    # implement the search logic - retrieves articles
    url = "https://google.serper.dev/search"

    payload = json.dumps({
    "q":query
    })
    headers = {
    'X-API-KEY': SERPER_API_KEY,
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    articles = response.text
    return articles


def fetch_article_content(articles):
    """
    Fetches the article content, extracting headings and text.
    """
    content = ""
    # implementation of fetching headings and content from the articles
    data = json.loads(articles)

    # Extract from answerBox if it exists
    if 'answerBox' in data:
        if 'title' in data['answerBox']:
            content += data['answerBox']['title']+"\n"
        if 'snippet' in data['answerBox']:
            content += data['answerBox']['snippet']+"\n"

    # Extract from organic search results
    if 'organic' in data:
        for result in data['organic']:
            if 'title' in result:
                content += result['title']+"\n"
            if 'snippet' in result:
                content += result['snippet']+"\n"

    # Extract from peopleAlsoAsk
    if 'peopleAlsoAsk' in data:
        for question in data['peopleAlsoAsk']:
            if 'title' in question:
                content += question['title']+"\n"
            if 'snippet' in question:
                content += question['snippet']+"\n"
    return content.strip()


def generate_answer(content,query):
    """
    Generates an answer from the concatenated content using GPT-4.
    The content and the user's query are used to generate a contextual answer.
    """
    # Create the prompt based on the content and the query
    response = None
    system_prompt = f"""You are a helpful assistant. Use the following context to answer the user's query. If the context doesn't contain relevant information, say so.\n
    Below is the context : \n
    {content}\n
    Below is the user query:
    {query}\n
    Based on the user query above and the context given provide with highly accurate response for the user query . You should be very precise about the answer based on the user query and content.
    """

    response = model.generate_content(system_prompt)
    return response.text
    
