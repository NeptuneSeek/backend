from pydantic import BaseModel


class SearchModel(BaseModel):
    search: str