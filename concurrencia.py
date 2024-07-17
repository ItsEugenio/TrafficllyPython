from flask import Flask, request, jsonify
import statistics

app = Flask(__name__)

def validar_datos(datos):
    if not isinstance(datos, dict):
        raise ValueError("Los datos deben estar en un diccionario.")
    for día, registros in datos.items():
        if not isinstance(día, str):
            raise ValueError("Las claves del diccionario deben ser cadenas de texto.")
        if not isinstance(registros, list):
            raise ValueError(f"Los valores de '{día}' deben ser una lista.")
        for registro in registros:
            if not (isinstance(registro, list) and len(registro) == 2):
                raise ValueError(f"Cada registro en '{día}' debe ser una lista de dos elementos.")
            hora, personas = registro
            if not (isinstance(hora, str) and isinstance(personas, int)):
                raise ValueError(f"El registro '{registro}' en '{día}' debe contener una hora como cadena y un número de personas como entero.")

def calcular_estadísticas(datos):
    estadísticas = {}
    for día, registros in datos.items():
        if not registros:
            estadísticas[día] = {
                "media": 0,
                "desviación_estándar": 0
            }
        else:
            personas_por_hora = [personas for hora, personas in registros]
            media = statistics.mean(personas_por_hora)
            desviación_estándar = statistics.stdev(personas_por_hora) if len(personas_por_hora) > 1 else 0
            estadísticas[día] = {
                "media": media,
                "desviación_estándar": desviación_estándar
            }
    return estadísticas


@app.route('/trafico', methods=['POST'])
def trafico():
    try:
        datos = request.json
        print(datos)
        validar_datos(datos)
        
        estadísticas = calcular_estadísticas(datos)
        
        max_tráfico = 0
        candidatos = []

        for día, registros in datos.items():
            for hora, personas in registros:
                if personas > max_tráfico:
                    max_tráfico = personas
                    candidatos = [(día, hora, estadísticas[día]["media"])]
                elif personas == max_tráfico:
                    candidatos.append((día, hora, estadísticas[día]["media"]))

        if len(candidatos) == 1:
            día_max_tráfico, hora_max_tráfico, _ = candidatos[0]
        else:
            # en caso de haber días y horas que tengan la misma cantidad de personas, se compara con la media del día para saber el día de mayor tráfico.
            día_max_tráfico, hora_max_tráfico, _ = max(candidatos, key=lambda x: x[2])

        resultado = {
            "max_tráfico": max_tráfico,
            "día_max_tráfico": día_max_tráfico,
            "hora_max_tráfico": hora_max_tráfico,
            "estadísticas": estadísticas
        }
        return jsonify(resultado)
    
    except ValueError as e:
        print(e)
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, port=9500)
