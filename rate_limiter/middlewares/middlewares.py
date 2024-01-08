import redis
from django.conf import settings

from django.http import HttpResponseForbidden

MAX_REQUESTS_PER_MINUTE = 5


class RateLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.redis_client = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)

    def __call__(self, request):
        if request.user.is_authenticated:
            user_id = request.user.id
            redis_key = f"ratelimit:{user_id}"

            current_requests = self.redis_client.incr(redis_key)
            self.redis_client.expire(redis_key, 60)

            if current_requests > MAX_REQUESTS_PER_MINUTE:
                return HttpResponseForbidden("Rate Limit Exceeded")
        else:
            print("No rate limiting is applicable")

        response = self.get_response(request)
        return response
