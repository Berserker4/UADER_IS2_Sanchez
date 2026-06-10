# TP8
"""
Sistema de pagos automatizado con re-ingenieria (TP8).

Patrones:
  - Command : ComandoPago encapsula cada solicitud de pago
  - Iterator: IteradorPagos recorre el historial cronologico

Integra GetJasonSingleton para resolver token -> clave API desde sitedata.json.
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime

from reader import ErrorPrograma, GetJasonSingleton


@dataclass
class RegistroPago:
    """Resultado de un pago ejecutado."""

    numero_pedido: str
    token: str
    monto: float
    clave_api: str
    fecha: datetime


class SelectorCuenta:
    """
    Componente de re-ingenieria: selecciona cuenta y resuelve clave del token.

    Usa el Singleton getJason para obtener la clave API asociada al banco.
    """

    def __init__(self, archivo_json):
        self._lector = GetJasonSingleton(archivo_json)

    def clave_para(self, token):
        """Devuelve la clave API del token indicado en sitedata.json."""
        return self._lector.obtener(token)

    def elegir_cuenta(self, cuentas, monto, turno):
        """
        Selecciona cuenta alternada con saldo suficiente.

        Intenta primero la cuenta del turno actual; si no alcanza, prueba la otra.
        """
        indices = [turno, 1 - turno]
        for indice in indices:
            cuenta = cuentas[indice]
            if cuenta.tiene_saldo(monto):
                return cuenta
        return None


class Cuenta:
    """Cuenta bancaria asociada a un token."""

    def __init__(self, token, saldo_inicial):
        self.token = token
        self.saldo = saldo_inicial

    def tiene_saldo(self, monto):
        return self.saldo >= monto

    def debitar(self, monto):
        if not self.tiene_saldo(monto):
            raise ErrorPrograma(
                f"Saldo insuficiente en {self.token}: ${self.saldo:.2f}"
            )
        self.saldo -= monto


class Comando(ABC):
    """Interfaz del patron Command."""

    @abstractmethod
    def ejecutar(self):
        """Ejecuta la operacion encapsulada."""


class ComandoPago(Comando):
    """Comando concreto: solicitud de pago (numero de pedido, monto)."""

    def __init__(self, numero_pedido, monto, sistema):
        self.numero_pedido = numero_pedido
        self.monto = monto
        self._sistema = sistema

    def ejecutar(self):
        return self._sistema.procesar_pago(self.numero_pedido, self.monto)


class IteradorPagos:
    """Iterator: recorre pagos en orden cronologico de registro."""

    def __init__(self, historial):
        self._historial = historial
        self._posicion = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._posicion >= len(self._historial):
            raise StopIteration
        registro = self._historial[self._posicion]
        self._posicion += 1
        return registro


class SistemaPagos:
    """
    Invocador del patron Command.

    Controla dos cuentas (token1: $1000, token2: $2000) y enruta pagos
    de $500 alternando entre cuentas con saldo suficiente.
    """

    MONTO_DEFAULT = 500.0

    def __init__(self, archivo_json):
        self._selector = SelectorCuenta(archivo_json)
        self._cuentas = [
            Cuenta('token1', 1000.0),
            Cuenta('token2', 2000.0),
        ]
        self._historial = []
        self._turno = 0

    def procesar_pago(self, numero_pedido, monto=None):
        monto = self.MONTO_DEFAULT if monto is None else monto
        cuenta = self._selector.elegir_cuenta(self._cuentas, monto, self._turno)
        if cuenta is None:
            raise ErrorPrograma(
                f"Pedido {numero_pedido}: ninguna cuenta tiene saldo para ${monto:.2f}"
            )

        clave = self._selector.clave_para(cuenta.token)
        cuenta.debitar(monto)
        registro = RegistroPago(
            numero_pedido=numero_pedido,
            token=cuenta.token,
            monto=monto,
            clave_api=clave,
            fecha=datetime.now(),
        )
        self._historial.append(registro)
        self._turno = 1 - self._turno
        return registro

    def ejecutar_comando(self, comando):
        """Ejecuta un comando del patron Command."""
        return comando.ejecutar()

    def listar_pagos(self):
        """Muestra todos los pagos realizados en orden cronologico."""
        if not self._historial:
            print('No hay pagos registrados.')
            return
        print('--- Listado de pagos (orden cronologico) ---')
        for pago in IteradorPagos(self._historial):
            print(
                f"  Pedido {pago.numero_pedido} | token={pago.token} | "
                f"monto=${pago.monto:.2f} | clave={pago.clave_api}"
            )

    def saldos(self):
        """Devuelve saldos actuales por token."""
        return {cuenta.token: cuenta.saldo for cuenta in self._cuentas}

    def total_pagos(self):
        """Cantidad de pagos registrados en el historial."""
        return len(self._historial)


def _demo():
    from pathlib import Path

    archivo = str(Path(__file__).resolve().parent / 'sitedata.json')
    sistema = SistemaPagos(archivo)

    pedidos = ['P001', 'P002', 'P003', 'P004', 'P005', 'P006']

    print('=== Sistema de pagos automatizado (TP8) ===\n')
    for numero in pedidos:
        comando = ComandoPago(numero, SistemaPagos.MONTO_DEFAULT, sistema)
        resultado = sistema.ejecutar_comando(comando)
        print(
            f"Pedido {resultado.numero_pedido} | token={resultado.token} | "
            f"monto=${resultado.monto:.2f}"
        )

    print()
    sistema.listar_pagos()
    print('\n--- Saldos finales ---')
    for token, saldo in sistema.saldos().items():
        print(f"  {token}: ${saldo:.2f}")


if __name__ == '__main__':
    _demo()
