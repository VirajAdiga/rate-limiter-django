import redis
from django.conf import settings

from django.http import HttpResponse

MAX_REQUESTS_PER_MINUTE = 5
RATELIMIT_CACHE_KEY_PREFIX = "ratelimit"


class RateLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.redis_client = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)

    def __call__(self, request):
        # If user is authenticated, use user id
        if request.user.is_authenticated:
            user_id = request.user.id
            redis_key = f"{RATELIMIT_CACHE_KEY_PREFIX}:{user_id}"
        else:
            # If user is not authenticated
            # Get IP address from the request
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip = x_forwarded_for.split(',')[0]  # If user is behind proxy
            else:
                ip = request.META.get('REMOTE_ADDR')  # If not behind a proxy, get direct IP
            redis_key = f"{RATELIMIT_CACHE_KEY_PREFIX}:{ip}"

        current_requests = self.redis_client.incr(redis_key)
        self.redis_client.expire(redis_key, 60)

        if current_requests > MAX_REQUESTS_PER_MINUTE:
            return HttpResponse("Too many requests! Rate Limit Exceeded", status=429)

        response = self.get_response(request)
        return response
