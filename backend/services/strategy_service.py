import pandas as pd
from utils.indicators import IndicatorEngine
from database import db

class StrategyService:
    """Service for evaluating strategies and generating signals"""
    
    def __init__(self):
        self.indicator_engine = IndicatorEngine()
    
    def evaluate_condition(self, condition, data, indicators):
        """
        Evaluate a single condition against data and indicators.
        
        Condition format:
        {
            "indicator": "EMA",
            "params": {"period": 20},
            "condition": "price_above",
            "value": "EMA_20"
        }
        """
        indicator = condition.get('indicator')
        params = condition.get('params', {})
        cond_type = condition.get('condition')
        value = condition.get('value')
        
        # Get current value
        if indicator == 'price':
            current_value = data['close'].iloc[-1]
        else:
            # Get indicator value
            indicator_key = f"{indicator.lower()}_{params.get('period', 20)}"
            if indicator_key in indicators:
                current_value = indicators[indicator_key].iloc[-1]
            else:
                return False
        
        # Get comparison value
        if value.startswith('EMA_') or value.startswith('SMA_') or value.startswith('RSI_'):
            # Reference another indicator
            if value in indicators:
                comparison_value = indicators[value].iloc[-1]
            else:
                return False
        else:
            # Numeric value
            try:
                comparison_value = float(value)
            except ValueError:
                return False
        
        # Evaluate condition
        if cond_type == 'price_above':
            return current_value > comparison_value
        elif cond_type == 'price_below':
            return current_value < comparison_value
        elif cond_type == 'greater_than':
            return current_value > comparison_value
        elif cond_type == 'less_than':
            return current_value < comparison_value
        elif cond_type == 'equal':
            return abs(current_value - comparison_value) < 0.01
        elif cond_type == 'cross_above':
            # Check if current is above and previous was below
            if len(indicators.get(value, [])) < 2:
                return False
            prev_current = current_value
            prev_comparison = indicators[value].iloc[-2]
            return prev_current > prev_comparison and indicators[indicator_key].iloc[-2] <= indicators[value].iloc[-2]
        elif cond_type == 'cross_below':
            # Check if current is below and previous was above
            if len(indicators.get(value, [])) < 2:
                return False
            prev_current = current_value
            prev_comparison = indicators[value].iloc[-2]
            return prev_current < prev_comparison and indicators[indicator_key].iloc[-2] >= indicators[value].iloc[-2]
        else:
            return False
    
    def evaluate_rule_set(self, rules, logic, data, indicators):
        """
        Evaluate a set of rules with AND/OR logic.
        
        Rules format:
        {
            "rules": [condition1, condition2, ...],
            "logic": "AND" or "OR"
        }
        """
        if not rules:
            return True
        
        results = []
        for rule in rules:
            result = self.evaluate_condition(rule, data, indicators)
            results.append(result)
        
        if logic == 'AND':
            return all(results)
        elif logic == 'OR':
            return any(results)
        else:
            return False
    
    def calculate_risk_parameters(self, risk_params, data, indicators):
        """
        Calculate stop loss and take profit based on risk parameters.
        
        Risk params format:
        {
            "stop_loss_method": "atr",
            "stop_loss_value": 2,
            "take_profit_method": "risk_reward",
            "take_profit_value": 2
        }
        """
        current_price = data['close'].iloc[-1]
        
        # Calculate stop loss
        sl_method = risk_params.get('stop_loss_method', 'atr')
        sl_value = risk_params.get('stop_loss_value', 2)
        
        if sl_method == 'atr':
            atr = indicators.get('atr_14', pd.Series([current_price * 0.02])).iloc[-1]
            stop_loss = current_price - (atr * sl_value)
        elif sl_method == 'percentage':
            stop_loss = current_price * (1 - sl_value / 100)
        else:
            stop_loss = current_price * 0.98  # Default 2%
        
        # Calculate take profit
        tp_method = risk_params.get('take_profit_method', 'risk_reward')
        tp_value = risk_params.get('take_profit_value', 2)
        
        if tp_method == 'risk_reward':
            risk = current_price - stop_loss
            take_profit = current_price + (risk * tp_value)
        elif tp_method == 'percentage':
            take_profit = current_price * (1 + tp_value / 100)
        else:
            take_profit = current_price * 1.04  # Default 4%
        
        return stop_loss, take_profit
    
    def calculate_confidence_score(self, data, indicators):
        """
        Calculate confidence score for a signal based on multiple factors.
        
        Factors:
        - Trend strength (ADX)
        - Volume confirmation
        - Risk/reward ratio
        """
        score = 0.5  # Base score
        
        # Trend strength (if ADX available)
        if 'adx_14' in indicators:
            adx = indicators['adx_14'].iloc[-1]
            if adx > 25:
                score += 0.2
            if adx > 40:
                score += 0.1
        
        # Volume confirmation
        if len(data) > 20:
            avg_volume = data['volume'].iloc[-20:].mean()
            current_volume = data['volume'].iloc[-1]
            if current_volume > avg_volume * 1.5:
                score += 0.1
            if current_volume > avg_volume * 2:
                score += 0.1
        
        # Cap at 0.95
        return min(score, 0.95)
    
    def generate_signal(self, strategy, instrument_id):
        """
        Generate a signal for a strategy and instrument.
        
        Returns signal data or None if conditions not met.
        """
        from services.data_service import DataService
        from datetime import datetime, timedelta
        
        data_service = DataService()
        
        # Get OHLCV data
        data = data_service.get_ohlcv_data(instrument_id, timeframe=strategy['timeframe'], limit=252)
        
        if data.empty or len(data) < 50:
            return None
        
        # Calculate indicators
        indicators = self.indicator_engine.calculate_all_indicators(data)
        
        # Evaluate entry conditions
        entry_conditions = strategy['entry_conditions']
        entry_met = self.evaluate_rule_set(
            entry_conditions.get('rules', []),
            entry_conditions.get('logic', 'AND'),
            data,
            indicators
        )
        
        if not entry_met:
            return None
        
        # Calculate risk parameters
        risk_params = strategy['risk_parameters']
        stop_loss, take_profit = self.calculate_risk_parameters(risk_params, data, indicators)
        
        # Calculate confidence score
        confidence = self.calculate_confidence_score(data, indicators)
        
        # Determine signal type (simplified - assumes BUY for now)
        signal_type = 'BUY'
        entry_price = data['close'].iloc[-1]
        
        # Generate reasoning
        reasoning = f"Signal generated by {strategy['name']} strategy. "
        reasoning += f"Entry conditions met. "
        reasoning += f"Confidence: {confidence:.2f}. "
        reasoning += f"Risk/Reward: {((take_profit - entry_price) / (entry_price - stop_loss)):.2f}:1"
        
        return {
            'strategy_id': strategy['id'],
            'instrument_id': instrument_id,
            'signal_type': signal_type,
            'entry_price': entry_price,
            'stop_loss': stop_loss,
            'take_profit': take_profit,
            'confidence_score': confidence,
            'reasoning': reasoning,
            'expires_at': datetime.now() + timedelta(days=7)
        }
