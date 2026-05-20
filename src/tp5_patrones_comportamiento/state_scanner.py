#!/usr/bin/python3
# * TP5 - Punto 4


class State:

    def scan(self):
        self.pos += 1
        if self.pos == len(self.stations):
            self.pos = 0
        print("Sintonizando... Estacion {} {}".format(self.stations[self.pos], self.name))


class AmState(State):

    def __init__(self, radio):
        self.radio = radio
        self.stations = ["1250", "1380", "1510"]
        self.pos = 0
        self.name = "AM"

    def toggle_amfm(self):
        print("Cambiando a FM")
        self.radio.state = self.radio.fmstate


class FmState(State):

    def __init__(self, radio):
        self.radio = radio
        self.stations = ["81.3", "89.1", "103.9"]
        self.pos = 0
        self.name = "FM"

    def toggle_amfm(self):
        print("Cambiando a AM")
        self.radio.state = self.radio.amstate


class MemoryState(State):

    def __init__(self, radio, etiqueta, banda, frecuencia):
        self.radio = radio
        self.etiqueta = etiqueta
        self.banda = banda
        self.stations = [frecuencia]
        self.pos = 0
        self.name = f"{banda} (memoria {etiqueta})"

    def scan(self):
        print("Sintonizando... Estacion {} {}".format(self.stations[0], self.name))

    def toggle_amfm(self):
        print("Las memorias no cambian de banda")


class Radio:

    def __init__(self):
        self.fmstate = FmState(self)
        self.amstate = AmState(self)

        self.memorias = [
            MemoryState(self, "M1", "AM", "1380"),
            MemoryState(self, "M2", "FM", "103.9"),
            MemoryState(self, "M3", "AM", "1510"),
            MemoryState(self, "M4", "FM", "89.1"),
        ]

        self.state = self.fmstate

    def toggle_amfm(self):
        self.state.toggle_amfm()

    def scan(self):
        self.state.scan()

    def scan_memorias(self):
        estado_previo = self.state
        for memoria in self.memorias:
            self.state = memoria
            self.state.scan()
        self.state = estado_previo


if __name__ == "__main__":
    print("\nCrea un objeto radio y almacena las siguientes acciones")
    radio = Radio()
    actions = (
        [radio.scan] * 3
        + [radio.toggle_amfm]
        + [radio.scan] * 3
        + [radio.scan_memorias]
    )
    actions *= 2

    print("Recorre las acciones; el objeto cambia su interfaz segun el estado")
    for action in actions:
        action()
