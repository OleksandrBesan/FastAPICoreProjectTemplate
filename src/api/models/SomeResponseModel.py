 

from pydantic import BaseModel 
from typing import List 

class SomeResponseModel(BaseModel):
    """
    Response model with some result
    """ 
    result: bool
 