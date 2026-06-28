import psycopg2
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager
import os

class Database:
    """Database connection manager"""
    
    def __init__(self, database_url=None):
        self.database_url = database_url or os.getenv('DATABASE_URL', 'postgresql://localhost/trading_platform')
        self.connection = None
    
    def connect(self):
        """Establish database connection"""
        if self.connection is None:
            self.connection = psycopg2.connect(self.database_url, cursor_factory=RealDictCursor)
        return self.connection
    
    def close(self):
        """Close database connection"""
        if self.connection is not None:
            self.connection.close()
            self.connection = None
    
    @contextmanager
    def get_cursor(self):
        """Context manager for database cursor"""
        conn = self.connect()
        cursor = conn.cursor()
        try:
            yield cursor
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
    
    def execute(self, query, params=None):
        """Execute a query and return results"""
        with self.get_cursor() as cursor:
            cursor.execute(query, params or ())
            if cursor.description:
                return cursor.fetchall()
            return cursor.rowcount
    
    def execute_many(self, query, params_list):
        """Execute a query multiple times"""
        with self.get_cursor() as cursor:
            cursor.executemany(query, params_list)
            return cursor.rowcount

# Global database instance
db = Database()
