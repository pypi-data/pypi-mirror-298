import os
from pytrackeres.url_generator.display import DisplayURLGenerator
from pytrackeres.url_generator.afiliacion import AfiliacionURLGenerator
from pytrackeres.url_generator.emailing import EmailingURLGenerator
from pytrackeres.url_generator.colaboracion import ColaboracionURLGenerator
from pytrackeres.url_generator.comparador import ComparadorPreciosURLGenerator
from pytrackeres.url_generator.google_ads import GoogleAdsURLGenerator
from pytrackeres.url_generator.bing_ads import BingAdsURLGenerator
from pytrackeres.url_generator.social import SocialURLGenerator

# Diccionario con las plantillas de cabeceras para cada canal
CSV_TEMPLATES = {
    'dy': {
        'headers': "dominio_tracking,sitio,nombre_soporte,nombre_campania,nombre_ubicacion,nombre_banner,formato_banner,nombre_segmento,valor_segmento,url_destino,adid,idfa",
        'mandatory': "yes,yes,yes,yes,yes,yes,yes,no,no,yes,no,no",
        'example': "aaa1.cliente.com,cliente-com,amazon,verano_2024,ROS,crea1,300x250,,,https://www.cliente.com?param=example,,"
    },
    'af': {
        'headers': "dominio_tracking,sitio,nombre_soporte,nombre_campania,nombre_banner,formato_banner,nombre_segmento,valor_segmento,url_destino,nombre_plan_medios,adid,idfa",
        'mandatory': "yes,yes,yes,yes,yes,yes,no,no,yes,no,no,no",
        'example': "aaa1.cliente.com,cliente-com,awin,verano_2024,crea1,300x250,,,https://www.cliente.com?param=example,,,",
    },
    'em': {
        'headers': "dominio_tracking,sitio,nombre_soporte,nombre_campania,mail_usuario,nombre_segmento,valor_segmento,url_destino,nombre_plan_medios,id_cliente,adid,idfa",
        'mandatory': "yes,yes,yes,yes,no,no,no,yes,no,no,no,no",
        'example': "aaa1.cliente.com,cliente-com,mailchimp,verano_2024,,,,https://www.cliente.com?param=example,,,,,",
    },
    'co': {
        'headers': "dominio_tracking,sitio,nombre_soporte,nombre_campania,nombre_ubicacion,nombre_banner,formato_banner,nombre_segmento,valor_segmento,url_destino,adid,idfa",
        'mandatory': "yes,yes,yes,yes,yes,yes,yes,no,no,yes,no,no",
        'example': "aaa1.cliente.com,cliente-com,partner,verano_2024,ROS,crea1,300x250,,,https://www.cliente.com?param=example,,"
    },
    'cp': {
        'headers': "dominio_tracking,sitio,nombre_soporte,nombre_campania,nombre_banner,nombre_segmento,valor_segmento,url_destino,nombre_plan_medios,adid,idfa",
        'mandatory': "yes,yes,yes,yes,no,no,no,yes,no,no,no,no",
        'example': "aaa1.cliente.com,cliente-com,comparador,verano_2024,,,,https://www.cliente.com?param=example,,,,,"
    },
    'ga': {
        'headers': "dominio_tracking,sitio,nombre_soporte,nombre_campania,nombre_ubicacion,nombre_banner,formato_banner,nombre_segmento,valor_segmento,url_destino,adid,idfa",
        'mandatory': "yes,yes,yes,yes,yes,yes,yes,no,no,yes,no,no",
        'example': "aaa1.cliente.com,cliente-com,google-ads,verano_2024,ROS,crea1,300x250,,,https://www.cliente.com?param=example,,"
    },
    'ba': {
        'headers': "dominio_tracking,sitio,nombre_soporte,nombre_campania,nombre_ubicacion,nombre_banner,formato_banner,nombre_segmento,valor_segmento,url_destino,adid,idfa",
        'mandatory': "yes,yes,yes,yes,yes,yes,yes,no,no,yes,no,no",
        'example': "aaa1.cliente.com,cliente-com,bing-ads,verano_2024,ROS,crea1,300x250,,,https://www.cliente.com?param=example,,"
    },
    'sc': {
        'headers': "dominio_tracking,sitio,nombre_soporte,nombre_campania,nombre_ubicacion,nombre_banner,formato_banner,nombre_segmento,valor_segmento,url_destino, nombre_plan_medios,adid,idfa",
        'mandatory': "yes,yes,yes,yes,yes,yes,yes,no,no,yes,no,no",
        'example': "aaa1.cliente.com,cliente-com,facebook,verano_2024,ROS,crea1,300x250,,,https://www.cliente.com?param=example,,,"
    },
    # Otros canales en el futuro
}

def show_csv_template(channel):
    """Muestra la plantilla de CSV para el canal seleccionado"""
    template = CSV_TEMPLATES.get(channel)
    if template:
        print("\nA continuación dispones de la plantilla de las cabeceras del CSV esperado con un ejemplo y con los campos obligatorios para este canal.")
        print(f"\nHEADERS: {template['headers']}")
        print(f"MANDATORY: {template['mandatory']}")
        print(f"EXAMPLE: {template['example']}\n")
    else:
        print("No hay una plantilla disponible para este canal.")

def main(canal_input=None, input_file=None):
    if canal_input is None:
        canal_input = input("Introduce el nombre del canal para procesar (dy para Display, af para Afiliación, em para Emailing, co para Colaboración, cp para Comparador de Precios, ga para Google Ads, ba para Bing Ads, sc para Social): ")

    canal_map = {
        'dy': DisplayURLGenerator,
        'af': AfiliacionURLGenerator,
        'em': EmailingURLGenerator,
        'co': ColaboracionURLGenerator,
        'cp': ComparadorPreciosURLGenerator,
        'ga': GoogleAdsURLGenerator,
        'ba': BingAdsURLGenerator,
        'sc': SocialURLGenerator,
    }

    if canal_input not in canal_map:
        print("Canal no encontrado. Por favor usa el código correcto.")
        return

    show_csv_template(canal_input)

    if input_file is None:
        input_file = input(r"Por favor, introduce la ruta completa del fichero CSV. Por ejemplo C:\user\desktop\datos.csv: ")

    if not os.path.exists(input_file):
        print(f"El fichero {input_file} no existe.")
        return

    generator_class = canal_map[canal_input]
    generator = generator_class(input_file)
    generator.process_csv()

if __name__ == "__main__":
    main()