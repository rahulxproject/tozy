import pandas as pd
from datetime import datetime, timedelta
from database import db
from models.instrument import Instrument

class DataService:
    """Service for fetching and storing EOD market data"""
    
    def __init__(self):
        self.instrument_model = Instrument(db)
    
    def fetch_sample_data(self, symbol, days=252):
        """
        Generate sample EOD data for development/testing.
        In production, this would fetch from NSE official sources or data vendors.
        """
        import numpy as np
        
        # Generate sample price data
        np.random.seed(hash(symbol) % 10000)
        
        base_price = np.random.uniform(100, 5000)
        dates = pd.date_range(end=datetime.now(), periods=days, freq='D')
        dates = dates[dates.dayofweek < 5]  # Remove weekends
        
        data = []
        close = base_price
        
        for date in dates:
            # Random walk for price
            change = np.random.normal(0, 0.02) * close
            high = close + abs(np.random.normal(0, 0.01 * close))
            low = close - abs(np.random.normal(0, 0.01 * close))
            open_price = close + np.random.normal(0, 0.005 * close)
            close = close + change
            volume = int(np.random.uniform(1000000, 50000000))
            
            data.append({
                'date': date.date(),
                'open': round(open_price, 2),
                'high': round(high, 2),
                'low': round(low, 2),
                'close': round(close, 2),
                'volume': volume
            })
        
        return pd.DataFrame(data)
    
    def store_ohlcv_data(self, instrument_id, df, timeframe='1D'):
        """Store OHLCV data in database"""
        records = []
        for _, row in df.iterrows():
            records.append({
                'instrument_id': instrument_id,
                'date': row['date'],
                'timeframe': timeframe,
                'open': row['open'],
                'high': row['high'],
                'low': row['low'],
                'close': row['close'],
                'volume': row['volume']
            })
        
        # Insert or update data
        query = """
        INSERT INTO ohlcv_data (instrument_id, date, timeframe, open, high, low, close, volume)
        VALUES (%(instrument_id)s, %(date)s, %(timeframe)s, %(open)s, %(high)s, %(low)s, %(close)s, %(volume)s)
        ON CONFLICT (instrument_id, date, timeframe) 
        DO UPDATE SET 
            open = EXCLUDED.open,
            high = EXCLUDED.high,
            low = EXCLUDED.low,
            close = EXCLUDED.close,
            volume = EXCLUDED.volume
        """
        
        db.execute_many(query, records)
        return len(records)
    
    def get_ohlcv_data(self, instrument_id, timeframe='1D', start_date=None, end_date=None, limit=None):
        """Retrieve OHLCV data from database"""
        query = """
        SELECT date, open, high, low, close, volume 
        FROM ohlcv_data 
        WHERE instrument_id = %s AND timeframe = %s
        """
        params = [instrument_id, timeframe]
        
        if start_date:
            query += " AND date >= %s"
            params.append(start_date)
        
        if end_date:
            query += " AND date <= %s"
            params.append(end_date)
        
        query += " ORDER BY date ASC"
        
        if limit:
            query += f" LIMIT {limit}"
        
        results = db.execute(query, params)
        return pd.DataFrame([dict(r) for r in results]) if results else pd.DataFrame()
    
    def update_all_instruments(self, days=252):
        """Update data for all active instruments"""
        instruments = self.instrument_model.get_all_instruments(active_only=True)
        
        total_updated = 0
        for instrument in instruments:
            try:
                df = self.fetch_sample_data(instrument['symbol'], days)
                count = self.store_ohlcv_data(instrument['id'], df)
                total_updated += count
                print(f"Updated {instrument['symbol']}: {count} records")
            except Exception as e:
                print(f"Error updating {instrument['symbol']}: {e}")
        
        return total_updated
    
    def update_single_instrument(self, symbol, days=252):
        """Update data for a single instrument"""
        instrument = self.instrument_model.get_instrument_by_symbol(symbol)
        
        if not instrument:
            raise ValueError(f"Instrument {symbol} not found")
        
        df = self.fetch_sample_data(symbol, days)
        count = self.store_ohlcv_data(instrument['id'], df)
        return count
