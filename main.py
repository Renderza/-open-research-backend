from fastapi import FastAPI, Query
import requests

app = FastAPI()

# Корневой маршрут
@app.get("/")
def read_root():
    return {"message": "Welcome to Open Research Hub!"}

# Исправленный маршрут поиска статей
@app.get("/search")
def search_articles(query: str, max_results: int = 5):
    results = []

    # Поиск в arXiv API
    arxiv_url = f"http://export.arxiv.org/api/query?search_query=all:{query}&start=0&max_results={max_results}"
    arxiv_response = requests.get(arxiv_url)

    if arxiv_response.status_code == 200:
        import xml.etree.ElementTree as ET
        root = ET.fromstring(arxiv_response.text)

        # Обработка каждой статьи
        for entry in root.findall("{http://www.w3.org/2005/Atom}entry"):
            results.append({
                "title": entry.find("{http://www.w3.org/2005/Atom}title").text.strip(),
                "authors": [author.find("{http://www.w3.org/2005/Atom}name").text 
                            for author in entry.findall("{http://www.w3.org/2005/Atom}author")],
                "abstract": entry.find("{http://www.w3.org/2005/Atom}summary").text.strip(),
                "source": "arXiv",
                "url": entry.find("{http://www.w3.org/2005/Atom}id").text
            })

    return {"results": results}



