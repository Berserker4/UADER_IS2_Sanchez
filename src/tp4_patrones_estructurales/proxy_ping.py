#!/usr/bin/python3
# * TP4 - Punto 1 : Patron Proxy                                            *
import platform
import subprocess
import sys


class Ping:
    """Servicio real de ping. Solo permite IPs que comienzan con '192.'."""

    INTENTOS = 10

    def _comando(self, destino):
        bandera = "-n" if platform.system().lower().startswith("win") else "-c"
        return ["ping", bandera, str(self.INTENTOS), destino]

    def _ejecutar(self, destino):
        try:
            res = subprocess.run(
                self._comando(destino),
                capture_output=True,
                text=True,
                timeout=30,
            )
            salida = res.stdout.strip().splitlines()
            for linea in salida[:6]:
                print(linea)
            print(f"  ... ({self.INTENTOS} intentos enviados a {destino})")
            return res.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError) as exc:
            print(f"[Ping] No se pudo ejecutar el ping real: {exc}")
            return False

    def execute(self, direccion):
        """Solo acepta direcciones que empiecen con '192.'."""
        if not direccion.startswith("192."):
            raise ValueError("Ping.execute solo admite direcciones que comienzan con '192.'")
        print(f"[Ping] execute -> {direccion}")
        return self._ejecutar(direccion)

    def executefree(self, direccion):
        """Variante sin validacion de prefijo de direccion."""
        print(f"[Ping] executefree -> {direccion}")
        return self._ejecutar(direccion)


class PingProxy:
    """Proxy: intercepta execute() y desvia si la IP es la 'gateway' especial."""

    IP_ESPECIAL = "192.168.0.254"
    DESTINO_ALTERNATIVO = "www.google.com"

    def __init__(self):
        self._real = Ping()

    def execute(self, direccion):
        if direccion == self.IP_ESPECIAL:
            print(f"[PingProxy] {direccion} es la IP especial; redirijo a {self.DESTINO_ALTERNATIVO}")
            return self._real.executefree(self.DESTINO_ALTERNATIVO)
        print(f"[PingProxy] delego en Ping.execute({direccion})")
        return self._real.execute(direccion)


def _demo():
    proxy = PingProxy()
    print("--- Caso 1: IP especial 192.168.0.254 (debe redirigir a google) ---")
    proxy.execute("192.168.0.254")
    print()
    print("--- Caso 2: IP comun 192.168.0.1 (delega en Ping.execute) ---")
    proxy.execute("192.168.0.1")
    print()
    print("--- Caso 3: IP no permitida 10.0.0.1 (Ping.execute la rechaza) ---")
    try:
        proxy.execute("10.0.0.1")
    except ValueError as err:
        print(f"Excepcion esperada: {err}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        PingProxy().execute(sys.argv[1])
    else:
        _demo()
