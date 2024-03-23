 

from pydantic import BaseModel  

class SomeRequestModel(BaseModel):
    """
   Model Request for some endpoint
    """ 
    text: str
    id: int
 