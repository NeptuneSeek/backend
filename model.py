from pydantic import BaseModel


class SearchQuery(BaseModel):
    search_query: str