from pydantic import BaseModel
from typing import List

class Nutr(BaseModel):
    callories: int
    proteins: int
    carbs: int


class Recipe(BaseModel):
    id: str
    name: str
    ingredients: str
    recipe: str
    img_url: str
    nutrition_info: Nutr
    recipe_url: str


class Ingredients(BaseModel):
    ingrs_list: List[str] = ['', '', '', '', '']
