from pydantic import BaseModel, ConfigDict

class UploadBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)