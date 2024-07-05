from pydantic import BaseModel
from typing import Optional

class TextInput(BaseModel):
    text: str
    style: Optional[str] = "default"
    use_claude: Optional[bool] = False
