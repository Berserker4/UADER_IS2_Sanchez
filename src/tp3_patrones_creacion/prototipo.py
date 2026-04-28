#!/usr/bin/python3
# *-------------------------------------------------------------------------*
# * TP3 - Punto 6                                                           *
# *-------------------------------------------------------------------------*
import copy


class Prototipo:
    """Prototype base: provee clonacion profunda mediante clonar()."""

    def clonar(self):
        # deepcopy garantiza que las estructuras anidadas tambien se copien.
        return copy.deepcopy(self)


class Documento(Prototipo):
    """Objeto de ejemplo con estado mutable (lista anidada)."""

    def __init__(self, titulo, autor, secciones=None):
        self.titulo = titulo
        self.autor = autor
        self.secciones = list(secciones) if secciones else []

    def agregar_seccion(self, texto):
        self.secciones.append(texto)

    def __repr__(self):
        return (
            f"Documento(titulo={self.titulo!r}, autor={self.autor!r}, "
            f"secciones={self.secciones!r})"
        )


def _demo():
    # 1) Original
    original = Documento("Patrones GoF", "Sanchez", ["Introduccion"])
    print("Original :", original)

    # 2) Clon obtenido del original
    clon = original.clonar()
    clon.titulo = "Patrones GoF (revisado)"
    clon.agregar_seccion("Singleton")
    print("Clon     :", clon)

    # 3) Verificacion: el clon tambien sabe clonarse a si mismo
    sub_clon = clon.clonar()
    sub_clon.agregar_seccion("Builder")
    print("Sub-clon :", sub_clon)

    # 4) Independencia de instancias y de su estado anidado
    assert original is not clon
    assert clon is not sub_clon
    assert original.secciones == ["Introduccion"]
    assert clon.secciones == ["Introduccion", "Singleton"]
    assert sub_clon.secciones == ["Introduccion", "Singleton", "Builder"]
    print("OK: el clon tambien produce copias independientes de si mismo.")


if __name__ == "__main__":
    _demo()
