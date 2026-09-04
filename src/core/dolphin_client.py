import asyncio
from typing import List, Dict, Any, Optional
from pyanty import DolphinAnty
from loguru import logger

class DolphinClient:
    def __init__(self, token: Optional[str] = None):
        self.token = token
        self.client = DolphinAnty(token) if token else DolphinAnty()

    async def get_profiles(self) -> List[Dict[str, Any]]:
        try:
            profiles = await self.client.get_profiles()
            return [{"id": p.id, "name": p.name, "status": p.status} for p in profiles]
        except Exception as e:
            logger.error(f"Ошибка получения профилей: {e}")
            return []

    async def start_profile(self, profile_id: str) -> Optional[Dict[str, Any]]:
        try:
            data = await self.client.start_profile(profile_id)
            return {"port": data.get("port"), "wsEndpoint": data.get("wsEndpoint")}
        except Exception as e:
            logger.error(f"Ошибка запуска профиля {profile_id}: {e}")
            return None

    async def stop_profile(self, profile_id: str) -> bool:
        try:
            await self.client.stop_profile(profile_id)
            return True
        except Exception as e:
            logger.error(f"Ошибка остановки профиля {profile_id}: {e}")
            return False
