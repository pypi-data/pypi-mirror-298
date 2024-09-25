# url_generator/bing_ads.py

from pytrackeres.url_generator.core import URLGeneratorBase

class BingAdsURLGenerator(URLGeneratorBase):
    def validate_params(self, params):
        """Valida los parámetros para el canal Links patrocinados Bing Ads."""
        required_params = ['dominio_tracking', 'sitio', 'nombre_soporte', 'nombre_campania',
                           'nombre_ubicacion', 'nombre_banner', 'formato_banner', 'url_destino']
        params = {k.strip(): (v.strip() if v is not None else '') for k, v in params.items()}
        
        missing_params = [param for param in required_params if param not in params or not params[param]]
        
        if missing_params:
            raise ValueError(f"Faltan parámetros obligatorios: {', '.join(missing_params)}")

    def generate_urls(self, params):
        """Genera las URLs para el canal Bing Ads."""
        params = {k.strip(): (v.strip() if v is not None else '') for k, v in params.items()}

        # Click URL (redirección)
        url_click_redirect = (
            f"https://{params['dominio_tracking']}/dynclick/{params['sitio']}/?"
            f"bingad-publisher={params['nombre_soporte']}&bingad-name={params['nombre_soporte']}-{params['nombre_campania']}&"
            f"bingad-location={params['nombre_ubicacion']}-{params['formato_banner']}&bingad-creative={params['nombre_banner']}-{params['formato_banner']}&"
            f"bingad-creativetype={params['formato_banner']}&eseg-name={params.get('nombre_segmento', '')}&eseg-item={params.get('valor_segmento', '')}&"
            f"bingad-mediaplan={params.get('nombre_plan_medios', '')}&ea-android-adid={params.get('adid', '')}&ea-ios-idfa={params.get('idfa', '')}&"
            f"eurl={self.encode_url(params['url_destino'])}"
        )
        
        # Impression URL
        url_impression = (
            f'<img src="https://{params["dominio_tracking"]}/dynview/{params["sitio"]}/1x1.b?'
            f"bingad-publisher={params['nombre_soporte']}&bingad-name={params['nombre_soporte']}-{params['nombre_campania']}&"
            f"bingad-location={params['nombre_ubicacion']}-{params['formato_banner']}&bingad-creative={params['nombre_banner']}-{params['formato_banner']}&"
            f"bingad-creativetype={params['formato_banner']}&eseg-name={params.get('nombre_segmento', '')}&eseg-item={params.get('valor_segmento', '')}&"
            f"bingad-mediaplan={params.get('nombre_plan_medios', '')}&ea-android-adid={params.get('adid', '')}&ea-ios-idfa={params.get('idfa', '')}&"
            f'ea-rnd=[RANDOM]" border="0" width="1" height="1" />'
        )
        
        # Click URL (parameter tracking)
        url_click_params = (
            f"{params['url_destino']}?bingad-publisher={params['nombre_soporte']}&"
            f"bingad-name={params['nombre_soporte']}-{params['nombre_campania']}&bingad-location={params['nombre_ubicacion']}-{params['formato_banner']}&"
            f"bingad-creative={params['nombre_banner']}-{params['formato_banner']}&bingad-creativetype={params['formato_banner']}&"
            f"eseg-name={params.get('nombre_segmento', '')}&eseg-item={params.get('valor_segmento', '')}&"
            f"bingad-mediaplan={params.get('nombre_plan_medios', '')}&ea-android-adid={params.get('adid', '')}&ea-ios-idfa={params.get('idfa', '')}"
        )
        
        return url_click_redirect, url_impression, url_click_params