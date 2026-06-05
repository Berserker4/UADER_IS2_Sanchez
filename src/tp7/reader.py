# TP7
"""
Capa de abstraccion para lectura de claves JSON (Branching by abstraction).

Permite converger entre la implementacion legada (TP6) y la refactorizada
con Singleton, sin modificar el punto de entrada del programa.
"""
import json
from abc import ABC, abstractmethod
from pathlib import Path


class ErrorPrograma(Exception):
    """Error controlado del programa; no expone excepciones del sistema."""


class LectorJson(ABC):
    """Interfaz abstracta: contrato comun para ambas ramas de implementacion."""

    def __init__(self):
        pass

    @abstractmethod
    def obtener(self, clave):
        """Devuelve el valor asociado a la clave en sitedata.json."""

    def nombre_archivo(self):
        """Nombre del archivo JSON configurado (metodo de soporte del contrato)."""
        return getattr(self, '_archivo', 'sitedata.json')


class LectorLegado(LectorJson):
    """Rama legada: replica el comportamiento procedural del TP6."""

    def __init__(self, archivo_json='sitedata.json'):
        super().__init__()
        self._archivo = archivo_json

    def obtener(self, clave):
        ruta = Path(self._archivo)
        if not ruta.is_file():
            raise ErrorPrograma(f"No se encontro el archivo '{self._archivo}'")
        try:
            with ruta.open('r', encoding='utf-8') as archivo:
                datos = json.load(archivo)
        except json.JSONDecodeError as exc:
            raise ErrorPrograma(f"JSON invalido en '{self._archivo}': {exc}") from exc
        except OSError as exc:
            raise ErrorPrograma(f"No se pudo leer '{self._archivo}': {exc}") from exc
        if clave not in datos:
            raise ErrorPrograma(f"La clave '{clave}' no existe en {self._archivo}")
        return datos[clave]


class GetJasonSingleton(LectorJson):
    """
    Rama refactorizada: Singleton que centraliza la carga del JSON.

    Una unica instancia comparte el estado en memoria para toda la aplicacion.
    """

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


def crear_lector(usar_singleton=True, archivo_json='sitedata.json'):
    """
    Branching by abstraction: selecciona la rama de implementacion.

    usar_singleton=True  -> GetJasonSingleton (refactorizado)
    usar_singleton=False -> LectorLegado (compatible con TP6)
    """
    if usar_singleton:
        return GetJasonSingleton(archivo_json)
    return LectorLegado(archivo_json)
