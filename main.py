from fastapi import FastAPI

app = FastAPI()

# Тестовый маршрут
@app.get("/")
def read_root():
    return {"message": "Welcome to Open Research Hub!"}

# Новый маршрут (пример поиска)
@app.get("/articles")
def get_articles():
    return {"articles": ["Article 1", "Article 2", "Article 3"]}
