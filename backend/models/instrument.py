class Instrument:
    """Instrument model for stocks, indices"""
    
    def __init__(self, db):
        self.db = db
    
    def get_all_instruments(self, active_only=True, limit=None):
        """Get all instruments"""
        query = "SELECT * FROM instruments"
        if active_only:
            query += " WHERE is_active = TRUE"
        query += " ORDER BY symbol"
        if limit:
            query += f" LIMIT {limit}"
        
        results = self.db.execute(query)
        return [dict(r) for r in results] if results else []
    
    def get_instrument_by_symbol(self, symbol):
        """Get instrument by symbol"""
        query = "SELECT * FROM instruments WHERE symbol = %s"
        result = self.db.execute(query, (symbol,))
        return dict(result) if result else None
    
    def get_instrument_by_id(self, instrument_id):
        """Get instrument by ID"""
        query = "SELECT * FROM instruments WHERE id = %s"
        result = self.db.execute(query, (instrument_id,))
        return dict(result) if result else None
    
    def get_instruments_by_exchange(self, exchange_id, active_only=True):
        """Get instruments by exchange"""
        query = "SELECT * FROM instruments WHERE exchange_id = %s"
        if active_only:
            query += " AND is_active = TRUE"
        query += " ORDER BY symbol"
        
        results = self.db.execute(query, (exchange_id,))
        return [dict(r) for r in results] if results else []
    
    def get_top_n_instruments(self, n=50):
        """Get top N instruments by volume (for MVP, just returns first N active)"""
        query = """
        SELECT i.* FROM instruments i
        WHERE i.is_active = TRUE
        ORDER BY i.symbol
        LIMIT %s
        """
        results = self.db.execute(query, (n,))
        return [dict(r) for r in results] if results else []
