from PyQt5.QtCore import QObject, QTimer, pyqtSignal
from random import randint
import parametros as p


class Meteorito(QObject):
    identificador = 0

    def __init__(self, x: int, y: int, senal_fin_meteorito: pyqtSignal,
                 senal_mover: pyqtSignal) -> None:

        super().__init__()
        self.id = Meteorito.identificador
        Meteorito.identificador += 1
        self.x = x
        self.y = y
        self.senal_mover = senal_mover
        self.senal_fin_meteorito = senal_fin_meteorito
        self._destruido = False
        self._distancia_a_recorrer = randint(
            p.DISTANCIA_MINIMA, p.DISTANCIA_MAXIMA)

        # COMPLETAR
        # Debo crear un QTimer para moverme
        self.timer_movimiento = QTimer(self)
        # Cada p.TIEMPO_CAIDA_METEORO se debe llamar a la función
        self.timer_movimiento.setInterval(p.TIEMPO_CAIDA_METEORO)
        # mover
        self.timer_movimiento.timeout.connect(self.mover)

    def mover(self) -> None:
        # COMPLETAR

        # 1. Aumento mi posición Y en self._distancia_a_recorrer
        # 2. Emito la señal para mover mi label
        # 3. Si mi posición es >= a p.POSICION_Y implica que llegué al suelo
        #    Debo emitir una señal para hacer daño y parar el timer.
        self.y += self._distancia_a_recorrer
        self.senal_mover.emit(self.id, self.x, self.y)
        if self.y >= p.POSICION_Y:
            self.senal_fin_meteorito.emit(self.id, True)
            self.timer_movimiento.stop()
        pass

    @property
    def destruido(self) -> bool:
        return self._destruido

    @destruido.setter
    def destruido(self, new_value: bool) -> None:
        # COMPLETAR
        # Seteo al atributo.
        # Si el nuevo valor es verdadero, emit la señal para que desaparezca
        # el meteorito sin hacer daño. Luego detengo el timer.
        if new_value:
            self.destruido = new_value
            self.senal_fin_meteorito.emit(self.id, False)
            self.timer_movimiento.stop()
        pass

    @property
    def centro_x(self) -> int:
        # Indica el centro del meteorito en eje X
        return self.x + 15

    @property
    def centro_y(self) -> int:
        # Indica el centro del meteorito en eje Y
        return self.y + 192


class Ciudad:
    def __init__(self, nombre: str, senal_problacion: pyqtSignal) -> None:
        self.nombre = nombre
        self._poblacion = 0
        self._destruidos = 0
        self.senal_problacion = senal_problacion

    @property
    def poblacion(self) -> int:
        return self._poblacion

    @poblacion.setter
    def poblacion(self, new_value: int) -> None:
        self._poblacion = new_value
        # COMPLETAR
        # Emitir señal según corresponda
        self._poblacion = new_value
        if self.poblacion <= 0:
            self.poblacion.emit(
                f'{self.nombre} ha perdido todos sus ciudaddanos')
        else:
            self.senal_problacion.emit(f'{self.poblacion}')
            # Avisar la cantidad de población
            pass


class Juego(QObject):
    senal_empezar_juego = pyqtSignal()
    # COMPLETAR
    # Crear señales que faltan
    # 1. Envía el ID del meteorito, la posición X e Y.
    senal_mover_meteorito = pyqtSignal(int, int, int)

    # 2. Envía el ID del meteorito, la posición X e Y.
    senal_aparecer_meteorito = pyqtSignal(int, int, int)

    # 3. Envía el ID del meteorito
    senal_remover_meteorito = pyqtSignal(int)

    # 4. Envía el ID del meteorito y un bool si hace daño o no
    senal_fin_meteorito = pyqtSignal(int, bool)

    # 5. Envía un texto para actulizar el label del frontend
    senal_actualizar_poblacion = pyqtSignal(str)

    def __init__(self) -> None:
        super().__init__()

        self.ciudad = Ciudad("DCCity", self.senal_actualizar_poblacion)
        self.meteoritos = []
        self.senal_fin_meteorito.connect(self.choque_meteorito)
        # COMPLETAR
        # Debo crear un QTimer para aparecer meteoritos
        self.timer_meteoritos = QTimer(self)
        self.timer_meteoritos.setInterval(p.DIFICULTAD["Facil"])
        self.timer_meteoritos.timeout.connect(self.caer_meteorito)
        # Cada p.DIFICULTAD["Facil"] se debe llamar a la función
        # caer_meteorito

    def iniciar_juego(self) -> None:
        self.ciudad._destruidos = 0
        self.ciudad.poblacion = p.POBLACION_MAXIMA
        # COMPLETAR
        self.senal_empezar_juego.emit()
        self.timer_meteoritos.start()
        # Avisar al juego que debe empezar y darle start a nuestro QTimer

    def caer_meteorito(self) -> None:
        meteorito = Meteorito(
            x=randint(50, 750),
            y=-200,
            senal_fin_meteorito=self.senal_fin_meteorito,
            senal_mover=self.senal_mover_meteorito
        )
        self.meteoritos.append(meteorito)
        # COMPLETAR
        self.senal_aparecer_meteorito.emit(
            meteorito.id, meteorito.x, meteorito.y)
        meteorito.timer_movimiento.start()
        # 1. Avisar que debe aparecer un meteorito
        # 2. Comenzar el movimiento del meteorito

    def choque_meteorito(self, id_meteorito: int, daño: bool) -> None:
        # COMPLETAR
        # 1. Eliminar visualmente el meteorito

        # 2. En caso de haber daño, reducir la población
        # 3. Si la población es <= 0, dejar de crear meteoritos
        pass

    def click_pantalla(self, x: int, y: int) -> None:
        for meteorito in self.meteoritos:
            if not meteorito.destruido:  # Solo verificar meteoritos sin destruir
                if self.chequear_colision(x, y, meteorito):
                    # Si el click es válido, se destruye el meteorito
                    meteorito.destruido = True
                    return

    def chequear_colision(self, x: int, y: int, meteorito: Meteorito) -> bool:
        distancia = ((x - meteorito.centro_x)**2 +
                     (y - meteorito.centro_y)**2)**(1/2)
        if distancia > 10:  # Lejos del centro del meteorio
            return False
        return True
