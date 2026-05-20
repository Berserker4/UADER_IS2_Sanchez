#!/usr/bin/python3
# * TP5 - Punto 5


class Memento:

    def __init__(self, file, content):
        self.file = file
        self.content = content


class FileWriterUtility:

    def __init__(self, file):
        self.file = file
        self.content = ""

    def write(self, string):
        self.content += string

    def save(self):
        return Memento(self.file, self.content)

    def undo(self, memento):
        self.file = memento.file
        self.content = memento.content


class FileWriterCaretaker:

    CAPACIDAD = 4

    def __init__(self):
        self._historial = []

    def save(self, writer):
        if len(self._historial) == self.CAPACIDAD:
            self._historial.pop(0)
        self._historial.append(writer.save())

    def undo(self, writer, n=0):
        if not self._historial:
            print("No hay estados guardados.")
            return
        if n < 0 or n >= len(self._historial):
            print(f"Indice {n} fuera de rango (hay {len(self._historial)} estados guardados).")
            return
        memento = self._historial[-1 - n]
        writer.undo(memento)


if __name__ == "__main__":
    print("Crea un objeto que gestionara las versiones anteriores")
    caretaker = FileWriterCaretaker()

    print("Crea el objeto cuyo estado se quiere preservar")
    writer = FileWriterUtility("GFG.txt")

    print("\nEstado 1: se graba y se salva")
    writer.write("Clase de IS2 en UADER\n")
    print(writer.content)
    caretaker.save(writer)

    print("\nEstado 2: se graba y se salva")
    writer.write("Material adicional de la clase de patrones\n")
    print(writer.content)
    caretaker.save(writer)

    print("\nEstado 3: se graba y se salva")
    writer.write("Material adicional de la clase de patrones II\n")
    print(writer.content)
    caretaker.save(writer)

    print("\nEstado 4: se graba y se salva")
    writer.write("Material adicional de la clase de patrones III\n")
    print(writer.content)
    caretaker.save(writer)

    print("\nEstado 5: se graba sin salvar (5to estado, fuera del historial de 4)")
    writer.write("Material adicional de la clase de patrones IV\n")
    print(writer.content)

    print("\nundo(0) -> estado inmediato anterior")
    caretaker.undo(writer, 0)
    print(writer.content)

    print("\nundo(2) -> dos pasos atras")
    caretaker.undo(writer, 2)
    print(writer.content)

    print("\nundo(3) -> el mas antiguo retenido (cuarto hacia atras)")
    caretaker.undo(writer, 3)
    print(writer.content)

    print("undo(4) -> fuera de rango")
    caretaker.undo(writer, 4)
