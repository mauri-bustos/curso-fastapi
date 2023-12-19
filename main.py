from fastapi import FastAPI, Body, Path, Query, HTTPException, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.security.http import HTTPAuthorizationCredentials
from pydantic import BaseModel, Field
from typing import Any, Coroutine, Optional, List
import datetime

from starlette.requests import Request
from jwt_manager import create_token, validate_token
from fastapi.security import HTTPBearer

app = FastAPI()
app.title = 'Mauricio Bustos'

class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data['email'] !=  'admin@gmail.com':
            raise HTTPException(status_code = 403, detail = "Credenciales inválidas")

class User(BaseModel):
    email: str
    password: str

class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(max_length   = 30)
    overview: str = Field(max_length = 300)
    year: int = Field(le = datetime.date.today().year)
    rating: float
    category: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": 1,
                    "title": "Mi Pelicula",
                    "overview": "Descripcion de la pelicula",
                    "year": 2022,
                    "rating": 9.9,
                    "category": "Acción"
                }
            ]
        }
    }

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

@app.post('/login', tags=['Auth'])
def login(user: User):
    if user.email == "admin@gmail.com" and user.password == "admin":
        token: str = create_token(user.model_dump())
        return JSONResponse(status_code = 200, content = token)

@app.get('/movies', tags=['Movies'], response_model = List[Movie], status_code = 200, dependencies = [Depends(JWTBearer())])
def get_movies() -> List[Movie]:
    return JSONResponse(status_code = 200, content = movies)

@app.get('/movies/{id}', tags=['Movies'], response_model = Movie)
def get_movie(id: int = Path(ge = 1)) -> Movie:
    for item in movies:
        if item['id'] == id:
            return JSONResponse(content = item)
    return JSONResponse(status_code = 404, content = [])

@app.get('/movies/', tags=['Movies'], response_model = List[Movie], status_code = 200)
def get_movies_by_categories(category: str = Query(min_length = 5, max_length = 30)) -> List[Movie]:
    data = [item for item in movies if item['category'] == category] 
    return JSONResponse(status_code = 200, content = data)

@app.post('/movies', tags=['Movies'], response_model = dict, status_code = 201)
def create_movie(movie: Movie) -> dict:
    movies.append(movie.model_dump())
    return JSONResponse(status_code = 201, content = {"Mensaje": "La pelicula se registró correctamente"})

@app.put('/movies/{id}', tags=['Movies'], response_model = dict, status_code = 200)
def update_movie(id: int, movie: Movie) -> dict:
    for item in movies:
        if item['id'] == id:
            item['title'] = movie.title
            item['overview'] = movie.overview
            item['year'] = movie.year
            item['rating'] = movie.rating
            item['category'] = movie.category
            return JSONResponse(status_code = 200, content = {"Mensaje": "La pelicula se modificó correctamente"})
    return []

@app.delete('/movies/{id}', tags=['Movies'], response_model = dict, status_code = 200)
def delete_movie(id: int) -> dict:
    for item in movies:
        if item['id'] == id:
            movies.remove(item)
    return JSONResponse(status_code = 200, content = {"Mensaje": "La pelicula se eliminó correctamente"})
    