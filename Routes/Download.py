"""
The entrypoint for the Download Portal.

Link:
    https://omnitechbros.ddns.net:591/Download
    http://omnitechbros.ddns.net:5000/Download
"""
from flask import Blueprint, Response, render_template, request, send_file, Request
from Models.SecurityManagementSystem import Security_Management_System, Union, Environment
from typing import Dict
from urllib.parse import urlparse, ParseResult


Download_Portal: Blueprint = Blueprint("Download", __name__)
"""
The Routing for all the Downloads.
"""
SecurityManagementSystem: Security_Management_System = Security_Management_System()
"""
It will be a major component that will assure the security of the data that will be stored across the application.
"""
ENV: Environment = Environment()
"""
ENV File of the application
"""

@Download_Portal.before_request
def before_request() -> None:
    """
    Preparing the data before the request is made.

    Returns:
        void
    """
    SecurityManagementSystem.generateNonce()

@Download_Portal.route('/YouTube/<string:identifier>', methods=['GET'])
def downloadPage(identifier: str) -> Response:
    """
    Rendering the template needed which will import the
    web-worker.

    Parameters:
        identifier (str): Identifier of the media content to be searched.

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
    template: str = render_template(
        template_name_or_list='Download.html',
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

@Download_Portal.route('/YouTube/Shorts/<string:identifier>', methods=['GET'])
def downloadShortsPage(identifier: str) -> Response:
    """
    Rendering the template needed which will import the web-worker.

    Parameters:
        identifier (str): Identifier of the media content to be searched.

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
    template: str = render_template(
        template_name_or_list='Download.html',
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
    Checking if the request is an embedded request.

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

@Download_Portal.route('/', methods=['POST'])
def downloadFile() -> Response:
    """
    Downloading the file from the file location that is sent
    from the view.

    Returns:
        Response
    """
    request_json: Dict[str, str] = request.json # type: ignore
    file_path: str = request_json['file']
    file_name: str = request_json['file_name']
    mime_type: str = "audio/mp3" if "Audio" in file_path else ""
    mime_type = "video/mp4" if "Video" in file_path else mime_type
    return send_file(
        path_or_file=file_path,
        mimetype=mime_type,
        as_attachment=True,
        download_name=file_name
    )
