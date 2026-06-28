class Signal:
    """Signal model for trading signals"""
    
    def __init__(self, db):
        self.db = db
    
    def create_signal(self, strategy_id, instrument_id, signal_type, entry_price, stop_loss, take_profit, confidence_score, reasoning, expires_at):
        """Create a new signal"""
        query = """
        INSERT INTO signals (strategy_id, instrument_id, signal_type, entry_price, stop_loss, take_profit, confidence_score, reasoning, expires_at, status)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING id, generated_at
        """
        
        result = self.db.execute(query, (
            strategy_id,
            instrument_id,
            signal_type,
            entry_price,
            stop_loss,
            take_profit,
            confidence_score,
            reasoning,
            expires_at,
            'active'
        ))
        
        return dict(result) if result else None
    
    def get_signals(self, instrument_id=None, strategy_id=None, status='active', limit=None):
        """Get signals with filters"""
        query = "SELECT s.*, i.symbol, i.name as instrument_name, st.name as strategy_name FROM signals s JOIN instruments i ON s.instrument_id = i.id JOIN strategies st ON s.strategy_id = st.id WHERE 1=1"
        params = []
        
        if instrument_id:
            query += " AND s.instrument_id = %s"
            params.append(instrument_id)
        
        if strategy_id:
            query += " AND s.strategy_id = %s"
            params.append(strategy_id)
        
        if status:
            query += " AND s.status = %s"
            params.append(status)
        
        query += " ORDER BY s.generated_at DESC"
        
        if limit:
            query += f" LIMIT {limit}"
        
        results = self.db.execute(query, params)
        return [dict(r) for r in results] if results else []
    
    def get_signal_by_id(self, signal_id):
        """Get signal by ID"""
        query = """
        SELECT s.*, i.symbol, i.name as instrument_name, st.name as strategy_name 
        FROM signals s 
        JOIN instruments i ON s.instrument_id = i.id 
        JOIN strategies st ON s.strategy_id = st.id 
        WHERE s.id = %s
        """
        result = self.db.execute(query, (signal_id,))
        return dict(result) if result else None
    
    def update_signal_status(self, signal_id, status):
        """Update signal status"""
        query = "UPDATE signals SET status = %s WHERE id = %s"
        self.db.execute(query, (status, signal_id))
        return True
    
    def expire_old_signals(self):
        """Mark expired signals"""
        query = "UPDATE signals SET status = 'expired' WHERE status = 'active' AND expires_at < CURRENT_TIMESTAMP"
        self.db.execute(query)
        return True
