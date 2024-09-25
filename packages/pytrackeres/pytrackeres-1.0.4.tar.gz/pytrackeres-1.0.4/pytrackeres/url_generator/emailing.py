# url_generator/emailing.py

from pytrackeres.url_generator.core import URLGeneratorBase

class EmailingURLGenerator(URLGeneratorBase):
    def validate_params(self, params):
        """Valida los parámetros para el canal Emailing."""
        required_params = ['dominio_tracking', 'sitio', 'nombre_soporte', 'nombre_campania', 'url_destino']
        params = {k.strip(): (v.strip() if v is not None else '') for k, v in params.items()}
        
        missing_params = [param for param in required_params if param not in params or not params[param]]
        
        if missing_params:
            raise ValueError(f"Faltan parámetros obligatorios: {', '.join(missing_params)}")

    def generate_urls(self, params):
        """Genera las URLs para el canal Emailing."""
        params = {k.strip(): (v.strip() if v is not None else '') for k, v in params.items()}

        # Click URL (redirección)
        url_click_redirect = (
            f"https://{params['dominio_tracking']}/dynclick/{params['sitio']}/?"
            f"eml-publisher={params['nombre_soporte']}&eml-name={params['nombre_soporte']}-{params['nombre_campania']}&"
            f"eseg-name={params.get('nombre_segmento', '')}&eseg-item={params.get('valor_segmento', '')}&"
            f"eml-mediaplan={params.get('nombre_plan_medios', '')}&uid={params.get('id_cliente', '')}&"
            f"ea-android-adid={params.get('adid', '')}&ea-ios-idfa={params.get('idfa', '')}&"
            f"eurl={self.encode_url(params['url_destino'])}"
        )
        
        # Agregar mail_usuario si está presente
        if params.get('mail_usuario'):
            url_click_redirect += f"&eemail={params['mail_usuario']}"
        
        # Impression URL
        url_impression = (
            f'<img src="https://{params["dominio_tracking"]}/dynview/{params["sitio"]}/1x1.b?'
            f"eml-publisher={params['nombre_soporte']}&eml-name={params['nombre_soporte']}-{params['nombre_campania']}&"
            f"eseg-name={params.get('nombre_segmento', '')}&eseg-item={params.get('valor_segmento', '')}&"
            f"eml-mediaplan={params.get('nombre_plan_medios', '')}&uid={params.get('id_cliente', '')}&"
            f"ea-android-adid={params.get('adid', '')}&ea-ios-idfa={params.get('idfa', '')}&ea-rnd=[RANDOM]\" border=\"0\" width=\"1\" height=\"1\" />"
        )
        
        # Click URL (tracking por parámetros)
        url_click_params = (
            f"{params['url_destino']}?eml-publisher={params['nombre_soporte']}&"
            f"eml-name={params['nombre_soporte']}-{params['nombre_campania']}&"
            f"eseg-name={params.get('nombre_segmento', '')}&eseg-item={params.get('valor_segmento', '')}&"
            f"eml-mediaplan={params.get('nombre_plan_medios', '')}&uid={params.get('id_cliente', '')}&"
            f"ea-android-adid={params.get('adid', '')}&ea-ios-idfa={params.get('idfa', '')}"
        )
        
        # Agregar mail_usuario si está presente
        if params.get('mail_usuario'):
            url_click_params += f"&eemail={params['mail_usuario']}"
        
        return url_click_redirect, url_impression, url_click_params