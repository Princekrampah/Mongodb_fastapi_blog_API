# library imports
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from datetime import datetime
from typing import List

# module imports
from ..schemas import BlogContent, BlogContentResponse, db
from .. import oauth2

router = APIRouter(
    prefix="/blog",
    tags=["Blog Content"]
)


@router.post("/", response_description="Create Post Content", response_model=BlogContentResponse)
async def read_item(blog_content: BlogContent, current_user=Depends(oauth2.get_current_user)):

    try:
        # jsonize the data
        blog_content = jsonable_encoder(blog_content)

        # add the additional info
        blog_content["auther_name"] = current_user["name"]
        blog_content["auther_id"] = current_user["_id"]
        blog_content["created_at"] = str(datetime.utcnow())

        # create blogPost collection
        new_blog_content = await db["blogPost"].insert_one(blog_content)

        # get created post content
        created_blog_post = await db["blogPost"].find_one({"_id": new_blog_content.inserted_id})

        print(new_blog_content.inserted_id)
        return created_blog_post
    
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )


@router.get("/", response_description="Get Blog Posts", response_model= List[BlogContentResponse])
async def get_blog_posts(limit: int = 4, orderby: str = "created_at"):
    try:
        blog_posts = await db["blogPost"].find({ "$query": {}, "$orderby": { orderby : -1 } }).to_list(limit)
        return blog_posts
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )


@router.get("/{id}", response_description="Get Blog Post", response_model= BlogContentResponse)
async def get_blog_post(id: str):
    try:
        blog_post = await db["blogPost"].find_one({"_id": id})
        return blog_post
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )


@router.put("/{id}", response_description="Update a blog Post", response_model=BlogContentResponse)
async def update_blog_post(id: str, blog_content: BlogContent, current_user = Depends(oauth2.get_current_user)):

    if blog_post := await db["blogPost"].find_one({"_id": id}):
        print(blog_post)
        # check if the owner is the currently logged in user
        if blog_post["auther_id"] == current_user["_id"]:
            print("owner")
            try:
                blog_content = {k: v for k, v in blog_content.dict().items() if v is not None}

                if len(blog_content) >= 1:
                    update_result = await db["blogPost"].update_one({"_id": id}, {"$set": blog_content})

                    if update_result.modified_count == 1:
                        if (updated_blog_post := await db["blogPost"].find_one({"_id": id})) is not None:
                            return updated_blog_post

                if (existing_blog_post := await db["blogPost"].find_one({"_id": id})) is not None:
                    return existing_blog_post

                raise HTTPException(status_code=404, detail=f"Blog Post {id} not found")

            except Exception as e:
                print(e)
                raise HTTPException(
                    status_code=500,
                    detail="Internal server error"
                )
        else:
            raise HTTPException(status_code=403, detail=f"You are not the owner of this blog post")


@router.delete("/{id}", response_description="Get Blog Post", )
async def get_blog_post(id: str, current_user = Depends(oauth2.get_current_user)):

    if blog_post := await db["blogPost"].find_one({"_id": id}):
        
        # check if the owner is the currently logged in user
        if blog_post["auther_id"] == current_user["_id"]:
            try:
                delete_result = await db["blogPost"].delete_one({"_id": id})

                if delete_result.deleted_count == 1:
                    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)

                raise HTTPException(status_code=404, detail=f"Blog Post {id} not found")

            except Exception as e:
                print(e)
                raise HTTPException(
                    status_code=500,
                    detail="Internal server error"
                )
        else:
            raise HTTPException(status_code=403, detail=f"You are not the owner of this blog post")