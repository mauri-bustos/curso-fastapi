from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from config.database import engine, Base
from middlewares.error_handler import ErrorHandler
from routers.movie import movie_router
from routers.user import user_router
import os
import uvicorn

app = FastAPI()
app.title = 'Películas'

app.add_middleware(ErrorHandler)
app.include_router(movie_router)
app.include_router(user_router)


Base.metadata.create_all(bind = engine)

movies = [
    {
        'id': 1,
        'title': 'Avatar',
        'overview': 'AVATAR nos lleva a un mundo situado más allá de la imaginación, en donde un recién llegado de la Tierra se embarca en una aventura épica, llegando a luchar, al final, por salvar el extraño mundo al que ha aprendido a llamar su hogar.',
        'year': 2009,
        'rating': 7.8,
        'category': 'Acción'
    },
    {
        'id': 2,
        'title': 'Titanic',
        'overview': 'AVATAR nos lleva a un mundo situado más allá de la imaginación, en donde un recién llegado de la Tierra se embarca en una aventura épica, llegando a luchar, al final, por salvar el extraño mundo al que ha aprendido a llamar su hogar.',
        'year': 1997,
        'rating': 7.8,
        'category': 'Drama'
    },
    {
        'id': 3,
        'title': 'Tonto y retonto',
        'overview': 'AVATAR nos lleva a un mundo situado más allá de la imaginación, en donde un recién llegado de la Tierra se embarca en una aventura épica, llegando a luchar, al final, por salvar el extraño mundo al que ha aprendido a llamar su hogar.',
        'year': 1994,
        'rating': 7.8,
        'category': 'Comedia'
    },
    {
        'id': 4,
        'title': 'Duro de matar',
        'overview': 'AVATAR nos lleva a un mundo situado más allá de la imaginación, en donde un recién llegado de la Tierra se embarca en una aventura épica, llegando a luchar, al final, por salvar el extraño mundo al que ha aprendido a llamar su hogar.',
        'year': 1988,
        'rating': 7.8,
        'category': 'Acción'
    },
    {
        'id': 5,
        'title': 'Harry Potter',
        'overview': 'AVATAR nos lleva a un mundo situado más allá de la imaginación, en donde un recién llegado de la Tierra se embarca en una aventura épica, llegando a luchar, al final, por salvar el extraño mundo al que ha aprendido a llamar su hogar.',
        'year': 1997,
        'rating': 7.8,
        'category': 'Fantasía'
    }
]

@app.get('/', tags=['Home'])
def message():
    return HTMLResponse('<h1>Hello World</h1>')

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0",
                port=int(os.environ.get("PORT", 5000)))