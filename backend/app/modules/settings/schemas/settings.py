from pydantic import BaseModel, ConfigDict

class SettingBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)