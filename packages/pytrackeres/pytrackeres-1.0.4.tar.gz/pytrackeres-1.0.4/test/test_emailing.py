# test/test_emailing.py

from pytrackeres.url_generator.emailing import EmailingURLGenerator

def test_generate_urls_emailing():
    generator = EmailingURLGenerator("test_file.csv")
    params = {
        'dominio_tracking': 'aaa1.cliente.com',
        'sitio': 'cliente-com',
        'nombre_soporte': 'mailchimp',
        'nombre_campania': 'verano_2024',
        'url_destino': 'https://www.cliente.com?param=example'
    }
    urls = generator.generate_urls(params)
    assert len(urls) == 3
    assert 'https://aaa1.cliente.com/dynclick/cliente-com/' in urls[0]