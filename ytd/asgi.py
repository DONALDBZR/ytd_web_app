from asgiref.wsgi import WsgiToAsgi
from index import Application


asgi_app: WsgiToAsgi = WsgiToAsgi(Application)
__all__ = ["asgi_app"]