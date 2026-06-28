import pandas as pd
import pandas_ta as ta

class IndicatorEngine:
    """Technical indicator calculation engine using pandas-ta"""
    
    @staticmethod
    def calculate_sma(data, period=20):
        """Calculate Simple Moving Average"""
        return ta.sma(data['close'], length=period)
    
    @staticmethod
    def calculate_ema(data, period=20):
        """Calculate Exponential Moving Average"""
        return ta.ema(data['close'], length=period)
    
    @staticmethod
    def calculate_rsi(data, period=14):
        """Calculate Relative Strength Index"""
        return ta.rsi(data['close'], length=period)
    
    @staticmethod
    def calculate_macd(data, fast=12, slow=26, signal=9):
        """Calculate MACD"""
        macd_data = ta.macd(data['close'], fast=fast, slow=slow, signal=signal)
        return {
            'macd': macd_data[f'MACD_{fast}_{slow}_{signal}'],
            'signal': macd_data[f'MACDh_{fast}_{slow}_{signal}'],
            'histogram': macd_data[f'MACDs_{fast}_{slow}_{signal}']
        }
    
    @staticmethod
    def calculate_bollinger_bands(data, period=20, std_dev=2):
        """Calculate Bollinger Bands"""
        bb_data = ta.bbands(data['close'], length=period, std=std_dev)
        return {
            'upper': bb_data[f'BBL_{period}_{std_dev}'],
            'middle': bb_data[f'BBM_{period}_{std_dev}'],
            'lower': bb_data[f'BBU_{period}_{std_dev}']
        }
    
    @staticmethod
    def calculate_atr(data, period=14):
        """Calculate Average True Range"""
        return ta.atr(data['high'], data['low'], data['close'], length=period)
    
    @staticmethod
    def calculate_vwap(data):
        """Calculate Volume Weighted Average Price"""
        # VWAP = (Cumulative Price * Volume) / Cumulative Volume
        typical_price = (data['high'] + data['low'] + data['close']) / 3
        vwap = (typical_price * data['volume']).cumsum() / data['volume'].cumsum()
        return vwap
    
    @staticmethod
    def calculate_adx(data, period=14):
        """Calculate Average Directional Index"""
        adx_data = ta.adx(data['high'], data['low'], data['close'], length=period)
        return adx_data[f'ADX_{period}']
    
    @staticmethod
    def calculate_all_indicators(data):
        """Calculate all standard indicators for a dataset"""
        indicators = {}
        
        # Moving averages
        indicators['sma_20'] = IndicatorEngine.calculate_sma(data, 20)
        indicators['sma_50'] = IndicatorEngine.calculate_sma(data, 50)
        indicators['ema_20'] = IndicatorEngine.calculate_ema(data, 20)
        indicators['ema_50'] = IndicatorEngine.calculate_ema(data, 50)
        
        # Momentum
        indicators['rsi_14'] = IndicatorEngine.calculate_rsi(data, 14)
        
        # MACD
        macd = IndicatorEngine.calculate_macd(data)
        indicators.update(macd)
        
        # Volatility
        indicators['atr_14'] = IndicatorEngine.calculate_atr(data, 14)
        bb = IndicatorEngine.calculate_bollinger_bands(data)
        indicators.update(bb)
        
        # VWAP
        indicators['vwap'] = IndicatorEngine.calculate_vwap(data)
        
        # Trend strength
        indicators['adx_14'] = IndicatorEngine.calculate_adx(data, 14)
        
        return indicators
    
    @staticmethod
    def get_latest_indicator_value(indicator_series):
        """Get the latest (most recent) value from an indicator series"""
        if indicator_series is None or len(indicator_series) == 0:
            return None
        return indicator_series.iloc[-1]
