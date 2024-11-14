from flask import Flask, jsonify, request
from werkzeug.exceptions import BadRequest
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
from IsMutante import is_mutant

app = Flask(__name__)

# Configuración de la cadena de conexión
server = 'testapp.database.windows.net'
database = 'Test'
username = 'bruno'
password = 'aGUS(2005)'

# Crear la conexión
conm_str = f"mssql+pymssql://{username}:{password}@{server}/{database}"
app.config['SQLALCHEMY_DATABASE_URI'] = conm_str
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

#TODO: store procedure
GET_RATIO = 'SP_L_RATIO_01'
ADD_ENTITY = 'SP_I_ENTITY_01'


# TODO: Home
@app.route('/')
def home():
    # Abre una conexión con el engine
    return render_template('index.html')


# TODO: Stats, get
@app.route('/Stats', methods=['GET'])
def Stats():
    try:
      with db.engine.connect() as connection:
       # Ejecuta la consulta
        sql_query = text(f'EXEC {GET_RATIO}')
        result = connection.execute(sql_query)
    
        data_json = []
        for row in result:
            try:
                row_dict = dict(row._asdict())
                data_json.append(row_dict)
            except Exception as e:
                print(f"Error al convertir la fila: {row} - Error: {e}")
      return jsonify(data_json)
    except Exception as e:
        return jsonify(f"error: {str(e)}")   



# TODO: Validate the dna
def validation_dna(dna):
    length = len(dna)
    # Verifica que la matriz sea cuadrada
    # Verifica que todos los campos sean 'A', 'T', 'C', 'G'
    for cadena in dna:
      if length != len(cadena):
        return False, "La matriz no es cuadrada"
      for letra in cadena:
        if letra.upper() not in ['A', 'T', 'C', 'G']:
            return False, "La matriz solo puede contener caracteres 'A', 'T', 'C', 'G'."
        
    return True, "La matriz de ADN es válida."
    

# TODO: Valida el formato de los datos en el body
def validate_data(data):
    # Verifica que 'dna' estén en los datos y que 'dna' cumpla las verificaciones
    if 'dna' not in data:
        return False, "El campo 'dna' es obligatorio y debe ser un string."
    else:
        return validation_dna(data['dna']) 
    
# TODO: Ruta para recibir la solicitud POST
@app.route('/mutant', methods=['POST'])
def submit():
    try:
        # Obtener y validar los datos en formato JSON
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Se esperaba un cuerpo en formato JSON'}), 400
        
        dna = data.get('dna')
        is_valid, error_message = validate_data(data)
        
        # Validación de los datos
        if not is_valid:
            return jsonify({'error': error_message}), 400

        # Verifica si el ADN es mutante
        mutant = is_mutant(dna)
        
        # Convertir el ADN a un formato compatible con SQL Server (una cadena)
        dna_str = ','.join(dna) if isinstance(dna, list) else dna
        
        # Ejecuta la consulta en una transacción
        with db.engine.begin() as connection:
            sql_query = text(f'EXEC {ADD_ENTITY} @Dna=:Dna, @IsMutant=:IsMutant')
            connection.execute(sql_query, {'Dna': dna_str, 'IsMutant': mutant})

        # Responder según el resultado
        return jsonify({'message': 'ADN mutante' if mutant else 'ADN humano'}), 200 if mutant else 401

    except BadRequest:
        # Error específico de JSON no válido
        return jsonify({'error': 'Se esperaba un cuerpo JSON válido'}), 400
    except SQLAlchemyError as e:
        # Manejo de errores de la base de datos
        return jsonify({'error': f'Error en la base de datos: {str(e)}'}), 500
    except Exception as e:
        # Manejo de otros posibles errores
        return jsonify({'error': f'Ocurrió un error inesperado: {str(e)}'}), 500
    

# TODO: iniciar la aplicacion si este script es ejecutado directamente
if __name__ == '__main__':
  # TODO: Configurar para ejecutar en modo depuracion
  app.run()
  