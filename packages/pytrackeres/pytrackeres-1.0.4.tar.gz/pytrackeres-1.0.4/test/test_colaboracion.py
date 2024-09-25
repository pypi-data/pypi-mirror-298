# test/test_colaboracion.py

from pytrackeres.url_generator.colaboracion import ColaboracionURLGenerator

def test_generate_urls_colaboracion():
    generator = ColaboracionURLGenerator("test_file.csv")
    params = {
        'dominio_tracking': 'aaa1.cliente.com',
        'sitio': 'cliente-com',
        'nombre_soporte': 'partner',
        'nombre_campania': 'verano_2024',
        'nombre_ubicacion': 'ROS',
        'nombre_banner': 'crea1',
        'formato_banner': '300x250',
        'url_destino': 'https://www.cliente.com?param=example'
    }
    urls = generator.generate_urls(params)
    assert len(urls) == 3
    assert 'https://aaa1.cliente.com/dynclick/cliente-com/' in urls[0]