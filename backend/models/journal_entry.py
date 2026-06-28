class JournalEntry:
    """Journal entry model for trade notes and insights"""
    
    def __init__(self, db):
        self.db = db
    
    def create_entry(self, user_id, notes, entry_type='general', trade_id=None, mood=None, tags=None):
        """Create a new journal entry"""
        query = """
        INSERT INTO journal_entries (user_id, trade_id, entry_type, notes, mood, tags)
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING id, created_at
        """
        
        result = self.db.execute(query, (
            user_id,
            trade_id,
            entry_type,
            notes,
            mood,
            tags or []
        ))
        
        return dict(result) if result else None
    
    def get_entry_by_id(self, entry_id, user_id):
        """Get journal entry by ID"""
        query = """
        SELECT je.*, t.id as trade_id, i.symbol as instrument_symbol 
        FROM journal_entries je 
        LEFT JOIN trades t ON je.trade_id = t.id 
        LEFT JOIN instruments i ON t.instrument_id = i.id 
        WHERE je.id = %s AND je.user_id = %s
        """
        result = self.db.execute(query, (entry_id, user_id))
        return dict(result) if result else None
    
    def get_user_entries(self, user_id, entry_type=None, trade_id=None, limit=None, offset=0):
        """Get user's journal entries"""
        query = """
        SELECT je.*, t.id as trade_id, i.symbol as instrument_symbol 
        FROM journal_entries je 
        LEFT JOIN trades t ON je.trade_id = t.id 
        LEFT JOIN instruments i ON t.instrument_id = i.id 
        WHERE je.user_id = %s
        """
        params = [user_id]
        
        if entry_type:
            query += " AND je.entry_type = %s"
            params.append(entry_type)
        
        if trade_id:
            query += " AND je.trade_id = %s"
            params.append(trade_id)
        
        query += " ORDER BY je.created_at DESC"
        
        if limit:
            query += f" LIMIT {limit}"
        if offset:
            query += f" OFFSET {offset}"
        
        results = self.db.execute(query, params)
        return [dict(r) for r in results] if results else []
    
    def update_entry(self, entry_id, user_id, updates):
        """Update journal entry"""
        allowed_fields = ['notes', 'mood', 'tags']
        set_clauses = []
        values = []
        
        for field, value in updates.items():
            if field in allowed_fields:
                if isinstance(value, list):
                    set_clauses.append(f"{field} = %s::jsonb")
                else:
                    set_clauses.append(f"{field} = %s")
                values.append(value)
        
        if not set_clauses:
            return False
        
        values.append(entry_id)
        values.append(user_id)
        query = f"UPDATE journal_entries SET {', '.join(set_clauses)}, updated_at = CURRENT_TIMESTAMP WHERE id = %s AND user_id = %s"
        
        self.db.execute(query, values)
        return True
    
    def delete_entry(self, entry_id, user_id):
        """Delete journal entry"""
        query = "DELETE FROM journal_entries WHERE id = %s AND user_id = %s"
        self.db.execute(query, (entry_id, user_id))
        return True
