from pydantic import BaseModel, Field
from typing import Optional
import datetime

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
