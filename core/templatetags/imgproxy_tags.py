from django import template
from django.conf import settings
import base64

register = template.Library()

DOCKER_MEDIA_BASE = "http://web:8000"  # imgproxy reaches Django via docker network

@register.simple_tag
def imgproxy(path_or_url, width=700, height=348):
    src = (path_or_url or "").strip()

    if not src:
        return ""

    # If it's a Django media path like "/media/..."
    if src.startswith("/media/"):
        src = DOCKER_MEDIA_BASE + src
    elif src.startswith("/"):
        src = DOCKER_MEDIA_BASE + src

    # Replace localhost with docker service name
    src = src.replace("http://localhost:8000", DOCKER_MEDIA_BASE)
    src = src.replace("https://localhost:8000", DOCKER_MEDIA_BASE)

    # Base64url encode the source URL (imgproxy requires this)
    encoded_url = base64.urlsafe_b64encode(src.encode()).decode()
    # Remove padding (imgproxy doesn't like padding)
    encoded_url = encoded_url.rstrip('=')

    # Build imgproxy URL
    # Format: /{processing_options}/{encoded_url}.{extension}
    processing = f"resize:fill:{width}:{height}/format:webp/quality:80"

    return f"{settings.IMGPROXY_BASE}/{processing}/{encoded_url}.webp"