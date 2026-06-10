# TP8
"""
Lector JSON con Singleton (heredado de TP7).

Resuelve la relacion banco/token -> clave API desde sitedata.json.
"""
import json
from abc import ABC, abstractmethod
from pathlib import Path


class ErrorPrograma(Exception):
    """Error controlado del dominio de la aplicacion."""


class LectorJson(ABC):
    """Contrato abstracto para lectura de claves JSON."""

    def __init__(self):
        pass

    @abstractmethod
    def obtener(self, clave):
        """Devuelve el valor asociado a la clave en sitedata.json."""

    def nombre_archivo(self):
        """Ruta del archivo JSON configurado."""
        return getattr(self, '_archivo', 'sitedata.json')


class GetJasonSingleton(LectorJson):
    """Singleton: una instancia compartida para resolver tokens bancarios."""

    _instancia = None

    def __new__(cls, archivo_json='sitedata.json'):
        if cls._instancia is None:
            instancia = super().__new__(cls)
            instancia._archivo = archivo_json
            instancia._datos = None
            cls._instancia = instancia
        return cls._instancia

    def __init__(self, archivo_json='sitedata.json'):
        super().__init__()
        if getattr(self, '_inicializado', False):
            return
        self._archivo = archivo_json
        self._datos = None
        self._inicializado = True

    def _cargar(self):
        if self._datos is not None:
            return
        ruta = Path(self._archivo)
        if not ruta.is_file():
            raise ErrorPrograma(f"No se encontro el archivo '{self._archivo}'")
        try:
            with ruta.open('r', encoding='utf-8') as archivo:
                self._datos = json.load(archivo)
        except json.JSONDecodeError as exc:
            raise ErrorPrograma(f"JSON invalido en '{self._archivo}': {exc}") from exc
        except OSError as exc:
            raise ErrorPrograma(f"No se pudo leer '{self._archivo}': {exc}") from exc

    def obtener(self, clave):
        self._cargar()
        if clave not in self._datos:
            raise ErrorPrograma(f"La clave '{clave}' no existe en {self._archivo}")
        return self._datos[clave]
