# ---------------------------------------------------------------------------
# Puntaje y Hero Power (Star Power) al estilo del Guitar Hero clasico.
# No usa pygame: es solo la logica, asi se puede probar sola. GuitarHuergo.py
# se encarga de dibujarla y de avisarle a estas clases cuando se acierta o se
# falla una nota.
#
# Reglas (las del Guitar Hero clasico):
#   - Cada nota acertada vale 50 puntos x el multiplicador.
#   - Las notas largas (sustains) suman 25 puntos por tiempo (beat) que las mantengas presionadas,
#     tambien x el multiplicador (y x2 con el Hero Power). Soltarlas antes solo te hace perder lo que faltaba.
#   - El multiplicador sube de a 1 cada 10 notas seguidas: x1, x2, x3, x4 (tope).
#     Al fallar una nota la racha vuelve a 0.
#   - Algunas frases de notas son "Star": si acertas TODAS las notas de la frase
#     (sin fallar ninguna) la barra de Hero Power sube un 25%.
#   - Con la barra en 50% o mas se puede activar el Hero Power. Mientras esta
#     activo el multiplicador se DUPLICA (hasta x8) y la barra se va vaciando:
#     una barra llena dura 8 compases (32 tiempos). Si completas otra frase Star
#     mientras esta activo, la barra recupera 25% y dura mas.
# ---------------------------------------------------------------------------

PUNTOS_POR_NOTA = 50
PUNTOS_SUSTAIN_POR_TIEMPO = 25  # puntos por cada tiempo (beat) que se mantiene una nota larga
NOTAS_POR_NIVEL = 10            # cada cuantas notas seguidas sube el multiplicador
MULTIPLICADOR_MAX = 4

CARGA_POR_FRASE = 0.25          # cuanto llena la barra completar una frase Star
MINIMO_PARA_ACTIVAR = 0.5       # la barra tiene que estar al 50% para poder activar
TIEMPOS_BARRA_LLENA = 32        # una barra llena dura 8 compases de 4 tiempos


class Marcador:
    def __init__(self):
        self.puntaje = 0
        self.racha = 0
        self.mejor_racha = 0
        self.aciertos = 0
        self.fallos = 0
        self.puntos_sustain = 0
        self._resto = 0.0           # fraccion de punto que todavia no se sumo (los sustains suman de a poquito por frame)

    def multiplicador_base(self):                  # x1 a x4 segun la racha
        return min(1 + self.racha // NOTAS_POR_NIVEL, MULTIPLICADOR_MAX)

    def multiplicador(self, power_activo=False):   # el Hero Power duplica el multiplicador
        base = self.multiplicador_base()
        return base * 2 if power_activo else base

    def acierto(self, power_activo=False):         # devuelve los puntos que dio esta nota
        puntos = PUNTOS_POR_NOTA * self.multiplicador(power_activo)   # se calcula ANTES de sumar la nota a la racha
        self.puntaje += puntos
        self.racha += 1
        self.mejor_racha = max(self.mejor_racha, self.racha)
        self.aciertos += 1
        return puntos

    def sustain(self, tiempos, power_activo=False):
        # Suma los puntos de mantener una nota larga durante 'tiempos' tiempos (beats). No cambia la racha.
        # Devuelve los puntos enteros que se sumaron en esta llamada.
        total = self._resto + PUNTOS_SUSTAIN_POR_TIEMPO * tiempos * self.multiplicador(power_activo)
        enteros = int(total)
        self._resto = total - enteros
        self.puntaje += enteros
        self.puntos_sustain += enteros
        return enteros

    def fallo(self):
        self.racha = 0
        self.fallos += 1

    def precision(self):                           # porcentaje de notas acertadas (0 a 100)
        total = self.aciertos + self.fallos
        return 100.0 * self.aciertos / total if total else 0.0


class HeroPower:
    def __init__(self, notas_por_frase=None):
        # notas_por_frase: {id_de_frase: cantidad de notas que tiene esa frase}
        self.total = dict(notas_por_frase or {})
        self.aciertos = {i: 0 for i in self.total}
        self.perdidas = set()           # frases en las que se fallo alguna nota
        self.completadas = set()
        self.energia = 0.0              # 0.0 a 1.0
        self.activo = False

    def frase_perdida(self, frase):
        return frase in self.perdidas

    def nota_acertada(self, frase):
        # Devuelve True si con esta nota se completo la frase (y la barra subio)
        if frase is None or frase in self.perdidas or frase in self.completadas or frase not in self.total:
            return False
        self.aciertos[frase] += 1
        if self.aciertos[frase] >= self.total[frase]:
            self.completadas.add(frase)
            self.energia = min(1.0, self.energia + CARGA_POR_FRASE)
            return True
        return False

    def nota_fallada(self, frase):
        # Devuelve True si con este fallo se perdio la frase (las notas que quedan dejan de ser Star)
        if frase is None or frase in self.perdidas or frase in self.completadas:
            return False
        self.perdidas.add(frase)
        return True

    def puede_activar(self):
        return not self.activo and self.energia >= MINIMO_PARA_ACTIVAR

    def activar(self):
        if self.puede_activar():
            self.activo = True
            return True
        return False

    def actualizar(self, dt_ms, bpm):
        # Vacia la barra mientras esta activo: una barra llena dura TIEMPOS_BARRA_LLENA tiempos,
        # asi que el gasto depende de los BPM de la cancion en ese momento.
        if self.activo and bpm > 0:
            self.energia -= dt_ms * bpm / 60000.0 / TIEMPOS_BARRA_LLENA
            if self.energia <= 0:
                self.energia = 0.0
                self.activo = False