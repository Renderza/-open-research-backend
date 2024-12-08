from fastapi import FastAPI, Query
import requests

app = FastAPI()

# Корневой маршрут
@app.get("/")
def read_root():
    return {"message": "Welcome to Open Research Hub!"}

# Поиск статей через внешние API
@app.get("/search")
def search_articles(query: str = Query(..., description="Search query")):
    results = []

    # Поиск в CORE API
    core_url = f"https://api.core.ac.uk/v3/search?q={query}"
    core_response = requests.get(core_url)
    if core_response.status_code == 200:
        core_data = core_response.json()
        for item in core_data.get("results", []):
            results.append({
                "title": item.get("title"),
                "authors": item.get("authors"),
                "abstract": item.get("abstract"),
                "source": "CORE",
                "url": item.get("downloadUrl")
            })

    # Поиск в arXiv API
    arxiv_url = f"http://export.arxiv.org/api/query?search_query=all:{query}&start=0&max_results=5"
    arxiv_response = requests.get(arxiv_url)
    if arxiv_response.status_code == 200:
        import xml.etree.ElementTree as ET
        root = ET.fromstring(arxiv_response.text)
        for entry in root.findall("{http://www.w3.org/2005/Atom}entry"):
            results.append({
                "title": entry.find("{http://www.w3.org/2005/Atom}title").text,
                "authors": [author.find("{http://www.w3.org/2005/Atom}name").text 
                            for author in entry.findall("{http://www.w3.org/2005/Atom}author")],
                "abstract": entry.find("{http://www.w3.org/2005/Atom}summary").text.strip(),
                "source": "arXiv",
                "url": entry.find("{http://www.w3.org/2005/Atom}id").text
            })

    return {"results": results}
