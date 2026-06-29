import redis
import json
import os
from datetime import timedelta

class CacheManager:
    """Redis-based cache manager for historical data and computed indicators"""
    
    def __init__(self):
        self.redis_client = redis.Redis(
            host=os.getenv('REDIS_HOST', 'localhost'),
            port=int(os.getenv('REDIS_PORT', 6379)),
            db=int(os.getenv('REDIS_DB', 0)),
            decode_responses=True
        )
    
    def _make_key(self, prefix, *parts):
        """Generate a cache key from parts"""
        return f"{prefix}:{':'.join(str(p) for p in parts)}"
    
    def get_ohlcv_data(self, instrument_id, timeframe, limit):
        """Get cached OHLCV data"""
        key = self._make_key('ohlcv', instrument_id, timeframe, limit)
        cached = self.redis_client.get(key)
        
        if cached:
            return json.loads(cached)
        return None
    
    def set_ohlcv_data(self, instrument_id, timeframe, limit, data, ttl=3600):
        """Cache OHLCV data with TTL (default 1 hour)"""
        key = self._make_key('ohlcv', instrument_id, timeframe, limit)
        self.redis_client.setex(key, ttl, json.dumps(data))
    
    def get_indicators(self, instrument_id, timeframe, indicator_type):
        """Get cached indicator data"""
        key = self._make_key('indicators', instrument_id, timeframe, indicator_type)
        cached = self.redis_client.get(key)
        
        if cached:
            return json.loads(cached)
        return None
    
    def set_indicators(self, instrument_id, timeframe, indicator_type, data, ttl=1800):
        """Cache indicator data with TTL (default 30 minutes)"""
        key = self._make_key('indicators', instrument_id, timeframe, indicator_type)
        self.redis_client.setex(key, ttl, json.dumps(data))
    
    def get_signal(self, strategy_id, instrument_id):
        """Get cached signal"""
        key = self._make_key('signal', strategy_id, instrument_id)
        cached = self.redis_client.get(key)
        
        if cached:
            return json.loads(cached)
        return None
    
    def set_signal(self, strategy_id, instrument_id, signal_data, ttl=300):
        """Cache signal with TTL (default 5 minutes)"""
        key = self._make_key('signal', strategy_id, instrument_id)
        self.redis_client.setex(key, ttl, json.dumps(signal_data))
    
    def invalidate_instrument(self, instrument_id):
        """Invalidate all cache entries for an instrument"""
        pattern = self._make_key('*', instrument_id, '*')
        keys = self.redis_client.keys(pattern)
        if keys:
            self.redis_client.delete(*keys)
    
    def invalidate_strategy(self, strategy_id):
        """Invalidate all cache entries for a strategy"""
        pattern = self._make_key('signal', strategy_id, '*')
        keys = self.redis_client.keys(pattern)
        if keys:
            self.redis_client.delete(*keys)
    
    def clear_all(self):
        """Clear all cache (use with caution)"""
        self.redis_client.flushdb()
    
    def get_stats(self):
        """Get cache statistics"""
        info = self.redis_client.info('stats')
        return {
            'hits': info.get('keyspace_hits', 0),
            'misses': info.get('keyspace_misses', 0),
            'keys': self.redis_client.dbsize()
        }

# Global cache instance
cache = CacheManager()
