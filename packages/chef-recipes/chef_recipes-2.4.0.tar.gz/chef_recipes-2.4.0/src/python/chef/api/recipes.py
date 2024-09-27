from typing import List, cast, Union

import httpx
from fastapi import APIRouter, HTTPException, UploadFile
from loguru import logger
from sqlalchemy.orm import Session

from chef.api.common import generic_get
from chef.controllers import RecipesController, IngredientsController
from chef.models import engine
from chef.schemas import Recipe, CreateOrUpdateRecipe, RecipeListItem
from chef.settings import settings

router = APIRouter()
recipes = RecipesController()
ingredients = IngredientsController()


# Store the current recipe id in memory
CURRENT_RECIPES_IDS = []


@router.get("")
async def get_recipes(
        category: int = None,
        favorite: bool = False,
) -> list[RecipeListItem]:

    with Session(engine()) as session:
        if favorite:
            return cast(
                List[RecipeListItem],
                await recipes.get_all_and_filter(session, favorite=favorite)
            )

        if category:
            return cast(
                List[RecipeListItem],
                await recipes.get_by_category(session, category)
            )

        return cast(
            List[RecipeListItem],
            sorted(await recipes.get_all(session), key=lambda rec: rec.title)
        )


@router.get("/details")
async def get_recipes_with_details(category: int = None, favorite: bool = False) -> list[Recipe]:
    with Session(engine()) as session:
        if favorite:
            return await recipes.get_all_and_filter(session, favorite=favorite)

        if category:
            return await recipes.get_by_category(session, category)

        return sorted(await recipes.get_all(session), key=lambda rec: rec.title)


@router.get("/{item_id}")
async def get_recipe(item_id: int) -> Recipe:
    with Session(engine()) as session:
        return await recipes.get_single(session, item_id)


@router.post("/{item_id}/parse", response_model=None)
async def parse_recipe(item_id: int) -> any:
    with Session(engine()) as session:
        recipe = await recipes.get_single(session, item_id)

    async with httpx.AsyncClient() as client:
        response = await client.post(
            settings.gpt_enpoint_url,
            json={
                "message": recipe.body,
            },
            headers={"content_type": "application/json"},
            timeout=30.0
        )
        response.raise_for_status()
    parsed_ingredients = response.json()["response"]["ingredients"]

    return parsed_ingredients


@router.delete("/{item_id}")
async def delete_recipe(item_id: int) -> None:
    with Session(engine()) as session:
        await recipes.delete_single(session, item_id)


@router.post('', status_code=201)
async def create_recipe(create_data: CreateOrUpdateRecipe) -> Recipe:

    if any(not i.ingredient.name for i in create_data.ingredients):
        raise HTTPException(
            status_code=400,
            detail="Empty ingredient name not allowed.",
        )

    with Session(engine()) as session:
        return await recipes.create(session, create_data)


@router.put('/{item_id}')
async def update_recipe(item_id: int, update_data: CreateOrUpdateRecipe) -> Recipe:

    if any(not i.ingredient.name for i in update_data.ingredients):
        raise HTTPException(
            status_code=400,
            detail="Empty ingredient name not allowed."
        )

    with Session(engine()) as session:
        return await recipes.update(session, item_id, update_data)


@router.post('/{recipe_id}/thumbnail-image')
async def post_recipe_thumbnail(recipe_id: int, image: UploadFile):
    await generic_get(recipes, recipe_id)
    logger.debug(f"uploading thumbnail for recipe (id={recipe_id}) image: {image.filename}, {image.size / 1000}kB")
    with Session(engine()) as session:
        recipes.update_thumbnail(session, recipe_id, image.file)
        session.commit()

    return await generic_get(recipes, recipe_id)


@router.post('/{recipe_id}/detail-image')
async def post_recipe_image(recipe_id: int, image: UploadFile) -> Recipe:
    await generic_get(recipes, recipe_id)
    logger.debug(f"uploading image for recipe (id={recipe_id}) image: {image.filename}, {image.size / 1000}kB")
    with Session(engine()) as session:
        recipes.update_image(session, recipe_id, image.file)
        session.commit()

    return await generic_get(recipes, recipe_id)
