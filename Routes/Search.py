"""
The entrypoint for the Search Portal.

Link:
    https://omnitechbros.ddns.net:591/Search
    http://omnitechbros.ddns.net:5000/Search
"""
from flask import Blueprint, Response, render_template, request, Request
from Models.SecurityManagementSystem import Security_Management_System, Union, Environment
from urllib.parse import urlparse, ParseResult


Search_Portal: Blueprint = Blueprint("Search", __name__)
"""
The Routing for all the Searches.
"""
SecurityManagementSystem: Security_Management_System = Security_Management_System()
"""
It will be a major component that will assure the security of the data that will be stored across the application.
"""
ENV: Environment = Environment()
"""
ENV File of the application
"""

@Search_Portal.before_request
def before_request() -> None:
    """
    Preparing the data before the request is made.

    Returns:
        void
    """
    SecurityManagementSystem.generateNonce()


@Search_Portal.route('/<string:identifier>', methods=['GET'])
def searchPage(identifier: str) -> Response:
    """
    Rendering the template needed which will import the
    web-worker.

    Parameters:
        identifier (string): Identifier of the media content to be searched.

    Returns:
        Response
    """
    is_embedded: bool = isEmbeddedRequest(request)
    status: int = 403 if is_embedded else 200
    mime_type: str = "text/html"
    if is_embedded:
        return Response(
            response="Forbidden",
            status=status,
            mimetype=mime_type
        )
    nonce: str = SecurityManagementSystem.getNonce()
    template = render_template(
        template_name_or_list="Search.html",
        nonce=nonce,
    )
    content_security_policy: str = "; ".join([
        "default-src 'self'",
        f"script-src 'self' 'nonce-{nonce}' https://cdnjs.cloudflare.com",
        "style-src 'self' https://fonts.cdnfonts.com https://cdnjs.cloudflare.com",
        "img-src 'self' data: https://i.ytimg.com",
        "font-src 'self' https://fonts.cdnfonts.com https://cdnjs.cloudflare.com",
        "connect-src 'self'",
        "frame-src 'none'",
        "object-src 'none'",
        "base-uri 'self'",
        "form-action 'self'"
    ])
    response: Response = Response(
        response=template,
        status=status,
        mimetype=mime_type
    )
    response.cache_control.max_age = 604800
    response.cache_control.no_cache = False  # type: ignore
    response.cache_control.public = True
    response.content_security_policy = content_security_policy
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    return response

def isEmbeddedRequest(request: Request) -> bool:
    """
    Checks if the request is an embedded request.

    Parameters:
        request (Request): The request object.

    Returns:
        boolean
    """
    referrer: Union[str, None] = request.headers.get("Referer")
    origin: Union[str, None] = request.headers.get("Origin")
    if referrer:
        parsed_referrer: ParseResult = urlparse(referrer)
        referrer_domain: str = f"{parsed_referrer.scheme}://{parsed_referrer.netloc}"
        if referrer_domain not in ENV.getAllowedOrigins():
            return True
    if origin and origin not in ENV.getAllowedOrigins():
        return True
    return False

@Search_Portal.route("/Shorts/<string:identifier>", methods=['GET'])
def searchShortsPage(identifier: str) -> Response:
    """
    Rendering the template needed which will import the web-worker.

    Parameters:
        identifier (string): Identifier of the media content to be searched.

    Returns:
        Response
    """
    is_embedded: bool = isEmbeddedRequest(request)
    status: int = 403 if is_embedded else 200
    mime_type: str = "text/html"
    if is_embedded:
        return Response(
            response="Forbidden",
            status=status,
            mimetype=mime_type
        )
    nonce: str = SecurityManagementSystem.getNonce()
    template = render_template(
        template_name_or_list="Search.html",
        nonce=nonce,
    )
    content_security_policy: str = "; ".join([
        "default-src 'self'",
        f"script-src 'self' 'nonce-{nonce}' https://cdnjs.cloudflare.com",
        "style-src 'self' https://fonts.cdnfonts.com https://cdnjs.cloudflare.com",
        "img-src 'self' data: https://i.ytimg.com",
        "font-src 'self' https://fonts.cdnfonts.com https://cdnjs.cloudflare.com",
        "connect-src 'self'",
        "frame-src 'none'",
        "object-src 'none'",
        "base-uri 'self'",
        "form-action 'self'"
    ])
    response: Response = Response(
        response=template,
        status=status,
        mimetype=mime_type
    )
    response.cache_control.max_age = 604800
    response.cache_control.no_cache = False  # type: ignore
    response.cache_control.public = True
    response.content_security_policy = content_security_policy
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    return response
