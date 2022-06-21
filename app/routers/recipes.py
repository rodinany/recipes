from fastapi import APIRouter, status
import pandas as pd
import requests
from bs4 import BeautifulSoup
from app.schemas.recipes import Recipe, Ingredients


router = APIRouter()
df = pd.read_csv(r'C:\Users\rodin\PycharmProjects\ColingPython-p2\seminar_5\app\routers\eda.csv')


@router.get('/recipes/query')
def search_recipies(query: str) -> dict:
    result = []
    for i in df['name']:
        if query.lower() in i.lower():
            res_rep = {
                'id': df.loc[df['name'] == i, 'id'].values[0],
                'name': i
            }
            result.append(res_rep)
    return result


@router.get('/recipes/{id}')
def seacrh_id(id: str) -> dict:
    for i in df['id']:
        if i == id:
            response = requests.get(df.loc[df['id'] == i, 'recept_link'].values[0])
            soup = BeautifulSoup(response.text, 'lxml')
            likes = soup.find('span', class_='emotion-1w5q7lf').text
            res_recp = {
                'id': i,
                'name': df.loc[df['id'] == i, 'name'].values[0],
                "ingredients": df.loc[df['id'] == i, 'list_ingrid'].values[0],
                "recipe": df.loc[df['id'] == i, 'list_resipe'].values[0],
                "img_url": df.loc[df['id'] == i, 'image_url'].values[0],
                "nutrition_info": {
                     "callories": int(df.loc[df['id'] == i, 'cal'].values[0]),
                     "proteins": df.loc[df['id'] == i, 'protein'].values[0],
                     "carbs": df.loc[df['id'] == i, 'carb'].values[0]
                },
                "recipe_url": df.loc[df['id'] == i, 'recept_link'].values[0],
                "likes": likes
            }
            return res_recp


@router.get('/recipes/random/')
def random_rec() -> dict:
    recipe = df.sample()
    response = requests.get(recipe['recept_link'].values[0])
    soup = BeautifulSoup(response.text, 'lxml')
    likes = soup.find('span', class_='emotion-1w5q7lf').text
    result = {
        'id': recipe['id'].values[0],
        'name': recipe['name'].values[0],
        "ingredients": recipe['list_ingrid'].values[0],
        "recipe": recipe['list_resipe'].values[0],
        "img_url": recipe['image_url'].values[0],
        "nutrition_info": {
            "callories": int(recipe['cal'].values[0]),
            "proteins": recipe['protein'].values[0],
            "carbs": recipe['carb'].values[0]
        },
        "recipe_url": recipe['recept_link'].values[0],
        "likes": likes
    }
    return result


@router.get('/recipes/diet/')
def top_cal(calories: int, topn: int) -> dict:
    cal_df = df[df['cal'] <= calories].sort_values(by='cal', ascending=False).head(topn)
    result = []
    for i in cal_df['id']:
        res_rec = {
            "id": i,
            "name": cal_df.loc[cal_df['id'] == i, 'name'].values[0],
            "nutritiion_info": {
                "callories": int(cal_df.loc[cal_df['id'] == i, 'cal'].values[0]),
                "proteins": cal_df.loc[cal_df['id'] == i, 'protein'].values[0],
                "carbs": cal_df.loc[cal_df['id'] == i, 'carb'].values[0]
            }
        }
        result.append(res_rec)
    if result:
        return result


@router.get('/recipes/')
def top_dif(difficulty: str, topn: int) -> dict:
    dif_df = pd.read_csv(open(r'C:\Users\rodin\PycharmProjects\ColingPython-p2\seminar_5\app\routers\difficulty.csv',
                              'r', errors='ignore'),
                         names=['id', 'name', 'difficulty'])
    result = []
    if difficulty == 'hard':
        for i in dif_df.sort_values(by='difficulty', ascending=False).head(topn)['id']:
            res_rec = {'id': i,
                       'name': df.loc[df['id'] == i, 'name'].values[0],
                       'difficulty': dif_df.loc[dif_df['id'] == i, 'difficulty'].values[0]
                       }
            result.append(res_rec)
        return result
    elif difficulty == 'simple':
        for i in dif_df.sort_values(by='difficulty').head(topn)['id']:
            res_rec = {'id': i,
                       'name': df.loc[df['id'] == i, 'name'].values[0],
                       'difficulty': dif_df.loc[dif_df['id'] == i, 'difficulty'].values[0]
                       }
            result.append(res_rec)
        return result
    else:
        return 'the request is not recognized'

@router.put('/recipes/new', status_code=status.HTTP_201_CREATED)
def add_recipe(recipe: Recipe):
    new_row = pd.DataFrame({"id": recipe.id,
                            "name": recipe.name,
                            "ingredients": recipe.ingredients,
                            "recipe": recipe.recipe,
                            "img_url": recipe.img_url,
                            "nutrition_info": {
                                'callories': recipe.nutrition_info.callories,
                                "proteins": recipe.nutrition_info.proteins,
                                "carbs": recipe.nutrition_info.carbs
                            },
                            "recipe_url": recipe.recipe_url
                            })
    df.append(new_row)
    return recipe

@router.post('/recipes/search')
def search_by_ingr(ingr: Ingredients):

    def strip(string):
        return string.strip("'',")

    result = []
    for i in df['ingridient_keywords']:
        list_i = i.strip("{}").split()
        new_list = list(map(strip, list_i))
        if set(ingr.ingrs_list) <= set(new_list):
            res_rec = {'id': df.loc[df['ingridient_keywords'] == i, 'id'].values[0],
                       'name': df.loc[df['ingridient_keywords'] == i, 'name'].values[0],
                       'ingredients': i
            }
            result.append(res_rec)
    if result:
        return result
    else:
        return 'recipes not found'

