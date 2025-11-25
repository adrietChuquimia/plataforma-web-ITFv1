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


tiempo_respuesta = ctrl.Antecedent(np.arange(0, 45, 1), 'tiempo_respuesta')
aciertos = ctrl.Antecedent(np.arange(0, 11, 1), 'aciertos')
errores_consec = ctrl.Antecedent(np.arange(0, 6, 1), 'errores_consec')
precision = ctrl.Antecedent(np.arange(0, 101, 1), 'precision') 

nivel = ctrl.Consequent(np.arange(0, 11, 1), 'nivel')
pistas_dificultad = ctrl.Consequent(np.arange(0, 4, 1), 'pistas_nivel')
motivacion = ctrl.Consequent(np.arange(0, 11, 1), 'motivacion')
tiempo_otorgado = ctrl.Consequent(np.arange(10, 46, 1), 'tiempo_otorgado') 

tiempo_respuesta['muy_rapido'] = fuzz.trimf(tiempo_respuesta.universe, [0, 4, 7])
tiempo_respuesta['rapido'] = fuzz.trimf(tiempo_respuesta.universe, [5, 10, 20])
tiempo_respuesta['medio'] = fuzz.trimf(tiempo_respuesta.universe, [10, 15, 25])
tiempo_respuesta['lento'] = fuzz.trimf(tiempo_respuesta.universe, [20, 30, 40])
tiempo_respuesta['muy_lento'] = fuzz.trimf(tiempo_respuesta.universe, [30, 45, 45])

aciertos['ninguno'] = fuzz.trimf(aciertos.universe, [0, 0, 1])
aciertos['pocos'] = fuzz.trimf(aciertos.universe, [1, 2, 4])
aciertos['medios'] = fuzz.trimf(aciertos.universe, [2, 5, 6])
aciertos['altos'] = fuzz.trimf(aciertos.universe, [5, 7, 9])
aciertos['muy_altos'] = fuzz.trimf(aciertos.universe, [8, 10, 10])

errores_consec['ninguno'] = fuzz.trimf(errores_consec.universe, [0, 0, 1])
errores_consec['pocos'] = fuzz.trimf(errores_consec.universe, [1, 2, 4])
errores_consec['muchos'] = fuzz.trimf(errores_consec.universe, [3, 5, 5])

precision['muy_baja'] = fuzz.trimf(precision.universe, [0, 0, 30])
precision['baja'] = fuzz.trimf(precision.universe, [20, 40, 50])
precision['media'] = fuzz.trimf(precision.universe, [40, 60, 70])
precision['alta'] = fuzz.trimf(precision.universe, [60, 80, 90])
precision['muy_alta'] = fuzz.trimf(precision.universe, [85, 100, 100])

nivel['principiante'] = fuzz.trimf(nivel.universe, [0, 2, 5])
nivel['medio'] = fuzz.trimf(nivel.universe, [3, 5, 8])
nivel['experto'] = fuzz.trimf(nivel.universe, [7, 10, 10])

pistas_dificultad['muchas'] = fuzz.trimf(pistas_dificultad.universe, [0, 2, 5])
pistas_dificultad['algunas'] = fuzz.trimf(pistas_dificultad.universe, [3, 5, 9])
pistas_dificultad['pocas'] = fuzz.trimf(pistas_dificultad.universe, [8, 10, 10])

motivacion['positivo'] = fuzz.trimf(motivacion.universe, [0, 2, 4])
motivacion['animar'] = fuzz.trimf(motivacion.universe, [3, 5, 8])
motivacion['felicitar'] = fuzz.trimf(motivacion.universe, [7, 9, 10])

tiempo_otorgado['corto'] = fuzz.trimf(tiempo_otorgado.universe, [10, 15, 25])
tiempo_otorgado['medio'] = fuzz.trimf(tiempo_otorgado.universe, [20, 30, 35])
tiempo_otorgado['largo'] = fuzz.trimf(tiempo_otorgado.universe, [30, 45, 45])


regla_n1 = ctrl.Rule(tiempo_respuesta['muy_rapido'] & errores_consec['ninguno'] & precision['muy_baja'], nivel['principiante'] )
regla_n2 = ctrl.Rule(tiempo_respuesta['muy_rapido'] & errores_consec['ninguno'] & precision['baja'], nivel['principiante'])
regla_n3 = ctrl.Rule(tiempo_respuesta['muy_rapido'] & errores_consec['ninguno'] & precision['media'], nivel['medio'])
regla_n4 = ctrl.Rule(tiempo_respuesta['muy_rapido'] & errores_consec['ninguno'] & precision['alta'], nivel['medio'])
regla_n5 = ctrl.Rule(tiempo_respuesta['muy_rapido'] & errores_consec['ninguno'] & precision['muy_alta'], nivel['experto'])
regla_n6 = ctrl.Rule(tiempo_respuesta['muy_rapido'] & errores_consec['pocos'] & precision['muy_baja'], nivel['principiante'])
regla_n7 = ctrl.Rule(tiempo_respuesta['muy_rapido'] & errores_consec['pocos'] & precision['baja'], nivel['principiante'])
regla_n8 = ctrl.Rule(tiempo_respuesta['muy_rapido'] & errores_consec['pocos'] & precision['media'], nivel['principiante'])
regla_n9 = ctrl.Rule(tiempo_respuesta['muy_rapido'] & errores_consec['pocos'] & precision['alta'], nivel['medio'])
regla_n10 = ctrl.Rule(tiempo_respuesta['muy_rapido'] & errores_consec['pocos'] & precision['muy_alta'], nivel['medio'])
regla_n11 = ctrl.Rule(tiempo_respuesta['muy_rapido'] & errores_consec['muchos'] & precision['muy_baja'], nivel['principiante'])
regla_n12 = ctrl.Rule(tiempo_respuesta['muy_rapido'] & errores_consec['muchos'] & precision['baja'], nivel['principiante'])
regla_n13 = ctrl.Rule(tiempo_respuesta['muy_rapido'] & errores_consec['muchos'] & precision['media'], nivel['principiante'])
regla_n14 = ctrl.Rule(tiempo_respuesta['muy_rapido'] & errores_consec['muchos'] & precision['alta'], nivel['principiante'])
regla_n15 = ctrl.Rule(tiempo_respuesta['muy_rapido'] & errores_consec['muchos'] & precision['muy_alta'], nivel['medio'])
regla_n16 = ctrl.Rule(tiempo_respuesta['rapido'] & errores_consec['ninguno'] & precision['muy_baja'], nivel['principiante'])
regla_n17 = ctrl.Rule(tiempo_respuesta['rapido'] & errores_consec['ninguno'] & precision['baja'], nivel['principiante'])
regla_n18 = ctrl.Rule(tiempo_respuesta['rapido'] & errores_consec['ninguno'] & precision['media'], nivel['medio'])
regla_n19 = ctrl.Rule(tiempo_respuesta['rapido'] & errores_consec['ninguno'] & precision['alta'], nivel['medio'])
regla_n20 = ctrl.Rule(tiempo_respuesta['rapido'] & errores_consec['ninguno'] & precision['muy_alta'], nivel['experto'])
regla_n21 = ctrl.Rule(tiempo_respuesta['rapido'] & errores_consec['pocos'] & precision['muy_baja'], nivel['principiante'])
regla_n22 = ctrl.Rule(tiempo_respuesta['rapido'] & errores_consec['pocos'] & precision['baja'], nivel['principiante'])
regla_n23 = ctrl.Rule(tiempo_respuesta['rapido'] & errores_consec['pocos'] & precision['media'], nivel['principiante'])
regla_n24 = ctrl.Rule(tiempo_respuesta['rapido'] & errores_consec['pocos'] & precision['alta'], nivel['medio'])
regla_n25 = ctrl.Rule(tiempo_respuesta['rapido'] & errores_consec['pocos'] & precision['muy_alta'], nivel['medio'])
regla_n26 = ctrl.Rule(tiempo_respuesta['rapido'] & errores_consec['muchos'] & precision['muy_baja'], nivel['principiante'])
regla_n27 = ctrl.Rule(tiempo_respuesta['rapido'] & errores_consec['muchos'] & precision['baja'], nivel['principiante'])
regla_n28 = ctrl.Rule(tiempo_respuesta['rapido'] & errores_consec['muchos'] & precision['media'], nivel['principiante'])
regla_n29 = ctrl.Rule(tiempo_respuesta['rapido'] & errores_consec['muchos'] & precision['alta'], nivel['principiante'])
regla_n30 = ctrl.Rule(tiempo_respuesta['rapido'] & errores_consec['muchos'] & precision['muy_alta'], nivel['medio'])
regla_n30 = ctrl.Rule(tiempo_respuesta['medio'] & errores_consec['ninguno'] & precision['muy_baja'], nivel['principiante'])
regla_n31 = ctrl.Rule(tiempo_respuesta['medio'] & errores_consec['ninguno'] & precision['baja'], nivel['principiante'])
regla_n32 = ctrl.Rule(tiempo_respuesta['medio'] & errores_consec['ninguno'] & precision['media'], nivel['medio'])
regla_n33 = ctrl.Rule(tiempo_respuesta['medio'] & errores_consec['ninguno'] & precision['alta'], nivel['medio'])
regla_n34 = ctrl.Rule(tiempo_respuesta['medio'] & errores_consec['ninguno'] & precision['muy_alta'], nivel['experto'])
regla_n35 = ctrl.Rule(tiempo_respuesta['medio'] & errores_consec['pocos'] & precision['muy_baja'], nivel['principiante'])
regla_n36 = ctrl.Rule(tiempo_respuesta['medio'] & errores_consec['pocos'] & precision['baja'], nivel['principiante'])
regla_n37 = ctrl.Rule(tiempo_respuesta['medio'] & errores_consec['pocos'] & precision['media'], nivel['principiante'])
regla_n38 = ctrl.Rule(tiempo_respuesta['medio'] & errores_consec['pocos'] & precision['alta'], nivel['medio'])
regla_n39 = ctrl.Rule(tiempo_respuesta['medio'] & errores_consec['pocos'] & precision['muy_alta'], nivel['medio'])
regla_n40 = ctrl.Rule(tiempo_respuesta['medio'] & errores_consec['muchos'] & precision['muy_baja'], nivel['principiante'])
regla_n41 = ctrl.Rule(tiempo_respuesta['medio'] & errores_consec['muchos'] & precision['baja'], nivel['principiante'])
regla_n42 = ctrl.Rule(tiempo_respuesta['medio'] & errores_consec['muchos'] & precision['media'], nivel['principiante'])
regla_n43 = ctrl.Rule(tiempo_respuesta['medio'] & errores_consec['muchos'] & precision['alta'], nivel['principiante'])
regla_n44 = ctrl.Rule(tiempo_respuesta['medio'] & errores_consec['muchos'] & precision['muy_alta'], nivel['principiante'])
regla_n45 = ctrl.Rule(tiempo_respuesta['lento'] & errores_consec['ninguno'] & precision['muy_baja'], nivel['principiante'])
regla_n46 = ctrl.Rule(tiempo_respuesta['lento'] & errores_consec['ninguno'] & precision['baja'], nivel['principiante'])
regla_n47 = ctrl.Rule(tiempo_respuesta['lento'] & errores_consec['ninguno'] & precision['media'], nivel['principiante'])
regla_n48 = ctrl.Rule(tiempo_respuesta['lento'] & errores_consec['ninguno'] & precision['alta'], nivel['principiante'])
regla_n49 = ctrl.Rule(tiempo_respuesta['lento'] & errores_consec['ninguno'] & precision['muy_alta'], nivel['medio'])
regla_n50 = ctrl.Rule(tiempo_respuesta['lento'] & errores_consec['pocos'] & precision['muy_baja'], nivel['principiante'])
regla_n52 = ctrl.Rule(tiempo_respuesta['lento'] & errores_consec['pocos'] & precision['media'], nivel['principiante'])
regla_n53 = ctrl.Rule(tiempo_respuesta['lento'] & errores_consec['pocos'] & precision['alta'], nivel['principiante'])
regla_n54 = ctrl.Rule(tiempo_respuesta['lento'] & errores_consec['pocos'] & precision['muy_alta'], nivel['principiante'])
regla_n55 = ctrl.Rule(tiempo_respuesta['lento'] & errores_consec['muchos'] & precision['muy_baja'], nivel['principiante'])
regla_n56 = ctrl.Rule(tiempo_respuesta['lento'] & errores_consec['muchos'] & precision['baja'], nivel['principiante'])
regla_n57 = ctrl.Rule(tiempo_respuesta['lento'] & errores_consec['muchos'] & precision['media'], nivel['principiante'])
regla_n58 = ctrl.Rule(tiempo_respuesta['lento'] & errores_consec['muchos'] & precision['alta'], nivel['principiante'])
regla_n59 = ctrl.Rule(tiempo_respuesta['lento'] & errores_consec['muchos'] & precision['muy_alta'], nivel['principiante'])
regla_n51 = ctrl.Rule(tiempo_respuesta['lento'] & errores_consec['pocos'] & precision['baja'], nivel['principiante'])
regla_n60 = ctrl.Rule(tiempo_respuesta['muy_lento'] & errores_consec['ninguno'] & precision['muy_baja'], nivel['principiante'])
regla_n61 = ctrl.Rule(tiempo_respuesta['muy_lento'] & errores_consec['ninguno'] & precision['baja'], nivel['principiante'])
regla_n62 = ctrl.Rule(tiempo_respuesta['muy_lento'] & errores_consec['ninguno'] & precision['media'], nivel['principiante'])
regla_n63 = ctrl.Rule(tiempo_respuesta['muy_lento'] & errores_consec['ninguno'] & precision['alta'], nivel['principiante'])
regla_n64 = ctrl.Rule(tiempo_respuesta['muy_lento'] & errores_consec['ninguno'] & precision['muy_alta'], nivel['principiante'])
regla_n65 = ctrl.Rule(tiempo_respuesta['muy_lento'] & errores_consec['pocos'] & precision['muy_baja'], nivel['principiante'])
regla_n66 = ctrl.Rule(tiempo_respuesta['muy_lento'] & errores_consec['pocos'] & precision['baja'], nivel['principiante'])
regla_n67 = ctrl.Rule(tiempo_respuesta['muy_lento'] & errores_consec['pocos'] & precision['media'], nivel['principiante'])
regla_n68 = ctrl.Rule(tiempo_respuesta['muy_lento'] & errores_consec['pocos'] & precision['alta'], nivel['principiante'])
regla_n69 = ctrl.Rule(tiempo_respuesta['muy_lento'] & errores_consec['pocos'] & precision['muy_alta'], nivel['principiante'])
regla_n70 = ctrl.Rule(tiempo_respuesta['muy_lento'] & errores_consec['muchos'] & precision['muy_baja'], nivel['principiante'])
regla_n71 = ctrl.Rule(tiempo_respuesta['muy_lento'] & errores_consec['muchos'] & precision['baja'], nivel['principiante'])
regla_n72 = ctrl.Rule(tiempo_respuesta['muy_lento'] & errores_consec['muchos'] & precision['media'], nivel['principiante'])
regla_n73 = ctrl.Rule(tiempo_respuesta['muy_lento'] & errores_consec['muchos'] & precision['alta'], nivel['principiante'])
regla_n74 = ctrl.Rule(tiempo_respuesta['muy_lento'] & errores_consec['muchos'] & precision['muy_alta'], nivel['principiante'])

regla_m1 = ctrl.Rule(errores_consec['ninguno'] & precision['muy_baja'], motivacion['animar'])
regla_m2 = ctrl.Rule(errores_consec['ninguno'] & precision['baja'], motivacion['animar'])
regla_m3 = ctrl.Rule(errores_consec['ninguno'] & precision['media'], motivacion['animar'])
regla_m4 = ctrl.Rule(errores_consec['ninguno'] & precision['alta'], motivacion['felicitar'])
regla_m5 = ctrl.Rule(errores_consec['ninguno'] & precision['muy_alta'], motivacion['felicitar'])
regla_m6 = ctrl.Rule(errores_consec['pocos'] & precision['muy_baja'], motivacion['positivo'])
regla_m7 = ctrl.Rule(errores_consec['pocos'] & precision['baja'], motivacion['positivo'])
regla_m8 = ctrl.Rule(errores_consec['pocos'] & precision['media'], motivacion['animar'])
regla_m9 = ctrl.Rule(errores_consec['pocos'] & precision['alta'], motivacion['animar'])
regla_m10 = ctrl.Rule(errores_consec['pocos'] & precision['muy_alta'], motivacion['animar'])
regla_m11 = ctrl.Rule(errores_consec['muchos'] & precision['muy_baja'], motivacion['positivo'])
regla_m12 = ctrl.Rule(errores_consec['muchos'] & precision['baja'], motivacion['positivo'])
regla_m13 = ctrl.Rule(errores_consec['muchos'] & precision['media'], motivacion['positivo'])
regla_m14 = ctrl.Rule(errores_consec['muchos'] & precision['alta'], motivacion['positivo'])
regla_m15 = ctrl.Rule(errores_consec['muchos'] & precision['muy_alta'], motivacion['positivo'])

regla_p1 = ctrl.Rule(tiempo_respuesta['muy_rapido'] & errores_consec['ninguno'] & precision['muy_baja'], pistas_dificultad['muchas'] )
regla_p2 = ctrl.Rule(tiempo_respuesta['muy_rapido'] & errores_consec['ninguno'] & precision['baja'], pistas_dificultad['muchas'] )
regla_p3 = ctrl.Rule(tiempo_respuesta['muy_rapido'] & errores_consec['ninguno'] & precision['media'], pistas_dificultad['algunas'] )
regla_p4 = ctrl.Rule(tiempo_respuesta['muy_rapido'] & errores_consec['ninguno'] & precision['alta'], pistas_dificultad['algunas'] )
regla_p5 = ctrl.Rule(tiempo_respuesta['muy_rapido'] & errores_consec['ninguno'] & precision['muy_alta'], pistas_dificultad['pocas'] )
regla_p6 = ctrl.Rule(tiempo_respuesta['muy_rapido'] & errores_consec['pocos'] & precision['muy_baja'], pistas_dificultad['muchas'] )
regla_p7 = ctrl.Rule(tiempo_respuesta['muy_rapido'] & errores_consec['pocos'] & precision['baja'], pistas_dificultad['muchas'] )
regla_p8 = ctrl.Rule(tiempo_respuesta['muy_rapido'] & errores_consec['pocos'] & precision['media'], pistas_dificultad['muchas'] )
regla_p9 = ctrl.Rule(tiempo_respuesta['muy_rapido'] & errores_consec['pocos'] & precision['alta'], pistas_dificultad['algunas'] )
regla_p10 = ctrl.Rule(tiempo_respuesta['muy_rapido'] & errores_consec['pocos'] & precision['muy_alta'], pistas_dificultad['muchas'] )
regla_p11 = ctrl.Rule(tiempo_respuesta['muy_rapido'] & errores_consec['muchos'] & precision['muy_baja'], pistas_dificultad['muchas'] )
regla_p12 = ctrl.Rule(tiempo_respuesta['muy_rapido'] & errores_consec['muchos'] & precision['baja'], pistas_dificultad['muchas'] )
regla_p13 = ctrl.Rule(tiempo_respuesta['muy_rapido'] & errores_consec['muchos'] & precision['media'], pistas_dificultad['muchas'] )
regla_p14 = ctrl.Rule(tiempo_respuesta['muy_rapido'] & errores_consec['muchos'] & precision['alta'], pistas_dificultad['muchas'] )
regla_p15 = ctrl.Rule(tiempo_respuesta['muy_rapido'] & errores_consec['muchos'] & precision['muy_alta'], pistas_dificultad['algunas'] )
regla_p16 = ctrl.Rule(tiempo_respuesta['rapido'] & errores_consec['ninguno'] & precision['muy_baja'], pistas_dificultad['muchas'] )
regla_p17 = ctrl.Rule(tiempo_respuesta['rapido'] & errores_consec['ninguno'] & precision['baja'], pistas_dificultad['muchas'] )
regla_p18 = ctrl.Rule(tiempo_respuesta['rapido'] & errores_consec['ninguno'] & precision['media'], pistas_dificultad['algunas'] )
regla_p19 = ctrl.Rule(tiempo_respuesta['rapido'] & errores_consec['ninguno'] & precision['alta'], pistas_dificultad['algunas'] )
regla_p20 = ctrl.Rule(tiempo_respuesta['rapido'] & errores_consec['ninguno'] & precision['muy_alta'], pistas_dificultad['muchas'] )
regla_p21 = ctrl.Rule(tiempo_respuesta['rapido'] & errores_consec['pocos'] & precision['muy_baja'], pistas_dificultad['muchas'] )
regla_p22 = ctrl.Rule(tiempo_respuesta['rapido'] & errores_consec['pocos'] & precision['baja'], pistas_dificultad['muchas'] )
regla_p23 = ctrl.Rule(tiempo_respuesta['rapido'] & errores_consec['pocos'] & precision['media'], pistas_dificultad['muchas'] )
regla_p24 = ctrl.Rule(tiempo_respuesta['rapido'] & errores_consec['pocos'] & precision['alta'], pistas_dificultad['algunas'] )
regla_p25 = ctrl.Rule(tiempo_respuesta['rapido'] & errores_consec['pocos'] & precision['muy_alta'], pistas_dificultad['algunas'] )
regla_p26 = ctrl.Rule(tiempo_respuesta['rapido'] & errores_consec['muchos'] & precision['muy_baja'], pistas_dificultad['muchas'] )
regla_p27 = ctrl.Rule(tiempo_respuesta['rapido'] & errores_consec['muchos'] & precision['baja'], pistas_dificultad['muchas'] )
regla_p28 = ctrl.Rule(tiempo_respuesta['rapido'] & errores_consec['muchos'] & precision['media'], pistas_dificultad['muchas'] )
regla_p29 = ctrl.Rule(tiempo_respuesta['rapido'] & errores_consec['muchos'] & precision['alta'], pistas_dificultad['muchas'] )
regla_p30 = ctrl.Rule(tiempo_respuesta['rapido'] & errores_consec['muchos'] & precision['muy_alta'], pistas_dificultad['algunas'] )
regla_p30 = ctrl.Rule(tiempo_respuesta['medio'] & errores_consec['ninguno'] & precision['muy_baja'], pistas_dificultad['muchas'] )
regla_p31 = ctrl.Rule(tiempo_respuesta['medio'] & errores_consec['ninguno'] & precision['baja'], pistas_dificultad['muchas'] )
regla_p32 = ctrl.Rule(tiempo_respuesta['medio'] & errores_consec['ninguno'] & precision['media'], pistas_dificultad['algunas'] )
regla_p33 = ctrl.Rule(tiempo_respuesta['medio'] & errores_consec['ninguno'] & precision['alta'], pistas_dificultad['muchas'] )
regla_p34 = ctrl.Rule(tiempo_respuesta['medio'] & errores_consec['ninguno'] & precision['muy_alta'], pistas_dificultad['pocas'] )
regla_p35 = ctrl.Rule(tiempo_respuesta['medio'] & errores_consec['pocos'] & precision['muy_baja'], pistas_dificultad['muchas'] )
regla_p36 = ctrl.Rule(tiempo_respuesta['medio'] & errores_consec['pocos'] & precision['baja'], pistas_dificultad['muchas'] )
regla_p37 = ctrl.Rule(tiempo_respuesta['medio'] & errores_consec['pocos'] & precision['media'], pistas_dificultad['muchas'] )
regla_p38 = ctrl.Rule(tiempo_respuesta['medio'] & errores_consec['pocos'] & precision['alta'], pistas_dificultad['algunas'] )
regla_p39 = ctrl.Rule(tiempo_respuesta['medio'] & errores_consec['pocos'] & precision['muy_alta'], pistas_dificultad['algunas'] )
regla_p40 = ctrl.Rule(tiempo_respuesta['medio'] & errores_consec['muchos'] & precision['muy_baja'], pistas_dificultad['algunas'] )
regla_p41 = ctrl.Rule(tiempo_respuesta['medio'] & errores_consec['muchos'] & precision['baja'], pistas_dificultad['muchas'] )
regla_p42 = ctrl.Rule(tiempo_respuesta['medio'] & errores_consec['muchos'] & precision['media'], pistas_dificultad['muchas'] )
regla_p43 = ctrl.Rule(tiempo_respuesta['medio'] & errores_consec['muchos'] & precision['alta'], pistas_dificultad['muchas'] )
regla_p44 = ctrl.Rule(tiempo_respuesta['medio'] & errores_consec['muchos'] & precision['muy_alta'], pistas_dificultad['muchas'] )
regla_p45 = ctrl.Rule(tiempo_respuesta['lento'] & errores_consec['ninguno'] & precision['muy_baja'], pistas_dificultad['muchas'] )
regla_p46 = ctrl.Rule(tiempo_respuesta['lento'] & errores_consec['ninguno'] & precision['baja'], pistas_dificultad['muchas'] )
regla_p47 = ctrl.Rule(tiempo_respuesta['lento'] & errores_consec['ninguno'] & precision['media'], pistas_dificultad['muchas'] )
regla_p48 = ctrl.Rule(tiempo_respuesta['lento'] & errores_consec['ninguno'] & precision['alta'], pistas_dificultad['muchas'] )
regla_p49 = ctrl.Rule(tiempo_respuesta['lento'] & errores_consec['ninguno'] & precision['muy_alta'], pistas_dificultad['algunas'] )
regla_p50 = ctrl.Rule(tiempo_respuesta['lento'] & errores_consec['pocos'] & precision['muy_baja'], pistas_dificultad['muchas'] )
regla_p52 = ctrl.Rule(tiempo_respuesta['lento'] & errores_consec['pocos'] & precision['media'], pistas_dificultad['muchas'] )
regla_p53 = ctrl.Rule(tiempo_respuesta['lento'] & errores_consec['pocos'] & precision['alta'], pistas_dificultad['muchas'] )
regla_p54 = ctrl.Rule(tiempo_respuesta['lento'] & errores_consec['pocos'] & precision['muy_alta'], pistas_dificultad['muchas'] )
regla_p55 = ctrl.Rule(tiempo_respuesta['lento'] & errores_consec['muchos'] & precision['muy_baja'], pistas_dificultad['muchas'] )
regla_p56 = ctrl.Rule(tiempo_respuesta['lento'] & errores_consec['muchos'] & precision['baja'], pistas_dificultad['muchas'] )
regla_p57 = ctrl.Rule(tiempo_respuesta['lento'] & errores_consec['muchos'] & precision['media'], pistas_dificultad['muchas'] )
regla_p58 = ctrl.Rule(tiempo_respuesta['lento'] & errores_consec['muchos'] & precision['alta'], pistas_dificultad['muchas'] )
regla_p59 = ctrl.Rule(tiempo_respuesta['lento'] & errores_consec['muchos'] & precision['muy_alta'], pistas_dificultad['muchas'] )
regla_p51 = ctrl.Rule(tiempo_respuesta['lento'] & errores_consec['pocos'] & precision['baja'], pistas_dificultad['muchas'] )
regla_p60 = ctrl.Rule(tiempo_respuesta['muy_lento'] & errores_consec['ninguno'] & precision['muy_baja'], pistas_dificultad['muchas'] )
regla_p61 = ctrl.Rule(tiempo_respuesta['muy_lento'] & errores_consec['ninguno'] & precision['baja'], pistas_dificultad['muchas'] )
regla_p62 = ctrl.Rule(tiempo_respuesta['muy_lento'] & errores_consec['ninguno'] & precision['media'], pistas_dificultad['muchas'] )
regla_p63 = ctrl.Rule(tiempo_respuesta['muy_lento'] & errores_consec['ninguno'] & precision['alta'], pistas_dificultad['muchas'] )
regla_p64 = ctrl.Rule(tiempo_respuesta['muy_lento'] & errores_consec['ninguno'] & precision['muy_alta'], pistas_dificultad['muchas'] )
regla_p65 = ctrl.Rule(tiempo_respuesta['muy_lento'] & errores_consec['pocos'] & precision['muy_baja'], pistas_dificultad['muchas'] )
regla_p66 = ctrl.Rule(tiempo_respuesta['muy_lento'] & errores_consec['pocos'] & precision['baja'], pistas_dificultad['muchas'] )
regla_p67 = ctrl.Rule(tiempo_respuesta['muy_lento'] & errores_consec['pocos'] & precision['media'], pistas_dificultad['muchas'] )
regla_p68 = ctrl.Rule(tiempo_respuesta['muy_lento'] & errores_consec['pocos'] & precision['alta'], pistas_dificultad['muchas'] )
regla_p69 = ctrl.Rule(tiempo_respuesta['muy_lento'] & errores_consec['pocos'] & precision['muy_alta'], pistas_dificultad['muchas'] )
regla_p70 = ctrl.Rule(tiempo_respuesta['muy_lento'] & errores_consec['muchos'] & precision['muy_baja'], pistas_dificultad['muchas'] )
regla_p71 = ctrl.Rule(tiempo_respuesta['muy_lento'] & errores_consec['muchos'] & precision['baja'], pistas_dificultad['muchas'] )
regla_p72 = ctrl.Rule(tiempo_respuesta['muy_lento'] & errores_consec['muchos'] & precision['media'], pistas_dificultad['muchas'] )
regla_p73 = ctrl.Rule(tiempo_respuesta['muy_lento'] & errores_consec['muchos'] & precision['alta'], pistas_dificultad['muchas'] )
regla_p74 = ctrl.Rule(tiempo_respuesta['muy_lento'] & errores_consec['muchos'] & precision['muy_alta'], pistas_dificultad['muchas'] )

regla_t1 = ctrl.Rule(tiempo_respuesta['muy_rapido'] & aciertos['ninguno'], tiempo_otorgado['largo'])
regla_t2 = ctrl.Rule(tiempo_respuesta['muy_rapido'] & aciertos['pocos'], tiempo_otorgado['largo'])
regla_t3 = ctrl.Rule(tiempo_respuesta['muy_rapido'] & aciertos['medios'], tiempo_otorgado['medio'])
regla_t4 = ctrl.Rule(tiempo_respuesta['muy_rapido'] & aciertos['altos'], tiempo_otorgado['corto'])
regla_t5 = ctrl.Rule(tiempo_respuesta['muy_rapido'] & aciertos['muy_altos'], tiempo_otorgado['corto'])
regla_t6 = ctrl.Rule(tiempo_respuesta['rapido'] & aciertos['ninguno'], tiempo_otorgado['largo'])
regla_t7 = ctrl.Rule(tiempo_respuesta['rapido'] & aciertos['pocos'], tiempo_otorgado['largo'])
regla_t8 = ctrl.Rule(tiempo_respuesta['rapido'] & aciertos['medios'], tiempo_otorgado['medio'])
regla_t9 = ctrl.Rule(tiempo_respuesta['rapido'] & aciertos['altos'], tiempo_otorgado['corto'])
regla_t10 = ctrl.Rule(tiempo_respuesta['rapido'] & aciertos['muy_altos'], tiempo_otorgado['corto'])
regla_t11 = ctrl.Rule(tiempo_respuesta['medio'] & aciertos['ninguno'], tiempo_otorgado['largo'])
regla_t12 = ctrl.Rule(tiempo_respuesta['medio'] & aciertos['pocos'], tiempo_otorgado['largo'])
regla_t13 = ctrl.Rule(tiempo_respuesta['medio'] & aciertos['medios'], tiempo_otorgado['largo'])
regla_t14 = ctrl.Rule(tiempo_respuesta['medio'] & aciertos['altos'], tiempo_otorgado['medio'])
regla_t15 = ctrl.Rule(tiempo_respuesta['medio'] & aciertos['muy_altos'], tiempo_otorgado['corto'])
regla_t16 = ctrl.Rule(tiempo_respuesta['lento'] & aciertos['ninguno'], tiempo_otorgado['largo'])
regla_t17 = ctrl.Rule(tiempo_respuesta['lento'] & aciertos['pocos'], tiempo_otorgado['largo'])
regla_t18 = ctrl.Rule(tiempo_respuesta['lento'] & aciertos['medios'], tiempo_otorgado['largo'])
regla_t19 = ctrl.Rule(tiempo_respuesta['lento'] & aciertos['altos'], tiempo_otorgado['medio'])
regla_t20 = ctrl.Rule(tiempo_respuesta['lento'] & aciertos['muy_altos'], tiempo_otorgado['medio'])
regla_t21 = ctrl.Rule(tiempo_respuesta['muy_lento'] & aciertos['ninguno'], tiempo_otorgado['largo'])
regla_t22 = ctrl.Rule(tiempo_respuesta['muy_lento'] & aciertos['pocos'], tiempo_otorgado['largo'])
regla_t23 = ctrl.Rule(tiempo_respuesta['muy_lento'] & aciertos['medios'], tiempo_otorgado['largo'])
regla_t24 = ctrl.Rule(tiempo_respuesta['muy_lento'] & aciertos['altos'], tiempo_otorgado['largo'])
regla_t25 = ctrl.Rule(tiempo_respuesta['muy_lento'] & aciertos['muy_altos'], tiempo_otorgado['medio'])

todas_reglas = [
    regla_n1, regla_n2,regla_n3, regla_n4,regla_n5, regla_n6,regla_n7, regla_n8,regla_n9, regla_n10,regla_n11, regla_n12,
    regla_n13, regla_n14,regla_n15, regla_n16,regla_n17, regla_n18,regla_n19, regla_n20,regla_n21, regla_n22,regla_n23, regla_n24,
    regla_n25, regla_n26,regla_n27, regla_n28,regla_n29, regla_n30,regla_n31, regla_n32,regla_n33, regla_n34,regla_n35, regla_n36,
    regla_n37, regla_n38,regla_n39, regla_n40,regla_n41, regla_n42,regla_n43, regla_n44,regla_n45, regla_n46,regla_n47, regla_n48,
    regla_n49, regla_n50,regla_n51, regla_n52,regla_n53, regla_n54,regla_n55, regla_n56,regla_n57, regla_n58,regla_n59, regla_n60,
    regla_n61, regla_n62,regla_n63, regla_n64,regla_n65, regla_n66,regla_n67, regla_n68,regla_n69, regla_n70,regla_n71, regla_n24,
    regla_n72, regla_n73,regla_n74,

    regla_m1, regla_m2,regla_m3, regla_m4,regla_m5, regla_m6,regla_m7, regla_m8,regla_m9, regla_m10,regla_m11, regla_m12,
    regla_m13, regla_m14,regla_m15,

    regla_p1, regla_p2,regla_p3, regla_p4,regla_p5, regla_p6,regla_p7, regla_p8,regla_p9, regla_p10,regla_p11, regla_p12,
    regla_p13, regla_p14,regla_p15, regla_p16,regla_p17, regla_p18,regla_p19, regla_p20,regla_p21, regla_p22,regla_p23, regla_p24,
    regla_p25, regla_p26,regla_p27, regla_p28,regla_p29, regla_p30,regla_p31, regla_p32,regla_p33, regla_p34,regla_p35, regla_p36,
    regla_p37, regla_p38,regla_p39, regla_p40,regla_p41, regla_p42,regla_p43, regla_p44,regla_p45, regla_p46,regla_p47, regla_p48,
    regla_p49, regla_p50,regla_p51, regla_p52,regla_p53, regla_p54,regla_p55, regla_p56,regla_p57, regla_p58,regla_p59, regla_p60,
    regla_p61, regla_p62,regla_p63, regla_p64,regla_p65, regla_p66,regla_p67, regla_p68,regla_p69, regla_p70,regla_p71, regla_p24,
    regla_p72, regla_p73,regla_p74,

    regla_t1, regla_t2,regla_t3, regla_t4,regla_t5, regla_t6,regla_t7, regla_t8,regla_t9, regla_t10,regla_t11, regla_t12,
    regla_t13, regla_t14,regla_t15, regla_t16,regla_t17, regla_t18,regla_t19, regla_t20,regla_t21, regla_t22,regla_t23, regla_t24,
    regla_t25

]

tutor_ctrl = ctrl.ControlSystem(todas_reglas)

def evaluar_tutor(tiempo_promedio, aciertos_count, errores_consecutivos, precision_percent):
    """Evaluación basada en historial completo"""
    sim = ctrl.ControlSystemSimulation(tutor_ctrl)
    sim.input['tiempo_respuesta'] = min(45, max(0, tiempo_promedio))
    sim.input['aciertos'] = min(10, max(0, aciertos_count))
    sim.input['errores_consec'] = min(5, max(0, errores_consecutivos))
    sim.input['precision'] = min(100, max(0, precision_percent))
    
    try:
        sim.compute()
    except:
        return {
            'nivel': 1, 
            'pistas': 3, 
            'motivacion': 5, 
            'tiempo_otorgado': 30
        }
    return {
        'nivel': sim.output.get('nivel', 1),
        'pistas': sim.output.get('pistas_nivel', 3),
        'motivacion': sim.output.get('motivacion', 5),
        'tiempo_otorgado': int(sim.output.get('tiempo_otorgado', 30))
    }

def esta_en_fase_inicial():
    """Determina si está en las primeras 10 preguntas"""
    total_preguntas = len(session.get("historial_aciertos", []))
    return total_preguntas < 5

def obtener_evaluacion_principiante():
    """Configuración fija para fase inicial"""
    return {
        'nivel': 1,  # Siempre principiante
        'pistas': 3,  # Máximas pistas
        'motivacion': 5,  # Motivación neutral
        'tiempo_otorgado': 30  # Tiempo normal (no se usa en nivel 1)
    }

def analizar_historial_completo():
    historial_aciertos = session.get("historial_aciertos", [])
    historial_tiempos  = session.get("historial_tiempos", [])
    
    if len(historial_aciertos) == 0:
        return obtener_evaluacion_principiante()

    precision_total      = sum(historial_aciertos) / len(historial_aciertos) * 100
    tiempo_promedio      = sum(historial_tiempos) / len(historial_tiempos)
    aciertos_recientes   = sum(historial_aciertos[-10:])
    errores_consecutivos = session.get("errores_consecutivos", 0)

    return evaluar_tutor(
        tiempo_promedio,
        aciertos_recientes,
        errores_consecutivos,
        precision_total
    )

def generar_pregunta_adaptativa(evaluacion_tutor):

    nivel_visual = session.get("nivel", 1)
    preguntas_anteriores = session.get("preguntas_anteriores", [])
    disponibles = [p for p in PIEZAS.items() if p[0] not in preguntas_anteriores[-10:]]

    if len(disponibles) < 3:
        preguntas_anteriores = []
        disponibles = list(PIEZAS.items())

    pieza, pistas = random.choice(disponibles)
    preguntas_anteriores.append(pieza)
    session["preguntas_anteriores"] = preguntas_anteriores[-10:]

    pistas_num = evaluacion_tutor['pistas']
    if pistas_num >= 2.5:
        pista = " | ".join(pistas[:3])
    elif pistas_num >= 1.5:
        pista = " | ".join(pistas[:2])
    else:
        pista = pistas[-1]
    opciones = []
    distractores = [p for p in PIEZAS.keys() if p != pieza]

    if nivel_visual == 1:
        opciones = random.sample(distractores, 2) + [pieza]
        random.shuffle(opciones)
        tiempo_limite = None

    elif nivel_visual == 2:
        opciones = random.sample(distractores, 2) + [pieza]
        random.shuffle(opciones)
        tiempo_limite = evaluacion_tutor.get("tiempo_otorgado", 20)

    elif nivel_visual == 3:
        opciones = []
        tiempo_limite = None

    elif nivel_visual == 4:
        modo = random.choice([1, 2, 3])

        if modo == 1:
            opciones = random.sample(distractores, 2) + [pieza]
            random.shuffle(opciones)
            tiempo_limite = None

        elif modo == 2:
            opciones = random.sample(distractores, 2) + [pieza]
            random.shuffle(opciones)
            tiempo_limite = evaluacion_tutor.get("tiempo_otorgado", 20)

        else:
            opciones = []
            tiempo_limite = None

    else:  
        opciones = []
        tiempo_limite = evaluacion_tutor.get("tiempo_otorgado", 20)

    return {
        "pieza": pieza,
        "pista": pista,
        "opciones": opciones,
        "tiempo_limite": tiempo_limite
    }

def regla_respuesta(respuesta, correcta, tiempo):
    if normalizar(respuesta) == normalizar(correcta):
        session["errores_consecutivos"] = 0
        
        bonus = max(0, 10 - tiempo) * 0.05 if tiempo < 10 else 0
        puntos = 1 + bonus
        
        session["racha"] = session.get("racha", 0) + 1
        
        if session["racha"] >= 3:
            puntos += 0.2
            mensaje = f"¡Correcto! +{puntos:.1f} pts (¡Racha {session['racha']}!)"
        else:
            mensaje = f"¡Correcto! +{puntos:.1f} pts"

        return {
            "acierto": True,
            "puntos": puntos,
            "vidas": 0,
            "mensaje": mensaje
        }
    
    else:
        session["errores_consecutivos"] = session.get("errores_consecutivos", 0) + 1
        session["racha"] = 0
        
        mensaje = f"Incorrecto. Era: {correcta}"
        
        return {
            "acierto": False,
            "puntos": 0,
            "vidas": -1,
            "mensaje": mensaje
        }


def regla_subir_nivel(racha, nivel, puntos):
    nuevo_nivel = nivel
    
    if nivel == 1 and racha >= 6:
        nuevo_nivel = 2
    elif nivel == 2 and racha >= 10:
        nuevo_nivel = 3
    elif nivel == 3 and racha >= 15:
        nuevo_nivel = 4
    elif nivel == 4 and racha >= 18:
        nuevo_nivel = 5
    
    if nuevo_nivel != nivel:
        return nuevo_nivel, 0
    
    return nivel, racha


@trivia_bp.route("/trivia", methods=["GET", "POST"])
def trivia():
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
            "ultimo_mensaje": None,
            "evaluacion_anterior": {'nivel': 1}
        })

    if request.method == "POST":
        respuesta = request.form.get("respuesta", "")
        correcta = request.form.get("correcta", "")
        tiempo_transcurrido = time.time() - session["start_time"]
        
        resultado = regla_respuesta(respuesta, correcta, tiempo_transcurrido)
        session["puntos"] += resultado["puntos"]
        session["vidas"] += resultado["vidas"]
        
        session.setdefault("historial_aciertos", [])
        session.setdefault("historial_tiempos", [])
        
        session["historial_aciertos"].append(1 if resultado["acierto"] else 0)
        session["historial_tiempos"].append(tiempo_transcurrido)
        
        session["historial_aciertos"] = session["historial_aciertos"][-5:]
        session["historial_tiempos"] = session["historial_tiempos"][-5:]
        
        session["nivel"], session["racha"] = regla_subir_nivel(
            session["racha"], 
            session["nivel"],
            session["puntos"]
        )
        
        registrar_logros()
        
        if esta_en_fase_inicial():
            evaluacion = obtener_evaluacion_principiante()
            fase_info = " | FASE INICIAL"
        else:
            evaluacion = analizar_historial_completo()
            fase_info = " | FASE ADAPTATIVA"
        
        mensaje_motivacional = generar_mensaje_motivacional(evaluacion['motivacion'])
        resultado["mensaje"] += f" | {mensaje_motivacional}{fase_info}"
        
        nivel_eval = evaluacion['nivel']
        if nivel_eval < 4:
            resultado["mensaje"] += " | CATEGORIA: PRINCIPIANTE [Apto para PASANTE]"
        elif nivel_eval < 7:
            resultado["mensaje"] += " | CATEGORIA: INTERMEDIO [Apto para AYUDANTE]"
        else:
            resultado["mensaje"] += " | CATEGORIA: EXPERTO [Apto para MECÁNICO]"
        
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

    if esta_en_fase_inicial():
        evaluacion = obtener_evaluacion_principiante()
    else:
        evaluacion = analizar_historial_completo()
    
    pregunta = generar_pregunta_adaptativa(evaluacion)
    session["correcta"] = pregunta["pieza"]
    session["start_time"] = time.time()
    
    total_preguntas = len(session.get("historial_aciertos", [0]))
    precision_percent = (sum(session.get("historial_aciertos", [0])) / max(1, total_preguntas) * 100) if total_preguntas > 0 else 0
    
    return render_template("trivia.html",
                           pregunta=pregunta,
                           nivel=session["nivel"],
                           vidas=session["vidas"],
                           puntos=session["puntos"],
                           racha=session["racha"],
                           logros=session.get("logros", []),
                           precision=precision_percent,
                           tiempo_limite=pregunta.get("tiempo_limite"),
                           fase="Inicial" if esta_en_fase_inicial() else "Adaptativa")

def generar_mensaje_motivacional(tipo_motivacion):
    if tipo_motivacion < 3:
        mensajes = ["No te desanimes, el aprendizaje es progresivo."]
    elif tipo_motivacion < 7:
        mensajes = ["Vas por buen camino, mantén la concentración."]
    else:
        mensajes = ["¡Rendimiento excepcional! Eres un experto."]
    return random.choice(mensajes)

def registrar_logros():
    """Sistema de logros unificado y ampliado"""
    logros = session.setdefault("logros", [])
    total_preguntas = len(session.get("historial_aciertos", []))
    
    if total_preguntas >= 5 and "completado_fase_inicial" not in logros:
        logros.append("completado_fase_inicial")
    
    for pts, key in [(10, "10_puntos"), (25, "25_puntos"), (50, "50_puntos"), (100, "100_puntos")]:
        if session.get("puntos", 0) >= pts and key not in logros:
            logros.append(key)
    
    for niv, key in [(3, "nivel_3"), (4, "nivel_4"), (5, "nivel_5")]:
        if session.get("nivel", 1) >= niv and key not in logros:
            logros.append(key)

    for r, key in [(5, "racha_5"), (10, "racha_10"), (15, "racha_15"), (20, "racha_20")]:
        if session.get("racha", 0) >= r and key not in logros:
            logros.append(key)

    for di, key in [(4, "Insignia_pasante"), (7, "Insignia_tallerista"), (10, "Insignia_mecánico")]:
        if session.get("dificultad", 0) >= di and key not in logros:
            logros.append(key)

    if total_preguntas >= 5:
        tiempos = session.get("historial_tiempos", [])
        if tiempos and sum(tiempos[-5:]) / min(5, len(tiempos[-5:])) < 5:
            if "velocista" not in logros:
                logros.append("velocista")

    if total_preguntas >= 10:
        if sum(session["historial_aciertos"][-10:]) == 10 and "perfeccion" not in logros:
            logros.append("perfeccion")
    
    if total_preguntas >= 10:
        precision = sum(session["historial_aciertos"]) / total_preguntas * 100
        if precision >= 95 and "precision_95" not in logros:
            logros.append("precision_95")
    
    session["logros"] = logros

def actualizar_nivel(respuesta_correcta):
    nivel = session.get("nivel", 1)
    racha = session.get("racha", 0)

    if respuesta_correcta:
        racha += 1
    else:
        racha = 0
    if racha >= nivel * 2:
        nivel += 1
        racha = 0  
    session["racha"] = racha
    session["nivel"] = nivel
