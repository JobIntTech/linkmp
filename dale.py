import datetime
import requests
import csv
from simple_salesforce import Salesforce
from google.cloud import bigquery

# Credenciales de autenticación para BigQuery
credentials_path = 'auth.json'

def cargar_credenciales(ruta_archivo):
    with open(ruta_archivo, 'r') as archivo:
        credenciales = {line.split('=')[0].strip(): line.split('=')[1].strip() for line in archivo}
    return credenciales

def ejecutar_servicio():
    # Cargar credenciales
    credenciales_salesforce = cargar_credenciales('salesforce_credentials.txt')

    # Obtener el token de autenticación de Salesforce
    url_auth = 'https://login.salesforce.com/services/oauth2/token'
    data_auth = {
        'grant_type': 'password',
        'client_id': credenciales_salesforce['client_id'],
        'client_secret': credenciales_salesforce['client_secret'],
        'username': credenciales_salesforce['username'],
        'password': credenciales_salesforce['password']
    }

    response = requests.post(url_auth, data=data_auth)
    auth_data = response.json()
    access_token = auth_data['access_token']

    # Crear una instancia de simple_salesforce utilizando el token de autenticación
    salesforce_instance_url = auth_data['instance_url']
    sf = Salesforce(instance_url=salesforce_instance_url, session_id=access_token)

    # Consulta Salesforce
    query = """
    SELECT Id, Name, Type, RecordTypeId, Phone, NumberOfEmployees, CurrencyIsoCode, OwnerId, CreatedDate,
           CreatedById, LastModifiedDate, LastModifiedById, SystemModstamp, LastActivityDate, AccountSource,
           Alias_Cta_Cte__c, Bloqueado__c, Ciudad_de_facturacion2__c, Ciudad_de_operacion__c,
           Codigo_postal_de_facturacion__c, Codigo_postal_de_operacion__c, Condicion_fiscal__c,
           Correo_electronico_de_contacto_principal__c, Direccion_de_facturacion__c, Direccion_de_operacion__c,
           Dominio_HR__c, Fecha_de_ultimo_error_SAP__c, Funcion__c, Giro_comercial__c, Giro_de_Negocio__c,
           Grupo_economico__c, ID_Cliente_SAP__c, ID_Cuenta_SF__c, Nombre_de_Fantasia__c,
           Nombre_del_propietario_de_la_cuenta__c, Numero_de_documento_fiscal__c, Organizacion_de_venta_principal__c,
           Pais_de_facturacion__c, Pais_de_operacion__c, Perfil_crediticio__c, Provincia_Estado_de_facturacion__c,
           Provincia_Estado_de_operacion__c, Requiere_orden_de_compra__c, Tipo_de_documento__c,
           Zona_Barrio_Colonia_Comuna_facturacion2__c, Zona_Barrio_Colonia_Comuna_operacion__c, id_externo_exclusivo__c,
           HR_New__c, Actividad__c, Cantidad_de_oportunidades__c, Fecha_ultima_oportunidad__c, Ult_Actividad__c,
           Ult_Gestion__c, Esperando_tarea__c, Fecha_Ult_Freemium__c, Fecha_primera_oportunidad__c, Sin_necesidad__c,
           Fecha_ltima_oportunidad_ecommerce__c
    FROM Account
    where CreatedDate = TODAY
    order by ID_Cuenta_SF__c desc
    limit 1
    """

    result = sf.query_all(query)
    records = result['records']

    # Obtener la fecha y hora actual
    fecha_hora_actual = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Parsear los campos de fecha y hora al formato deseado
    for record in records:
        record['attributes'] = f"{fecha_hora_actual} api.bycmendoza"
        # Parsear CreatedDate
        created_date = datetime.datetime.strptime(record['CreatedDate'], "%Y-%m-%dT%H:%M:%S.%f+0000")
        record['CreatedDate'] = created_date.strftime("%Y-%m-%d %H:%M:%S")  # O el formato que necesites

        # Parsear LastModifiedDate
        last_modified_date = datetime.datetime.strptime(record['LastModifiedDate'], "%Y-%m-%dT%H:%M:%S.%f+0000")
        record['LastModifiedDate'] = last_modified_date.strftime("%Y-%m-%d %H:%M:%S")  # O el formato que necesites

        # Parsear SystemModstamp
        system_modstamp_date = datetime.datetime.strptime(record['SystemModstamp'], "%Y-%m-%dT%H:%M:%S.%f+0000")
        record['SystemModstamp'] = system_modstamp_date.strftime("%Y-%m-%d %H:%M:%S")  # O el formato que necesites

        # Parsear Ult_Actividad__c si existe
        if 'Ult_Actividad__c' in record and record['Ult_Actividad__c'] is not None:
            ult_actividad_date = datetime.datetime.strptime(record['Ult_Actividad__c'], "%Y-%m-%dT%H:%M:%S.%f+0000")
            record['Ult_Actividad__c'] = ult_actividad_date.strftime("%Y-%m-%d %H:%M:%S")  # O el formato que necesites

        # Parsear Ult_Gestion__c si existe
        if 'Ult_Gestion__c' in record and record['Ult_Gestion__c'] is not None:
            ult_gestion_date = datetime.datetime.strptime(record['Ult_Gestion__c'], "%Y-%m-%dT%H:%M:%S.%f+0000")
            record['Ult_Gestion__c'] = ult_gestion_date.strftime("%Y-%m-%d %H:%M:%S")  # O el formato que necesites

        # Parsear 'Cantidad_de_oportunidades__c' si existe
        if 'Cantidad_de_oportunidades__c' in record and record['Cantidad_de_oportunidades__c'] is not None:
            record['Cantidad_de_oportunidades__c'] = int(record['Cantidad_de_oportunidades__c'])

    # Escribir los resultados en un archivo CSV
    csv_file_path = 'datos.csv'
    fieldnames = records[0].keys()
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for record in records:
            writer.writerow(record)

    # Configuración del cliente de BigQuery
    client = bigquery.Client.from_service_account_json(credentials_path)

    # Nombre del conjunto de datos y tabla en BigQuery donde insertaremos los datos
    dataset_id = 'salesforce'
    table_id = 'Accounts'

    # Referencia a la tabla en BigQuery
    table_ref = client.dataset(dataset_id).table(table_id)

    # Especifica el formato de origen del archivo CSV y la fila desde la cual empezar a leer
    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1,  # Empieza a leer desde la segunda fila (fila 2)
    )

    # Usa el método load_table_from_file para cargar el archivo CSV en la tabla
    with open(csv_file_path, "rb") as source_file:
        job = client.load_table_from_file(source_file, table_ref, job_config=job_config)

    job.result()  # Espera a que la carga del archivo se complete

    print("Archivo CSV cargado exitosamente en BigQuery.")

# Llamar a la función para ejecutar el servicio
ejecutar_servicio()