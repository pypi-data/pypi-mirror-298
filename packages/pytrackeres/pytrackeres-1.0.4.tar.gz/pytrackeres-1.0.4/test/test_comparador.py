# test/test_comparador.py

from pytrackeres.url_generator.comparador import ComparadorPreciosURLGenerator

def test_generate_urls_comparador():
    generator = ComparadorPreciosURLGenerator("test_file.csv")
    params = {
        'dominio_tracking': 'aaa1.cliente.com',
        'sitio': 'cliente-com',
        'nombre_soporte': 'comparador',
        'nombre_campania': 'verano_2024',
        'nombre_banner': 'crea1',
        'url_destino': 'https://www.cliente.com?param=example'
    }
    urls = generator.generate_urls(params)
    assert len(urls) == 3
    assert 'https://aaa1.cliente.com/dynclick/cliente-com/' in urls[0]