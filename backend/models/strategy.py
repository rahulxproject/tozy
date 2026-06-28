class Strategy:
    """Strategy model for trading strategies"""
    
    def __init__(self, db):
        self.db = db
    
    def get_all_strategies(self, user_id=None, active_only=True, system_only=False):
        """Get all strategies"""
        query = "SELECT * FROM strategies WHERE 1=1"
        params = []
        
        if user_id:
            query += " AND (user_id = %s OR is_system = TRUE)"
            params.append(user_id)
        
        if active_only:
            query += " AND is_active = TRUE"
        
        if system_only:
            query += " AND is_system = TRUE"
        
        query += " ORDER BY name"
        
        results = self.db.execute(query, params)
        return [dict(r) for r in results] if results else []
    
    def get_strategy_by_id(self, strategy_id):
        """Get strategy by ID"""
        query = "SELECT * FROM strategies WHERE id = %s"
        result = self.db.execute(query, (strategy_id,))
        return dict(result) if result else None
    
    def create_strategy(self, user_id, name, description, entry_conditions, exit_conditions, risk_parameters, timeframe, instrument_filters=None):
        """Create a new custom strategy"""
        query = """
        INSERT INTO strategies (name, description, user_id, is_system, entry_conditions, exit_conditions, risk_parameters, timeframe, instrument_filters, is_active)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING id, name, created_at
        """
        
        result = self.db.execute(query, (
            name,
            description,
            user_id,
            False,  # is_system
            entry_conditions,
            exit_conditions,
            risk_parameters,
            timeframe,
            instrument_filters or {},
            True   # is_active
        ))
        
        return dict(result) if result else None
    
    def update_strategy(self, strategy_id, updates):
        """Update strategy"""
        allowed_fields = ['name', 'description', 'entry_conditions', 'exit_conditions', 'risk_parameters', 'timeframe', 'instrument_filters', 'is_active']
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
        
        values.append(strategy_id)
        query = f"UPDATE strategies SET {', '.join(set_clauses)}, updated_at = CURRENT_TIMESTAMP WHERE id = %s"
        
        self.db.execute(query, values)
        return True
    
    def delete_strategy(self, strategy_id, user_id):
        """Delete a custom strategy (only if user owns it)"""
        query = "DELETE FROM strategies WHERE id = %s AND user_id = %s AND is_system = FALSE"
        self.db.execute(query, (strategy_id, user_id))
        return True
