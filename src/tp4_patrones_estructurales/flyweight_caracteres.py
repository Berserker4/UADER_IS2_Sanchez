#!/usr/bin/python3
# * TP4 - Punto 5 : Patron Flyweight                                        *
import sys


class Glyph:
    """Estado intrinseco: caracter + fuente + tamaño (compartido)."""

    def __init__(self, caracter, fuente, tamano):
        self.caracter = caracter
        self.fuente = fuente
        self.tamano = tamano

    def dibujar(self, x, y):
        print(f"  '{self.caracter}' en ({x},{y})  [{self.fuente} {self.tamano}pt]")


class GlyphFactory:
    """Garantiza que cada combinacion (char,fuente,tamaño) exista una sola vez."""

    def __init__(self):
        self._cache = {}

    def obtener(self, caracter, fuente, tamano):
        clave = (caracter, fuente, tamano)
        if clave not in self._cache:
            self._cache[clave] = Glyph(caracter, fuente, tamano)
        return self._cache[clave]

    def cantidad_creada(self):
        return len(self._cache)


class Documento:
    """Almacena posiciones y referencias compartidas a glyphs."""

    def __init__(self, fabrica):
        self._fabrica = fabrica
        self._items = []

    def escribir(self, texto, fuente="Arial", tamano=12, fila=0):
        for col, ch in enumerate(texto):
            glyph = self._fabrica.obtener(ch, fuente, tamano)
            self._items.append((glyph, col, fila))

    def renderizar(self):
        for glyph, x, y in self._items:
            glyph.dibujar(x, y)


def _demo():
    fabrica = GlyphFactory()
    doc = Documento(fabrica)

    doc.escribir("HOLA MUNDO", fuente="Arial", tamano=12, fila=0)
    doc.escribir("HOLA",       fuente="Arial", tamano=12, fila=1)

    print("--- Render del documento ---")
    doc.renderizar()

    total_caracteres = sum(1 for _ in doc._items)
    print(
        f"\nCaracteres en el documento : {total_caracteres}"
        f"\nGlyphs distintos creados   : {fabrica.cantidad_creada()}"
        f"\nAhorro = se reutilizo cada glyph para todas sus apariciones."
    )


if __name__ == "__main__":
    _demo()
    sys.exit(0)
