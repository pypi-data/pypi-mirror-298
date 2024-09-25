# test/test_display.py

from pytrackeres.url_generator.display import DisplayURLGenerator

def test_generate_urls_display_amazon():
    generator = DisplayURLGenerator("test_file.csv")
    params = {
        'dominio_tracking': 'aaa1.cliente.com',
        'sitio': 'cliente-com',
        'nombre_soporte': 'Amazon',
        'nombre_campania': 'verano_2024',
        'nombre_ubicacion': 'ROS',
        'nombre_banner': 'crea1',
        'formato_banner': '300x250',
        'url_destino': 'https://www.cliente.com?param=example'
    }
    urls = generator.generate_urls(params)
    assert len(urls) == 3
    assert 'https://ew3.io/c/a/cliente-com/' in urls[0]

def test_generate_urls_display_outbrain():
    generator = DisplayURLGenerator("test_file.csv")
    params = {
        'dominio_tracking': 'aaa1.cliente.com',
        'sitio': 'cliente-com',
        'nombre_soporte': 'Outbrain',
        'nombre_campania': 'verano_2024',
        'nombre_ubicacion': 'ROS',
        'nombre_banner': 'crea1',
        'formato_banner': '300x250',
        'url_destino': 'https://www.cliente.com?param=example'
    }
    urls = generator.generate_urls(params)
    assert len(urls) == 3
    assert 'https://ew3.io/c/a/cliente-com/' in urls[0]

def test_generate_urls_display_google_ads():
    generator = DisplayURLGenerator("test_file.csv")
    params = {
        'dominio_tracking': 'aaa1.cliente.com',
        'sitio': 'cliente-com',
        'nombre_soporte': 'google-ads',
        'nombre_campania': 'verano_2024',
        'nombre_ubicacion': 'ROS',
        'nombre_banner': 'crea1',
        'formato_banner': '300x250',
        'url_destino': 'https://www.cliente.com?param=example'
    }
    urls = generator.generate_urls(params)
    assert len(urls) == 3
    assert 'https://ew3.io/c/a/cliente-com/' in urls[0]

def test_generate_urls_display_default():
    generator = DisplayURLGenerator("test_file.csv")
    params = {
        'dominio_tracking': 'aaa1.cliente.com',
        'sitio': 'cliente-com',
        'nombre_soporte': 'generic',
        'nombre_campania': 'verano_2024',
        'nombre_ubicacion': 'ROS',
        'nombre_banner': 'crea1',
        'formato_banner': '300x250',
        'url_destino': 'https://www.cliente.com?param=example'
    }
    urls = generator.generate_urls(params)
    assert len(urls) == 3
    assert 'https://aaa1.cliente.com/dynclick/cliente-com/' in urls[0]