# url_generator/display.py

from pytrackeres.url_generator.core import URLGeneratorBase

class DisplayURLGenerator(URLGeneratorBase):
    def validate_params(self, params):
        """Valida los parámetros para el canal Display."""
        required_params = ['dominio_tracking', 'sitio', 'nombre_soporte', 'nombre_campania', 
                           'nombre_ubicacion', 'nombre_banner', 'formato_banner', 'url_destino']
        params = {k.strip(): (v.strip() if v is not None else '') for k, v in params.items()}
        
        missing_params = [param for param in required_params if param not in params or not params[param]]
        
        if missing_params:
            raise ValueError(f"Faltan parámetros obligatorios: {', '.join(missing_params)}")

    def adjust_for_special_cases(self, params):
        """Ajusta las URLs para soportes especiales como Google, Amazon y Outbrain."""
        nombre_soporte = params['nombre_soporte'].lower()
        
        if 'google' in nombre_soporte:
            params['nombre_soporte'] = 'google-ads'
            params['domain_prefix'] = 'https://ew3.io/c/a/'
            params['domain_prefix_impression'] = 'https://ew3.io/v/a/'
        elif 'amazon' in nombre_soporte:
            params['nombre_soporte'] = 'Amazon'
            params['domain_prefix'] = 'https://ew3.io/c/a/'
            params['domain_prefix_impression'] = 'https://ew3.io/v/a/'
        elif 'outbrain' in nombre_soporte:
            params['nombre_soporte'] = 'Outbrain'
            params['domain_prefix'] = 'https://ew3.io/c/a/'
            params['domain_prefix_impression'] = 'https://ew3.io/v/a/'
        else:
            # Usar el dominio de tracking normal si no es uno de los casos especiales
            params['domain_prefix'] = f"https://{params['dominio_tracking']}/dynclick/"
            params['domain_prefix_impression'] = f"https://{params['dominio_tracking']}/dynview/"
        
        return params

    def generate_urls(self, params):
        """Genera las URLs para el canal Display."""
        params = {k.strip(): (v.strip() if v is not None else '') for k, v in params.items()}
        
        # Ajustar para Google, Amazon o Outbrain si es necesario
        params = self.adjust_for_special_cases(params)

        # Click URL (redirect)
        url_click_redirect = (
            f"{params['domain_prefix']}{params['sitio']}/?"
            f"ead-publisher={params['nombre_soporte']}&ead-name={params['nombre_soporte']}-{params['nombre_campania']}&"
            f"ead-location={params['nombre_ubicacion']}-{params['formato_banner']}&ead-creative={params['nombre_banner']}-{params['formato_banner']}&"
            f"ead-creativetype={params['formato_banner']}&eseg-name={params.get('nombre_segmento', '')}&eseg-item={params.get('valor_segmento', '')}&"
            f"ead-mediaplan={params.get('nombre_plan_medios', '')}&ea-android-adid={params.get('adid', '')}&ea-ios-idfa={params.get('idfa', '')}&"
            f"eurl={self.encode_url(params['url_destino'])}"
        )
        
        # Impression URL
        url_impression = (
            f'<img src="{params["domain_prefix_impression"]}{params["sitio"]}/1x1.b?'
            f"ead-publisher={params['nombre_soporte']}&ead-name={params['nombre_soporte']}-{params['nombre_campania']}&"
            f"ead-location={params['nombre_ubicacion']}-{params['formato_banner']}&ead-creative={params['nombre_banner']}-{params['formato_banner']}&"
            f"ead-creativetype={params['formato_banner']}&eseg-name={params.get('nombre_segmento', '')}&eseg-item={params.get('valor_segmento', '')}&"
            f"ead-mediaplan={params.get('nombre_plan_medios', '')}&ea-android-adid={params.get('adid', '')}&ea-ios-idfa={params.get('idfa', '')}&"
            f'ea-rnd=[RANDOM]" border="0" width="1" height="1" />'
        )
        
        # Click URL (parameter tracking)
        url_click_params = (
            f"{params['url_destino']}?ead-publisher={params['nombre_soporte']}&"
            f"ead-name={params['nombre_soporte']}-{params['nombre_campania']}&ead-location={params['nombre_ubicacion']}-{params['formato_banner']}&"
            f"ead-creative={params['nombre_banner']}-{params['formato_banner']}&ead-creativetype={params['formato_banner']}&"
            f"eseg-name={params.get('nombre_segmento', '')}&eseg-item={params.get('valor_segmento', '')}&"
            f"ead-mediaplan={params.get('nombre_plan_medios', '')}&ea-android-adid={params.get('adid', '')}&ea-ios-idfa={params.get('idfa', '')}"
        )
        
        return url_click_redirect, url_impression, url_click_params