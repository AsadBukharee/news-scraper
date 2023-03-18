from pydantic import BaseModel


class News(BaseModel):
    name: str = 'filgoal'
    url: str = 'https://www.filgoal.com/articles/'
    interval: int = 200