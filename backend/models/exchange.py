class Exchange:
    """Exchange model for NSE, BSE, MCX"""
    
    def __init__(self, db):
        self.db = db
    
    def get_all_exchanges(self):
        """Get all exchanges"""
        query = "SELECT * FROM exchanges ORDER BY code"
        results = self.db.execute(query)
        return [dict(r) for r in results] if results else []
    
    def get_exchange_by_code(self, code):
        """Get exchange by code"""
        query = "SELECT * FROM exchanges WHERE code = %s"
        result = self.db.execute(query, (code,))
        return dict(result) if result else None
    
    def get_exchange_by_id(self, exchange_id):
        """Get exchange by ID"""
        query = "SELECT * FROM exchanges WHERE id = %s"
        result = self.db.execute(query, (exchange_id,))
        return dict(result) if result else None
