from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
from transformers import pipeline

# Initialize Flask app
app = Flask(__name__)

# Initialize the summarizer
summarizer = pipeline("summarization")

# Function to fetch and summarize content from a URL
def fetch_and_summarize(url):
    # Fetch the content from the URL
    response = requests.get(url)
    
    if response.status_code != 200:
        return "Error: Unable to fetch the content."
    
    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extract the text from the HTML (you can customize this)
    paragraphs = soup.find_all('p')
    text = " ".join([para.get_text() for para in paragraphs])
    
    if len(text) == 0:
        return "Error: No text found to summarize."
    
    # Generate the summary using transformers
    summary = summarizer(text, max_length=200, min_length=50, do_sample=False)
    
    return summary[0]['summary_text']

# Define the route for the home page
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        url = request.form["url"]
        if url:
            summary = fetch_and_summarize(url)
            return render_template("index.html", summary=summary, url=url)
    return render_template("index.html", summary=None)

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
