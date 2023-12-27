from fastapi import APIRouter
from fastapi import Path, Query, Depends
from fastapi.responses import JSONResponse
from typing import List
from config.database import SessionLocal
from models.movie import Movie as MovieModel
from fastapi.encoders import jsonable_encoder
from middlewares.jwt_bearer import JWTBearer
from services.movie import MovieService
from schemas.movie import Movie

movie_router = APIRouter()

@movie_router.get('/movies', tags=['Movies'], response_model = List[Movie], status_code = 200, dependencies = [Depends(JWTBearer())])
def get_movies() -> List[Movie]:
    db = SessionLocal()
    result = MovieService(db).get_movies()
    return JSONResponse(status_code = 200, content = jsonable_encoder(result))

@movie_router.get('/movies/{id}', tags=['Movies'], response_model = Movie)
def get_movie(id: int = Path(ge = 1)) -> Movie:
    db = SessionLocal()
    result = MovieService(db).get_movie(id)
    if not result:
        return JSONResponse(status_code = 404, content = {'Mensaje': 'No encontrado'})
    return JSONResponse(status_code = 200, content = jsonable_encoder(result))

@movie_router.get('/movies/', tags=['Movies'], response_model = List[Movie], status_code = 200)
def get_movies_by_categories(category: str = Query(min_length = 5, max_length = 30)) -> List[Movie]:
    db = SessionLocal()
    result = MovieService(db).get_movies_by_categories(category)
    if not result:
        return JSONResponse(status_code = 404, content = jsonable_encoder({'Mensaje': 'Categoría inexistente'}))
    return JSONResponse(status_code = 200, content = jsonable_encoder(result))

@movie_router.post('/movies', tags=['Movies'], response_model = dict, status_code = 201)
def create_movie(movie: Movie) -> dict:
    db = SessionLocal()
    MovieService(db).create_movie(movie)
    return JSONResponse(status_code = 201, content = {"Mensaje": "La pelicula se registró correctamente"})

@movie_router.put('/movies/{id}', tags=['Movies'], response_model = dict, status_code = 200)
def update_movie(id: int, movie: Movie) -> dict:
    db = SessionLocal()
    result = MovieService(db).get_movie(id)
    if not result:
        return JSONResponse(status_code = 404, content = jsonable_encoder({'Mensaje': 'No se encontró'}))
    MovieService(db).update_movie(id, movie)
    return JSONResponse(status_code = 200, content = {"Mensaje": "La pelicula se modificó correctamente"})
    

@movie_router.delete('/movies/{id}', tags=['Movies'], response_model = dict, status_code = 200)
def delete_movie(id: int) -> dict:
    db = SessionLocal()
    result = MovieService(db).get_movie(id)
    if not result:
        return JSONResponse(status_code = 404, content = jsonable_encoder({'Mensaje': 'No se encontró'}))
    MovieService(db).delete_movie(id)
    return JSONResponse(status_code = 200, content = {"Mensaje": "La pelicula se eliminó correctamente"})