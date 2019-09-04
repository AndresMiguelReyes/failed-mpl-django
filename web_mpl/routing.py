from django.conf.urls import url
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator, OriginValidator

from web_mpl.consumers import MplConsumer

application = ProtocolTypeRouter({
    # Websocket chat handler
    'websocket': AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                [
                url(r"^example/(?P<fig_id>[0-9]+)/$", MplConsumer, name='example')
                # url(r"^messages/(?P<username>[\w.@+-]+)/$", ChatConsumer)
                ]
            )
        ),
    )
})