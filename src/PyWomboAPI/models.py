from dataclasses import dataclass, field


@dataclass
class Credentials:
    api_key:str
    auth_token:str
@dataclass
class Task:
    id: int
    state: str
    completed: bool
    url: str = field(default=None, init=False)
    bearer: str

