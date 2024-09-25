
from abc import ABC, abstractmethod
import urllib.parse
import csv
from datetime import datetime

class URLGeneratorBase(ABC):
    def __init__(self, input_file):
        self.input_file = input_file
        self.urls = []
        self.canal = 'default_channel'  # Puedes cambiar esto o asignarlo dinámicamente según sea necesario

    @abstractmethod
    def validate_params(self, params):
        """Este método será implementado por cada canal para validar los parámetros."""
        pass

    @abstractmethod
    def generate_urls(self, params):
        """Este método será implementado por cada canal para generar las URLs."""
        pass

    def encode_url(self, url):
        """Codifica una URL de destino."""
        return urllib.parse.quote(url, safe='')

    def process_csv(self):
        """Lee el archivo CSV, valida los parámetros y genera las URLs."""
        try:
            with open(self.input_file, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    if row:  # Saltar cualquier fila vacía
                        try:
                            # Limpiar el espacio en blanco en las filas del CSV y evitar None
                            row = {k.strip(): (v.strip() if v is not None else '') for k, v in row.items() if k and v}
                            
                            # Solo procesar si hay suficientes valores en la fila
                            if row:
                                self.validate_params(row)  # Validar los parámetros
                                url_click_redirect, url_impression, url_click_params = self.generate_urls(row)
                                self.urls.append({
                                    'URL de Clic (Redirección)': url_click_redirect,
                                    'URL de Impresión': url_impression,
                                    'URL de Clic (Tracking por Parámetros)': url_click_params
                                })
                        except ValueError as e:
                            print(f"Error en la fila: {row} - {str(e)}")
        except FileNotFoundError:
            print(f"El archivo {self.input_file} no existe.")
        except Exception as e:
            print(f"Ocurrió un error procesando el archivo: {str(e)}")

        self.write_csv()

    def generate_output_filename(self):
        """Generates a unique output filename with date, time, and channel."""
        now = datetime.now()
        timestamp = now.strftime("%Y_%m_%d_%H_%M_%S")
        return f"{timestamp}_urls_{self.canal}_generadas.csv"

    def write_csv(self):
        """Escribe las URLs generadas en un archivo CSV."""
        output_file = self.generate_output_filename()  # Usar el nombre con timestamp
        try:
            with open(output_file, mode='w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['URL de Clic (Redirección)', 'URL de Impresión', 'URL de Clic (Tracking por Parámetros)']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                writer.writeheader()
                for url in self.urls:
                    writer.writerow(url)
            
            print(f"Las URLs generadas se han guardado en {output_file}.")
        except Exception as e:
            print(f"Error al escribir el archivo: {str(e)}")
