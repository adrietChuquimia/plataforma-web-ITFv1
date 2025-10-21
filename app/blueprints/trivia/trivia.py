from flask import Blueprint, render_template, session, request
import json, random, time, unicodedata
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

trivia_bp = Blueprint("trivia", __name__, template_folder="../templates")

# BASE DE CONOCIMIENTO
with open("conocimiento.json", "r", encoding="utf-8") as f:
    PIEZAS = json.load(f)

def normalizar(texto):
    """Normaliza texto para comparación (elimina acentos y convierte a minúsculas)"""
    nfkd = unicodedata.normalize('NFKD', texto)
    return "".join([c for c in nfkd if not unicodedata.combining(c)]).lower().strip()

# MOTOR DE INFERENCIA DIFUSO 

# Variables de entrada
tiempo_respuesta = ctrl.Antecedent(np.arange(0, 31, 1), 'tiempo_respuesta')
aciertos = ctrl.Antecedent(np.arange(0, 11, 1), 'aciertos')
racha_actual = ctrl.Antecedent(np.arange(0, 11, 1), 'racha_actual')
errores_consec = ctrl.Antecedent(np.arange(0, 6, 1), 'errores_consec')
precision = ctrl.Antecedent(np.arange(0, 101, 1), 'precision') 

# Variables de salida
dificultad = ctrl.Consequent(np.arange(0, 11, 1), 'dificultad')
pistas_nivel = ctrl.Consequent(np.arange(0, 4, 1), 'pistas_nivel')
motivacion = ctrl.Consequent(np.arange(0, 11, 1), 'motivacion')
tiempo_otorgado = ctrl.Consequent(np.arange(15, 46, 1), 'tiempo_otorgado') 

# Funciones de membresía para TIEMPO (a 30s)
tiempo_respuesta['muy_rapido'] = fuzz.trimf(tiempo_respuesta.universe, [0, 0, 5])
tiempo_respuesta['rapido'] = fuzz.trimf(tiempo_respuesta.universe, [3, 7, 12])
tiempo_respuesta['medio'] = fuzz.trimf(tiempo_respuesta.universe, [10, 15, 20])
tiempo_respuesta['lento'] = fuzz.trimf(tiempo_respuesta.universe, [18, 25, 30])
tiempo_respuesta['muy_lento'] = fuzz.trimf(tiempo_respuesta.universe, [25, 30, 30])

# Funciones de membresía para ACIERTOS (últimas 10 preguntas)
aciertos['ninguno'] = fuzz.trimf(aciertos.universe, [0, 0, 1])
aciertos['pocos'] = fuzz.trimf(aciertos.universe, [1, 3, 4])
aciertos['medios'] = fuzz.trimf(aciertos.universe, [3, 5, 6])
aciertos['altos'] = fuzz.trimf(aciertos.universe, [5, 7, 9])
aciertos['muy_altos'] = fuzz.trimf(aciertos.universe, [8, 10, 10])

# Funciones de membresía para RACHA
racha_actual['ninguna'] = fuzz.trimf(racha_actual.universe, [0, 0, 1])
racha_actual['corta'] = fuzz.trimf(racha_actual.universe, [1, 2, 3])
racha_actual['buena'] = fuzz.trimf(racha_actual.universe, [3, 5, 7])
racha_actual['excelente'] = fuzz.trimf(racha_actual.universe, [6, 10, 10])

# Funciones de membresía para ERRORES CONSECUTIVOS
errores_consec['ninguno'] = fuzz.trimf(errores_consec.universe, [0, 0, 0])
errores_consec['pocos'] = fuzz.trimf(errores_consec.universe, [1, 2, 3])
errores_consec['muchos'] = fuzz.trimf(errores_consec.universe, [3, 5, 5])

# Funciones de membresía para PRECISIÓN (%)
precision['muy_baja'] = fuzz.trimf(precision.universe, [0, 0, 30])
precision['baja'] = fuzz.trimf(precision.universe, [20, 40, 50])
precision['media'] = fuzz.trimf(precision.universe, [40, 60, 70])
precision['alta'] = fuzz.trimf(precision.universe, [60, 80, 90])
precision['muy_alta'] = fuzz.trimf(precision.universe, [85, 100, 100])

# Funciones de membresía para DIFICULTAD (salida)
dificultad['muy_facil'] = fuzz.trimf(dificultad.universe, [0, 0, 2])
dificultad['facil'] = fuzz.trimf(dificultad.universe, [1, 3, 5])
dificultad['medio'] = fuzz.trimf(dificultad.universe, [4, 5, 6])
dificultad['dificil'] = fuzz.trimf(dificultad.universe, [5, 7, 9])
dificultad['muy_dificil'] = fuzz.trimf(dificultad.universe, [8, 10, 10])

# Funciones de membresía para NIVEL DE PISTAS (salida)
pistas_nivel['pocas'] = fuzz.trimf(pistas_nivel.universe, [0, 1, 2])
pistas_nivel['algunas'] = fuzz.trimf(pistas_nivel.universe, [1, 2, 3])
pistas_nivel['muchas'] = fuzz.trimf(pistas_nivel.universe, [2, 3, 3])

# Funciones de membresía para MOTIVACIÓN (salida)
motivacion['refuerzo_positivo'] = fuzz.trimf(motivacion.universe, [0, 0, 3])
motivacion['animo'] = fuzz.trimf(motivacion.universe, [2, 5, 7])
motivacion['felicitacion'] = fuzz.trimf(motivacion.universe, [7, 10, 10])

# NUEVO: Funciones de membresía para TIEMPO OTORGADO (salida)
tiempo_otorgado['corto'] = fuzz.trimf(tiempo_otorgado.universe, [10, 15, 25])
tiempo_otorgado['medio'] = fuzz.trimf(tiempo_otorgado.universe, [20, 30, 35])
tiempo_otorgado['largo'] = fuzz.trimf(tiempo_otorgado.universe, [30, 45, 45])


# REGLAS DE PRIORIDAD MÁXIMA PARA USUARIOS NUEVOS (deben ir PRIMERO)
regla_d0_nuevo = ctrl.Rule(aciertos['ninguno'] & racha_actual['ninguna'], dificultad['muy_facil'])
regla_p0_nuevo = ctrl.Rule(aciertos['ninguno'] & racha_actual['ninguna'], pistas_nivel['muchas'])
regla_m0_nuevo = ctrl.Rule(aciertos['ninguno'] & racha_actual['ninguna'], motivacion['animo'])
regla_t0_nuevo = ctrl.Rule(aciertos['ninguno'] & racha_actual['ninguna'], tiempo_otorgado['largo'])

# REGLAS DE DIFICULTAD 
regla_d1 = ctrl.Rule(tiempo_respuesta['muy_lento'] & precision['muy_baja'], dificultad['muy_facil'])
regla_d2 = ctrl.Rule(aciertos['ninguno'] & errores_consec['muchos'], dificultad['muy_facil'])
regla_d3 = ctrl.Rule(precision['muy_baja'] & racha_actual['ninguna'], dificultad['muy_facil'])
regla_d4 = ctrl.Rule(errores_consec['muchos'] & tiempo_respuesta['lento'], dificultad['muy_facil'])
regla_d5 = ctrl.Rule(tiempo_respuesta['lento'] & aciertos['pocos'], dificultad['facil'])
regla_d6 = ctrl.Rule(precision['baja'] & racha_actual['ninguna'], dificultad['facil'])
regla_d7 = ctrl.Rule(aciertos['pocos'] & errores_consec['muchos'], dificultad['facil'])
regla_d8 = ctrl.Rule(tiempo_respuesta['muy_lento'] & precision['media'], dificultad['facil'])
regla_d9 = ctrl.Rule(racha_actual['corta'] & precision['baja'], dificultad['facil'])
regla_d10 = ctrl.Rule(tiempo_respuesta['medio'] & aciertos['medios'], dificultad['medio'])
regla_d11 = ctrl.Rule(precision['media'] & racha_actual['corta'], dificultad['medio'])
regla_d12 = ctrl.Rule(aciertos['medios'] & errores_consec['pocos'], dificultad['medio'])
regla_d13 = ctrl.Rule(tiempo_respuesta['lento'] & precision['alta'], dificultad['medio'])
regla_d14 = ctrl.Rule(racha_actual['buena'] & errores_consec['muchos'], dificultad['medio'])
regla_d15 = ctrl.Rule(tiempo_respuesta['rapido'] & precision['baja'], dificultad['medio'])
regla_d16 = ctrl.Rule(tiempo_respuesta['rapido'] & precision['alta'], dificultad['dificil'])
regla_d17 = ctrl.Rule(aciertos['altos'] & racha_actual['buena'], dificultad['dificil'])
regla_d18 = ctrl.Rule(precision['muy_alta'] & errores_consec['ninguno'] & aciertos['altos'], dificultad['dificil'])
regla_d19 = ctrl.Rule(racha_actual['excelente'] & aciertos['altos'], dificultad['dificil'])
regla_d20 = ctrl.Rule(tiempo_respuesta['medio'] & precision['muy_alta'], dificultad['dificil'])
regla_d21 = ctrl.Rule(tiempo_respuesta['muy_rapido'] & precision['muy_alta'], dificultad['muy_dificil'])
regla_d22 = ctrl.Rule(aciertos['muy_altos'] & racha_actual['excelente'], dificultad['muy_dificil'])
regla_d23 = ctrl.Rule(precision['muy_alta'] & racha_actual['excelente'], dificultad['muy_dificil'])
regla_d24 = ctrl.Rule(tiempo_respuesta['muy_rapido'] & errores_consec['ninguno'] & aciertos['muy_altos'], dificultad['muy_dificil'])
regla_d25 = ctrl.Rule(aciertos['muy_altos'] & precision['alta'] & tiempo_respuesta['rapido'], dificultad['muy_dificil'])

# REGLAS DE PISTAS
regla_p1 = ctrl.Rule(tiempo_respuesta['muy_lento'] & errores_consec['muchos'], pistas_nivel['muchas'])
regla_p2 = ctrl.Rule(precision['muy_baja'] & aciertos['ninguno'], pistas_nivel['muchas'])
regla_p3 = ctrl.Rule(aciertos['pocos'] & racha_actual['ninguna'], pistas_nivel['muchas'])
regla_p4 = ctrl.Rule(errores_consec['muchos'] & precision['baja'], pistas_nivel['muchas'])
regla_p5 = ctrl.Rule(tiempo_respuesta['lento'] & precision['muy_baja'], pistas_nivel['muchas'])
regla_p6 = ctrl.Rule(racha_actual['ninguna'] & errores_consec['muchos'], pistas_nivel['muchas'])
regla_p7 = ctrl.Rule(aciertos['ninguno'] & tiempo_respuesta['medio'], pistas_nivel['muchas'])
regla_p8 = ctrl.Rule(tiempo_respuesta['medio'] & precision['media'], pistas_nivel['algunas'])
regla_p9 = ctrl.Rule(aciertos['medios'] & racha_actual['corta'], pistas_nivel['algunas'])
regla_p10 = ctrl.Rule(precision['media'] & errores_consec['pocos'], pistas_nivel['algunas'])
regla_p11 = ctrl.Rule(tiempo_respuesta['lento'] & aciertos['medios'], pistas_nivel['algunas'])
regla_p12 = ctrl.Rule(racha_actual['buena'] & errores_consec['muchos'], pistas_nivel['algunas'])
regla_p13 = ctrl.Rule(precision['baja'] & tiempo_respuesta['rapido'], pistas_nivel['algunas'])
regla_p14 = ctrl.Rule(aciertos['pocos'] & precision['alta'], pistas_nivel['algunas'])
regla_p15 = ctrl.Rule(tiempo_respuesta['medio'] & racha_actual['ninguna'], pistas_nivel['algunas'])
regla_p16 = ctrl.Rule(tiempo_respuesta['rapido'] & precision['alta'], pistas_nivel['pocas'])
regla_p17 = ctrl.Rule(aciertos['altos'] & racha_actual['buena'], pistas_nivel['pocas'])
regla_p18 = ctrl.Rule(precision['muy_alta'] & errores_consec['ninguno'] & aciertos['altos'], pistas_nivel['pocas'])
regla_p19 = ctrl.Rule(tiempo_respuesta['muy_rapido'] & aciertos['muy_altos'], pistas_nivel['pocas'])
regla_p20 = ctrl.Rule(racha_actual['excelente'] & precision['alta'], pistas_nivel['pocas'])
regla_p21 = ctrl.Rule(aciertos['altos'] & tiempo_respuesta['muy_rapido'], pistas_nivel['pocas'])
regla_p22 = ctrl.Rule(precision['muy_alta'] & racha_actual['buena'], pistas_nivel['pocas'])

# REGLAS DE MOTIVACIÓN (24 reglas optimizadas)
regla_m1 = ctrl.Rule(tiempo_respuesta['muy_lento'] & errores_consec['muchos'], motivacion['refuerzo_positivo'])
regla_m2 = ctrl.Rule(aciertos['ninguno'] & racha_actual['ninguna'], motivacion['refuerzo_positivo'])
regla_m3 = ctrl.Rule(precision['muy_baja'] & tiempo_respuesta['lento'], motivacion['refuerzo_positivo'])
regla_m4 = ctrl.Rule(errores_consec['muchos'] & precision['baja'], motivacion['refuerzo_positivo'])
regla_m5 = ctrl.Rule(aciertos['pocos'] & racha_actual['ninguna'], motivacion['refuerzo_positivo'])
regla_m6 = ctrl.Rule(precision['muy_baja'] & errores_consec['pocos'], motivacion['refuerzo_positivo'])
regla_m7 = ctrl.Rule(tiempo_respuesta['lento'] & aciertos['ninguno'], motivacion['refuerzo_positivo'])
regla_m8 = ctrl.Rule(racha_actual['corta'] & errores_consec['muchos'], motivacion['refuerzo_positivo'])
regla_m9 = ctrl.Rule(tiempo_respuesta['medio'] & precision['media'], motivacion['animo'])
regla_m10 = ctrl.Rule(aciertos['medios'] & racha_actual['corta'], motivacion['animo'])
regla_m11 = ctrl.Rule(precision['media'] & errores_consec['pocos'], motivacion['animo'])
regla_m12 = ctrl.Rule(tiempo_respuesta['lento'] & precision['alta'], motivacion['animo'])
regla_m13 = ctrl.Rule(aciertos['altos'] & errores_consec['muchos'], motivacion['animo'])
regla_m14 = ctrl.Rule(racha_actual['buena'] & precision['baja'], motivacion['animo'])
regla_m15 = ctrl.Rule(tiempo_respuesta['rapido'] & aciertos['pocos'], motivacion['animo'])
regla_m16 = ctrl.Rule(precision['alta'] & racha_actual['corta'], motivacion['animo'])
regla_m17 = ctrl.Rule(tiempo_respuesta['rapido'] & precision['alta'], motivacion['felicitacion'])
regla_m18 = ctrl.Rule(aciertos['altos'] & racha_actual['buena'], motivacion['felicitacion'])
regla_m19 = ctrl.Rule(precision['muy_alta'] & errores_consec['ninguno'] & aciertos['altos'], motivacion['felicitacion'])
regla_m20 = ctrl.Rule(tiempo_respuesta['muy_rapido'] & aciertos['muy_altos'], motivacion['felicitacion'])
regla_m21 = ctrl.Rule(racha_actual['excelente'] & precision['muy_alta'], motivacion['felicitacion'])
regla_m22 = ctrl.Rule(aciertos['muy_altos'] & errores_consec['ninguno'], motivacion['felicitacion'])
regla_m23 = ctrl.Rule(tiempo_respuesta['muy_rapido'] & racha_actual['excelente'], motivacion['felicitacion'])
regla_m24 = ctrl.Rule(precision['muy_alta'] & tiempo_respuesta['rapido'] & racha_actual['buena'], motivacion['felicitacion'])

# Tiempo_otorgado 
regla_t1 = ctrl.Rule(precision['muy_alta'] & tiempo_respuesta['muy_rapido'], tiempo_otorgado['corto'])
regla_t2 = ctrl.Rule(aciertos['muy_altos'] & errores_consec['ninguno'], tiempo_otorgado['corto'])
regla_t3 = ctrl.Rule(racha_actual['excelente'] & precision['alta'], tiempo_otorgado['corto'])
regla_t4 = ctrl.Rule(precision['alta'] & tiempo_respuesta['rapido'] & aciertos['altos'], tiempo_otorgado['corto'])
regla_t5 = ctrl.Rule(aciertos['altos'] & racha_actual['buena'] & errores_consec['ninguno'], tiempo_otorgado['corto'])
regla_t6 = ctrl.Rule(tiempo_respuesta['muy_rapido'] & racha_actual['excelente'], tiempo_otorgado['corto'])
regla_t7 = ctrl.Rule(precision['media'] & aciertos['medios'], tiempo_otorgado['medio'])
regla_t8 = ctrl.Rule(tiempo_respuesta['medio'] & precision['alta'], tiempo_otorgado['medio'])
regla_t9 = ctrl.Rule(aciertos['altos'] & errores_consec['pocos'], tiempo_otorgado['medio'])
regla_t10 = ctrl.Rule(racha_actual['corta'] & precision['media'], tiempo_otorgado['medio'])
regla_t11 = ctrl.Rule(tiempo_respuesta['rapido'] & aciertos['medios'], tiempo_otorgado['medio'])
regla_t12 = ctrl.Rule(precision['alta'] & racha_actual['corta'], tiempo_otorgado['medio'])
regla_t13 = ctrl.Rule(aciertos['medios'] & tiempo_respuesta['medio'] & errores_consec['pocos'], tiempo_otorgado['medio'])
regla_t14 = ctrl.Rule(tiempo_respuesta['muy_lento'] & errores_consec['muchos'], tiempo_otorgado['largo'])
regla_t15 = ctrl.Rule(precision['muy_baja'] & aciertos['pocos'], tiempo_otorgado['largo'])
regla_t16 = ctrl.Rule(errores_consec['muchos'] & racha_actual['ninguna'], tiempo_otorgado['largo'])
regla_t17 = ctrl.Rule(precision['baja'] & tiempo_respuesta['lento'], tiempo_otorgado['largo'])
regla_t18 = ctrl.Rule(aciertos['ninguno'] & errores_consec['muchos'], tiempo_otorgado['largo'])
todas_reglas = [
    regla_d0_nuevo, regla_p0_nuevo, regla_m0_nuevo, regla_t0_nuevo,
    # Dificultad
    regla_d1, regla_d2, regla_d3, regla_d4, regla_d5, regla_d6, regla_d7, regla_d8, regla_d9, regla_d10, regla_d11, regla_d12, regla_d13, regla_d14, regla_d15,
    regla_d16, regla_d17, regla_d18, regla_d19, regla_d20, regla_d21, regla_d22, regla_d23, regla_d24, regla_d25,
    # Pistas
    regla_p1, regla_p2, regla_p3, regla_p4, regla_p5, regla_p6, regla_p7, regla_p8, regla_p9, regla_p10, regla_p11, regla_p12, regla_p13, regla_p14, regla_p15,
    regla_p16, regla_p17, regla_p18, regla_p19, regla_p20, regla_p21, regla_p22, 
    # Motivación
    regla_m1, regla_m2, regla_m3, regla_m4, regla_m5, regla_m6, regla_m7, regla_m8, regla_m9, regla_m10, regla_m11, regla_m12, regla_m13, regla_m14, regla_m15, 
    regla_m16, regla_m17, regla_m18, regla_m19, regla_m20, regla_m21, regla_m22, regla_m23, regla_m24,
    # Tiempo
    regla_t1, regla_t2, regla_t3, regla_t4, regla_t5, regla_t6, regla_t7, regla_t8, regla_t9, regla_t10, regla_t11, regla_t12, regla_t13, regla_t14, regla_t15,
    regla_t16, regla_t17, regla_t18
]

tutor_ctrl = ctrl.ControlSystem(todas_reglas)

def evaluar_tutor(tiempo, aciertos_count, racha, errores, precision_percent):
    """Sistema difuso mejorado con entrada de precisión"""
    sim = ctrl.ControlSystemSimulation(tutor_ctrl)
    sim.input['tiempo_respuesta'] = min(30, max(0, tiempo))
    sim.input['aciertos'] = min(10, max(0, aciertos_count))
    sim.input['racha_actual'] = min(10, max(0, racha))
    sim.input['errores_consec'] = min(5, max(0, errores))
    sim.input['precision'] = min(100, max(0, precision_percent))
    
    try:
        sim.compute()
    except:
        return {
            'dificultad': 1, 
            'pistas': 3, 
            'motivacion': 5, 
            'tiempo_otorgado': 30,
            'precision': 0
        }
    
    return {
        'dificultad': sim.output.get('dificultad', 1),
        'pistas': sim.output.get('pistas_nivel', 3),
        'motivacion': sim.output.get('motivacion', 5),
        'tiempo_otorgado': int(sim.output.get('tiempo_otorgado', 30)),
        'precision': sim.output.get('precision', 0) 
    }

# MOTOR DE INFERENCIA

def regla_respuesta(respuesta, correcta, tiempo):
    """Evaluación mejorada con sistema de puntuación adaptativo"""
    if normalizar(respuesta) == normalizar(correcta):
        bonus = max(0, 10 - tiempo) * 0.05 if tiempo < 10 else 0
        puntos = 1 + bonus
        session["errores_consecutivos"] = 0
        
        if session.get("racha", 0) >= 3:
            puntos += 0.2
            mensaje = f"¡Correcto! +{puntos:.1f} pts (¡Racha activa!)"
        else:
            mensaje = f"¡Correcto! +{puntos:.1f} puntos"
        
        return {"acierto": True, "puntos": puntos, "vidas": 0, "mensaje": mensaje}
    else:
        session["errores_consecutivos"] = session.get("errores_consecutivos", 0) + 1
        errores = session["errores_consecutivos"]
        
        vidas_perdidas = -1
        if errores >= 4:
            vidas_perdidas = -2
            session["errores_consecutivos"] = 0
            mensaje = f"Incorrecto. -2 vidas por 4 errores seguidos. Era: {correcta}"
        elif errores >= 3:
            vidas_perdidas = -2
            mensaje = f"Incorrecto. -2 vidas totales. Era: {correcta}"
        else:
            mensaje = f"Incorrecto. Era: {correcta}"
        
        return {"acierto": False, "puntos": 0, "vidas": vidas_perdidas, "mensaje": mensaje}

def regla_subir_nivel(racha, nivel, puntos):
    """Sistema de progresión mejorado"""
    if nivel == 1 and racha >= 5:
        return 2, 0
    elif nivel == 2 and racha >= 8:
        return 3, 0
    elif nivel == 3 and racha >= 12:
        return 4, 0
    elif nivel == 4 and racha >= 16:
        return 5, 0
    
    return nivel, racha

def registrar_logros():
    """Sistema de logros ampliado"""
    logros = session.setdefault("logros", [])
    
    # Logros por puntos
    for pts, key in [(10, "10_puntos"), (25, "25_puntos"), (50, "50_puntos"), (100, "100_puntos")]:
        if session["puntos"] >= pts and key not in logros:
            logros.append(key)
    
    # Logros por nivel
    for niv, key in [(3, "nivel_3"), (4, "nivel_4"), (5, "nivel_5")]:
        if session["nivel"] >= niv and key not in logros:
            logros.append(key)
    
    # Logros por racha
    for r, key in [(5, "racha_5"), (10, "racha_10"), (15, "racha_15"), (20, "racha_20")]:
        if session.get("racha", 0) >= r and key not in logros:
            logros.append(key)
    #logro por dificultad
    for di, key in [(4,"Insignia_pasante"), (7,"Insignia_tallerista"), (10, "Insignia_mecánico")]:
        if session.get("dificultad",0) >= di and key not in logros:
            logros.append(key)
    # Logros especiales
    total_preguntas = len(session.get("historial_aciertos", []))
    if total_preguntas >= 5:
        tiempos = session.get("historial_tiempos", [])
        if tiempos and sum(tiempos[-5:]) / min(5, len(tiempos[-5:])) < 5:
            if "velocista" not in logros:
                logros.append("velocista")
    
    if len(session.get("historial_aciertos", [])) >= 10:
        if sum(session["historial_aciertos"][-10:]) == 10 and "perfeccion" not in logros:
            logros.append("perfeccion")
    
    # Logro de precisión
    if total_preguntas >= 10:
        precision = sum(session["historial_aciertos"]) / total_preguntas * 100
        if precision == 95 and "precision_95" not in logros:
            logros.append("precision_95")
    
    session["logros"] = logros

def generar_pregunta_adaptativa(evaluacion_tutor):
    """Genera preguntas adaptadas según evaluación difusa"""
    preguntas_anteriores = session.get("preguntas_anteriores", [])
    disponibles = [p for p in PIEZAS.items() if p[0] not in preguntas_anteriores[-5:]]
    
    if len(disponibles) < 3:
        preguntas_anteriores = []
        disponibles = list(PIEZAS.items())
    
    pieza, pistas = random.choice(disponibles)
    preguntas_anteriores.append(pieza)
    session["preguntas_anteriores"] = preguntas_anteriores[-10:]
    
    dif = evaluacion_tutor['dificultad']
    pistas_num = evaluacion_tutor['pistas']
    tiempo_limite = evaluacion_tutor.get('tiempo_otorgado')
    
    # Seleccionar pistas según nivel
    if pistas_num >= 2.5:  # Muchas pistas
        pista = " | ".join(pistas[:3]) if len(pistas) >= 3 else (pistas[0] if pistas else "")
    elif pistas_num >= 1.5:  # Algunas pistas
        pista = pistas[2] if pistas else ""
    elif pistas_num >= 0.5:  # Pocas pistas
        pista = random.choice(pistas[:1]) if pistas else ""
    
    nivel_visual = session["nivel"]
    opciones = []
    
    # Determinar modo de pregunta
    if nivel_visual in [1, 2]:  
        distractores = [p for p in PIEZAS.keys() if p != pieza]
        opciones = random.sample(distractores, min(2, len(distractores))) + [pieza]
        random.shuffle(opciones)
    elif nivel_visual == 4:  
        if dif < 5:
            distractores = [p for p in PIEZAS.keys() if p != pieza]
            opciones = random.sample(distractores, min(2, len(distractores))) + [pieza]
            random.shuffle(opciones)
    
    return {
        "pieza": pieza, 
        "pista": pista, 
        "opciones": opciones,
        "tiempo_limite": tiempo_limite
    }

def generar_mensaje_motivacional(tipo_motivacion):
    if tipo_motivacion < 3:
        mensajes = [
            "No te desanimes, el aprendizaje es progresivo.",
            "Cada intento te acerca más al dominio del tema.",
            "Tómate el tiempo necesario para analizar las pistas.",
            "El error es parte fundamental del aprendizaje."
        ]
    elif tipo_motivacion < 7:
        mensajes = [
            "Vas por buen camino, mantén la concentración.",
            "Tu desempeño está mejorando consistentemente.",
            "Excelente progreso, sigue así.",
            "Estás demostrando buen dominio del tema."
        ]
    else:
        mensajes = [
            "¡Rendimiento excepcional! Eres un experto.",
            "¡Impresionante precisión y velocidad!",
            "¡Dominio total del tema! Sigue así.",
            "¡Nivel profesional! Continúa esta racha."
        ]
    
    return random.choice(mensajes)

# INTERFAZ DE USUARIO

@trivia_bp.route("/trivia", methods=["GET", "POST"])
def trivia():
    # Inicialización de sesión
    if "nivel" not in session:
        session.update({
            "nivel": 1,
            "vidas": 5,
            "puntos": 0,
            "racha": 0,
            "errores_consecutivos": 0,
            "preguntas_anteriores": [],
            "logros": [],
            "start_time": time.time(),
            "historial_aciertos": [],
            "historial_tiempos": [],
            "ultimo_mensaje": None
        })

    if request.method == "POST":
        respuesta = request.form.get("respuesta", "")
        correcta = request.form.get("correcta", "")
        tiempo_transcurrido = time.time() - session["start_time"]
        
        # Evaluar respuesta
        resultado = regla_respuesta(respuesta, correcta, tiempo_transcurrido)
        session["puntos"] += resultado["puntos"]
        session["vidas"] += resultado["vidas"]
        
        # Actualizar historial
        session.setdefault("historial_aciertos", [])
        session.setdefault("historial_tiempos", [])
        
        session["historial_aciertos"].append(1 if resultado["acierto"] else 0)
        session["historial_tiempos"].append(tiempo_transcurrido)
        
        session["historial_aciertos"] = session["historial_aciertos"][-10:]
        session["historial_tiempos"] = session["historial_tiempos"][-10:]
        
        # Actualizar racha
        if resultado["acierto"]:
            session["racha"] += 1
        else:
            session["racha"] = 0
        
        # Evaluar progresión
        session["nivel"], session["racha"] = regla_subir_nivel(
            session["racha"], 
            session["nivel"],
            session["puntos"]
        )
        
        registrar_logros()
        
        # Calcular precisión
        total_preguntas = len(session["historial_aciertos"])
        precision_percent = (sum(session["historial_aciertos"]) / total_preguntas * 100) if total_preguntas > 0 else 50
        
        # EVALUACIÓN DIFUSA
        aciertos_count = sum(session["historial_aciertos"])
        evaluacion = evaluar_tutor(
            tiempo_transcurrido,
            aciertos_count,
            session["racha"],
            session["errores_consecutivos"],
            precision_percent
        )
        
        # Mensaje personalizado
        mensaje_motivacional = generar_mensaje_motivacional(evaluacion['motivacion'])
        resultado["mensaje"] += f" | {mensaje_motivacional}"
        
        dif = evaluacion['dificultad']
        if dif >= 0 and dif < 4:
            resultado["mensaje"] += " | CATEGORIA: PRINCIPIANTE [Apto para PASANTE de taller]"
        elif dif >= 4 and dif < 7:
            resultado["mensaje"] += " | CATEGORIA: INTERMEDIO [Apto para AYUDANTE de taller]"
        else:
            resultado["mensaje"] += " | CATEGORIA: EXPERTO [Apto para MECÁNICO/AUTOTRÓNICO]"
        
        session["ultimo_mensaje"] = resultado["mensaje"]
        
        if session["vidas"] <= 0:
            puntos_final = session["puntos"]
            nivel_final = session["nivel"]
            logros_finales = session.get("logros", [])
            session.clear()
            return render_template("gameover.html",
                                   puntos=puntos_final,
                                   nivel=nivel_final,
                                   logros=logros_finales,
                                   mensaje=resultado["mensaje"])
    
    # Generar nueva pregunta
    total_preguntas = len(session.get("historial_aciertos", [0]))
    precision_percent = (sum(session.get("historial_aciertos", [0])) / max(1, total_preguntas) * 100) if total_preguntas > 0 else 0
    aciertos_count = sum(session.get("historial_aciertos", [0]))
    tiempo_promedio = sum(session.get("historial_tiempos", [15])) / max(1, len(session.get("historial_tiempos", [1])))
    
    evaluacion = evaluar_tutor(
        tiempo_promedio,
        aciertos_count,
        session.get("racha", 0),
        session.get("errores_consecutivos", 0),
        precision_percent
    )
    
    pregunta = generar_pregunta_adaptativa(evaluacion)
    session["correcta"] = pregunta["pieza"]
    session["start_time"] = time.time()
    
    return render_template("trivia.html",
                           pregunta=pregunta,
                           nivel=session["nivel"],
                           vidas=session["vidas"],
                           puntos=session["puntos"],
                           logros=session.get("logros", []),
                           precision=precision_percent,
                           tiempo_limite=pregunta.get("tiempo_limite", 30)) 