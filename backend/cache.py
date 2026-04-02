"""
Redis Cache Manager for API Optimization

Provides caching utilities for frequently accessed endpoints with configurable
TTL (Time-To-Live) and cache invalidation strategies.
"""

import redis
import json
import hashlib
import os
from functools import wraps
from flask import request, current_app
from flask_jwt_extended import get_jwt_identity

# Redis client instance
redis_client = None

def init_redis(app):
    """Initialize Redis client with Flask app config."""
    global redis_client
    try:
        # Get Redis config from environment or use defaults
        redis_host = os.getenv("REDIS_HOST", "localhost")
        redis_port = int(os.getenv("REDIS_PORT", 6379))
        redis_db = int(os.getenv("REDIS_DB", 0))
        redis_password = os.getenv("REDIS_PASSWORD", None)
        
        redis_client = redis.Redis(
            host=redis_host,
            port=redis_port,
            db=redis_db,
            password=redis_password,
            decode_responses=True,
            socket_connect_timeout=5
        )
        
        # Test connection
        redis_client.ping()
        print("✅ Redis Cache Connected Successfully")
        app.config['REDIS_ENABLED'] = True
        return redis_client
    except Exception as e:
        print(f"⚠️  Redis Connection Failed: {e}")
        print("   API will run without caching")
        redis_client = None
        app.config['REDIS_ENABLED'] = False
        return None

def is_redis_available():
    """Check if Redis is available and connected."""
    return redis_client is not None

def generate_cache_key(prefix, **kwargs):
    """
    Generate a cache key from prefix and parameters.
    
    Args:
        prefix: Cache key prefix (e.g., 'available_slots', 'search')
        **kwargs: Additional parameters to include in key
    
    Returns:
        str: Generated cache key
    """
    key_parts = [prefix]
    
    # Add request query parameters
    if request.args:
        # Sort query params for consistency
        sorted_params = sorted(request.args.items())
        param_str = json.dumps(sorted_params)
        param_hash = hashlib.md5(param_str.encode()).hexdigest()[:8]
        key_parts.append(f"params_{param_hash}")
    
    # Add additional kwargs
    for k, v in sorted(kwargs.items()):
        if v is not None:
            key_parts.append(f"{k}_{v}")
    
    return ":".join(key_parts)

def cache_response(ttl=300, prefix=None, user_specific=False):
    """
    Decorator to cache Flask-RESTful resource responses.
    
    Args:
        ttl: Time-to-live in seconds (default: 5 minutes)
        prefix: Cache key prefix (auto-generated from function name if None)
        user_specific: If True, cache is per-user (default: False for public data)
    
    Usage:
        @cache_response(ttl=600, prefix='available_slots')
        def get(self):
            ...
    """
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            # Skip caching if Redis is unavailable
            if not is_redis_available():
                return func(self, *args, **kwargs)
            
            # Generate cache key
            cache_prefix = prefix or func.__name__
            cache_key_kwargs = {}
            
            if user_specific:
                try:
                    email = get_jwt_identity()
                    cache_key_kwargs['user'] = email
                except:
                    pass
            
            cache_key = generate_cache_key(cache_prefix, **cache_key_kwargs)
            
            try:
                # Try to get from cache
                cached = redis_client.get(cache_key)
                if cached:
                    print(f"📦 Cache HIT: {cache_key}")
                    return json.loads(cached)
            except Exception as e:
                print(f"⚠️  Cache GET error: {e}")
            
            # Call original function
            result = func(self, *args, **kwargs)
            
            # Cache the response
            try:
                redis_client.setex(
                    cache_key,
                    ttl,
                    json.dumps(result)
                )
                print(f"💾 Cached: {cache_key} (TTL: {ttl}s)")
            except Exception as e:
                print(f"⚠️  Cache SET error: {e}")
            
            return result
        
        return wrapper
    return decorator

def invalidate_cache(pattern):
    """
    Invalidate cache entries matching a pattern.
    
    Args:
        pattern: Redis key pattern (e.g., 'available_slots:*')
    
    Example:
        invalidate_cache('available_slots:*')
    """
    if not is_redis_available():
        return
    
    try:
        keys = redis_client.keys(pattern)
        if keys:
            redis_client.delete(*keys)
            print(f"🗑️  Invalidated {len(keys)} cache entries matching: {pattern}")
    except Exception as e:
        print(f"⚠️  Cache invalidation error: {e}")

def invalidate_user_cache(user_email, pattern_prefix='*'):
    """
    Invalidate all cache entries for a specific user.
    
    Args:
        user_email: User email identifier
        pattern_prefix: Prefix of cache keys to invalidate
    """
    if not is_redis_available():
        return
    
    pattern = f"{pattern_prefix}*user_{user_email}*"
    invalidate_cache(pattern)

def clear_all_cache():
    """Clear all cache from Redis (use with caution)."""
    if not is_redis_available():
        return
    
    try:
        redis_client.flushdb()
        print("🗑️  All cache cleared")
    except Exception as e:
        print(f"⚠️  Cache clear error: {e}")

def get_cache_stats():
    """Get Redis cache statistics."""
    if not is_redis_available():
        return {"status": "Redis not available"}
    
    try:
        info = redis_client.info('stats')
        dbsize = redis_client.dbsize()
        
        return {
            "status": "connected",
            "total_commands": info.get('total_commands_processed', 0),
            "cached_items": dbsize,
            "memory_usage": info.get('used_memory_human', 'N/A')
        }
    except Exception as e:
        return {"status": "error", "error": str(e)}
