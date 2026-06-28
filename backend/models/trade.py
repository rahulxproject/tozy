class Trade:
    """Trade model for user trades"""
    
    def __init__(self, db):
        self.db = db
    
    def create_trade(self, user_id, instrument_id, trade_type, entry_price, quantity, entry_date, stop_loss=None, take_profit=None, setup_type=None, notes=None, signal_id=None):
        """Create a new trade"""
        query = """
        INSERT INTO trades (user_id, instrument_id, signal_id, trade_type, entry_price, quantity, entry_date, stop_loss, take_profit, setup_type, notes, status)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING id, created_at
        """
        
        result = self.db.execute(query, (
            user_id,
            instrument_id,
            signal_id,
            trade_type,
            entry_price,
            quantity,
            entry_date,
            stop_loss,
            take_profit,
            setup_type,
            notes,
            'open'
        ))
        
        return dict(result) if result else None
    
    def get_trade_by_id(self, trade_id, user_id):
        """Get trade by ID (user-specific)"""
        query = """
        SELECT t.*, i.symbol, i.name as instrument_name 
        FROM trades t 
        JOIN instruments i ON t.instrument_id = i.id 
        WHERE t.id = %s AND t.user_id = %s
        """
        result = self.db.execute(query, (trade_id, user_id))
        return dict(result) if result else None
    
    def get_user_trades(self, user_id, status=None, instrument_id=None, limit=None, offset=0):
        """Get user's trades with filters"""
        query = """
        SELECT t.*, i.symbol, i.name as instrument_name 
        FROM trades t 
        JOIN instruments i ON t.instrument_id = i.id 
        WHERE t.user_id = %s
        """
        params = [user_id]
        
        if status:
            query += " AND t.status = %s"
            params.append(status)
        
        if instrument_id:
            query += " AND t.instrument_id = %s"
            params.append(instrument_id)
        
        query += " ORDER BY t.entry_date DESC"
        
        if limit:
            query += f" LIMIT {limit}"
        if offset:
            query += f" OFFSET {offset}"
        
        results = self.db.execute(query, params)
        return [dict(r) for r in results] if results else []
    
    def update_trade(self, trade_id, user_id, updates):
        """Update trade"""
        allowed_fields = ['exit_price', 'exit_date', 'stop_loss', 'take_profit', 'setup_type', 'notes', 'mistake_tags', 'status']
        set_clauses = []
        values = []
        
        for field, value in updates.items():
            if field in allowed_fields:
                if isinstance(value, dict):
                    set_clauses.append(f"{field} = %s::jsonb")
                else:
                    set_clauses.append(f"{field} = %s")
                values.append(value)
        
        if not set_clauses:
            return False
        
        # Calculate P/L if exit price is provided
        if 'exit_price' in updates:
            set_clauses.append("pnl = (exit_price - entry_price) * quantity")
            set_clauses.append("pnl_percentage = ((exit_price - entry_price) / entry_price) * 100")
        
        values.append(trade_id)
        values.append(user_id)
        query = f"UPDATE trades SET {', '.join(set_clauses)}, updated_at = CURRENT_TIMESTAMP WHERE id = %s AND user_id = %s"
        
        self.db.execute(query, values)
        return True
    
    def close_trade(self, trade_id, user_id, exit_price, exit_date):
        """Close a trade"""
        updates = {
            'exit_price': exit_price,
            'exit_date': exit_date,
            'status': 'closed'
        }
        return self.update_trade(trade_id, user_id, updates)
    
    def get_user_performance(self, user_id):
        """Get user's performance metrics"""
        query = """
        SELECT 
            COUNT(*) as total_trades,
            COUNT(CASE WHEN status = 'closed' THEN 1 END) as closed_trades,
            COUNT(CASE WHEN status = 'closed' AND pnl > 0 THEN 1 END) as winning_trades,
            COUNT(CASE WHEN status = 'closed' AND pnl < 0 THEN 1 END) as losing_trades,
            COALESCE(SUM(CASE WHEN status = 'closed' THEN pnl END), 0) as total_pnl,
            COALESCE(AVG(CASE WHEN status = 'closed' AND pnl > 0 THEN pnl END), 0) as avg_win,
            COALESCE(AVG(CASE WHEN status = 'closed' AND pnl < 0 THEN pnl END), 0) as avg_loss
        FROM trades 
        WHERE user_id = %s
        """
        result = self.db.execute(query, (user_id,))
        return dict(result) if result else {}
