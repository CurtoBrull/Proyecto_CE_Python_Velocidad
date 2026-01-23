import requests
from django.conf import settings
from typing import Dict, Any, List, Optional


class RadarAPIClient:
    def __init__(self):
        self.base_url = getattr(settings, 'FASTAPI_BASE_URL', 'http://localhost:8080')
        self.timeout = 10

    def _get(self, endpoint: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        try:
            response = requests.get(
                f"{self.base_url}{endpoint}",
                params=params,
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e)}

    def _post(self, endpoint: str, data: Optional[Dict] = None) -> Dict[str, Any]:
        try:
            response = requests.post(
                f"{self.base_url}{endpoint}",
                json=data,
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e)}

    def _put(self, endpoint: str, data: Dict) -> Dict[str, Any]:
        try:
            response = requests.put(
                f"{self.base_url}{endpoint}",
                json=data,
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e)}

    def obtener_mediciones(
        self,
        skip: int = 0,
        limit: int = 20,
        fecha_inicio: Optional[str] = None,
        fecha_fin: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        params = {"skip": skip, "limit": limit, "solo_completas": True}
        if fecha_inicio:
            params["fecha_inicio"] = fecha_inicio
        if fecha_fin:
            params["fecha_fin"] = fecha_fin
        result = self._get("/mediciones/", params)
        return result if isinstance(result, list) else []

    def obtener_medicion(self, medicion_id: int) -> Dict[str, Any]:
        return self._get(f"/mediciones/{medicion_id}")

    def obtener_estadisticas(self) -> Dict[str, Any]:
        return self._get("/estadisticas/")

    def obtener_configuracion(self) -> List[Dict[str, Any]]:
        result = self._get("/configuracion/")
        return result if isinstance(result, list) else []

    def obtener_distancia(self) -> float:
        result = self._get("/configuracion/distancia_sensores")
        if "error" not in result:
            return float(result.get("valor", 100))
        return 100.0

    def actualizar_distancia(self, nueva_distancia: float) -> Dict[str, Any]:
        return self._put(
            "/configuracion/distancia_sensores",
            {"valor": str(nueva_distancia)}
        )

    def registrar_medicion(self) -> Dict[str, Any]:
        return self._post("/mediciones/")
