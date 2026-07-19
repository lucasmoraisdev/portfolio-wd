import json
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from sqlalchemy import select, delete
from sqlalchemy.orm import Session

from .models import SettingModel

class SettingsRepository:
    def __init__(self, db: Session) -> None:
        self._db = db
        self._cache = None

    def preload(self) -> None:
        stmt = select(SettingModel)
        settings = self._db.scalars(stmt).all()
        self._cache = {s.key: s for s in settings}

    def get_by_key(self, key: str) -> SettingModel | None:
        if self._cache is None:
            self.preload()
        return self._cache.get(key)
    
    def list_all(self, limit: int = 100, offset: int = 0) -> list[SettingModel]:
        stmt = (
            select(SettingModel)
            .order_by(SettingModel.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        return self._db.scalars(stmt).all()
    
    def get_public(self) -> list[SettingModel]:
        stmt = select(SettingModel).where(SettingModel.is_public)

        return self._db.scalars(stmt).all()
    
    def create_or_update(
        self,
        key: str,
        value: Any,
        type_: str = "string",
        is_public: bool = False
    ) -> SettingModel:
        setting = self.get_by_key(key)

        if setting:
            setting.value = self._serialize_value(value, type_)
            setting.type = type_
            setting.is_public = is_public
            setting.updated_at = datetime.now(timezone.utc)
        else:
            setting = SettingModel(
                id=uuid4(),
                key=key,
                value=self._serialize_value(value, type_),
                type=type_,
                is_public=is_public
            )
            self._db.add(setting)
            if self._cache is not None:
                self._cache[key] = setting
        
        self._db.commit()
        self._db.refresh(setting)
        
        if self._cache is not None:
            self._cache[key] = setting
            
        return setting
    
    def bulk_update(self, settings: dict[str, Any]) -> list[SettingModel]:
        updated = []
        for k, v in settings.items():
            type_ = self._infer_type(v)
            is_public = k.startswith(("company_", "hero_", "contact_", "social_", 
                "seo_", "theme_", "footer_"))
            setting = self.create_or_update(k, v, type_, is_public)

            updated.append(setting)
        return updated
    
    def delete(self, key: str) -> bool:
        setting = self.get_by_key(key)
        if not setting:
            return False
        self._db.delete(setting)
        self._db.commit()
        if self._cache is not None:
            self._cache.pop(key, None)
        return True
    
    def delete_by_prefix(self, prefix: str) -> int:
        stmt = delete(SettingModel).where(SettingModel.key.like(f"{prefix}%"))
        result = self._db.execute(stmt)
        self._db.commit()
        return result.rowcount
    
    @staticmethod
    def _serialize_value(value: Any, type_: str) -> Any:
        if value is None:
            return None
        if type_ == "json":
            return value if isinstance(value, (dict, list)) else json.loads(value)
        if type_ == "bool":
            return bool(value)
        if type_ == "int":
            return int(value)
        if type_ == "float":
            return float(value)
        return str(value)
    
    @staticmethod
    def _infer_type(value: Any) -> str:
        if value is None:
            return "string"
        if isinstance(value, bool):
            return "bool"
        if isinstance(value, int):
            return "int"
        if isinstance(value, float):
            return "float"
        if isinstance(value, (dict, list)):
            return "json"
        return "string"
        
        
        