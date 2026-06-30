import pandas as pd
from datetime import datetime
from services.strategy_service import StrategyService
from services.data_service import DataService
from utils.indicators import IndicatorEngine

class BacktestService:
    """Service for backtesting trading strategies on historical data"""
    
    def __init__(self):
        self.strategy_service = StrategyService()
        self.indicator_engine = IndicatorEngine()
        self.data_service = DataService()
    
    def run_backtest(self, strategy, instrument_id, start_date=None, end_date=None, initial_capital=100000):
        """
        Run a backtest for a strategy on historical data.
        
        Args:
            strategy: Strategy dictionary with entry/exit conditions
            instrument_id: Instrument to backtest on
            start_date: Start date for backtest (optional)
            end_date: End date for backtest (optional)
            initial_capital: Starting capital for the backtest
        
        Returns:
            Dictionary with backtest results and metrics
        """
        # Get historical data
        data = self.data_service.get_ohlcv_data(
            instrument_id, 
            timeframe=strategy['timeframe'],
            start_date=start_date,
            end_date=end_date
        )
        
        if data.empty or len(data) < 50:
            return {'error': 'Insufficient data for backtesting'}
        
        # Calculate indicators for the entire dataset
        indicators = self.indicator_engine.calculate_all_indicators(data)
        
        # Run backtest
        trades = []
        current_position = None
        capital = initial_capital
        position_size = 0
        
        for i in range(50, len(data)):  # Start from 50 to have enough indicator data
            current_data = data.iloc[:i+1]
            current_indicators = {k: v.iloc[:i+1] for k, v in indicators.items()}
            
            # Check entry conditions if not in position
            if current_position is None:
                entry_met = self.strategy_service.evaluate_rule_set(
                    strategy['entry_conditions'].get('rules', []),
                    strategy['entry_conditions'].get('logic', 'AND'),
                    current_data,
                    current_indicators
                )
                
                if entry_met:
                    # Calculate position size (simplified - 10% of capital)
                    entry_price = data['close'].iloc[i]
                    risk_amount = capital * 0.10
                    position_size = int(risk_amount / entry_price)
                    
                    # Calculate stop loss and take profit
                    sl, tp = self.strategy_service.calculate_risk_parameters(
                        strategy['risk_parameters'],
                        current_data,
                        current_indicators
                    )
                    
                    current_position = {
                        'entry_date': data['date'].iloc[i],
                        'entry_price': entry_price,
                        'quantity': position_size,
                        'stop_loss': sl,
                        'take_profit': tp,
                        'capital_at_entry': capital
                    }
            
            # Check exit conditions if in position
            elif current_position:
                exit_met = False
                exit_reason = None
                exit_price = data['close'].iloc[i]
                
                # Check stop loss
                if current_position['stop_loss'] and exit_price <= current_position['stop_loss']:
                    exit_met = True
                    exit_reason = 'stop_loss'
                    exit_price = current_position['stop_loss']
                
                # Check take profit
                elif current_position['take_profit'] and exit_price >= current_position['take_profit']:
                    exit_met = True
                    exit_reason = 'take_profit'
                    exit_price = current_position['take_profit']
                
                # Check exit conditions
                else:
                    exit_met = self.strategy_service.evaluate_rule_set(
                        strategy['exit_conditions'].get('rules', []),
                        strategy['exit_conditions'].get('logic', 'AND'),
                        current_data,
                        current_indicators
                    )
                    if exit_met:
                        exit_reason = 'signal'
                
                if exit_met:
                    # Calculate P&L
                    pnl = (exit_price - current_position['entry_price']) * current_position['quantity']
                    pnl_percentage = (pnl / current_position['capital_at_entry']) * 100
                    capital += pnl
                    
                    trades.append({
                        'entry_date': current_position['entry_date'],
                        'exit_date': data['date'].iloc[i],
                        'entry_price': current_position['entry_price'],
                        'exit_price': exit_price,
                        'quantity': current_position['quantity'],
                        'pnl': pnl,
                        'pnl_percentage': pnl_percentage,
                        'exit_reason': exit_reason,
                        'capital_after': capital
                    })
                    
                    current_position = None
        
        # Calculate performance metrics
        metrics = self.calculate_metrics(trades, initial_capital, capital)
        
        return {
            'trades': trades,
            'metrics': metrics,
            'strategy_name': strategy['name'],
            'instrument_id': instrument_id,
            'initial_capital': initial_capital,
            'final_capital': capital
        }
    
    def calculate_metrics(self, trades, initial_capital, final_capital):
        """Calculate performance metrics from backtest results"""
        if not trades:
            return {
                'total_trades': 0,
                'total_return': 0,
                'total_return_percentage': 0,
                'win_rate': 0,
                'avg_win': 0,
                'avg_loss': 0,
                'profit_factor': 0,
                'max_drawdown': 0,
                'sharpe_ratio': 0
            }
        
        total_trades = len(trades)
        winning_trades = [t for t in trades if t['pnl'] > 0]
        losing_trades = [t for t in trades if t['pnl'] <= 0]
        
        total_return = final_capital - initial_capital
        total_return_percentage = (total_return / initial_capital) * 100
        
        win_rate = (len(winning_trades) / total_trades) * 100 if total_trades > 0 else 0
        
        avg_win = sum(t['pnl'] for t in winning_trades) / len(winning_trades) if winning_trades else 0
        avg_loss = sum(t['pnl'] for t in losing_trades) / len(losing_trades) if losing_trades else 0
        
        gross_profit = sum(t['pnl'] for t in winning_trades) if winning_trades else 0
        gross_loss = abs(sum(t['pnl'] for t in losing_trades)) if losing_trades else 0
        profit_factor = gross_profit / gross_loss if gross_loss > 0 else float('inf')
        
        # Calculate max drawdown
        peak = initial_capital
        max_drawdown = 0
        equity_curve = [initial_capital]
        
        for trade in trades:
            equity = equity_curve[-1] + trade['pnl']
            equity_curve.append(equity)
            
            if equity > peak:
                peak = equity
            
            drawdown = (peak - equity) / peak * 100
            if drawdown > max_drawdown:
                max_drawdown = drawdown
        
        # Calculate Sharpe ratio (simplified)
        if len(equity_curve) > 1:
            returns = pd.Series(equity_curve).pct_change().dropna()
            sharpe_ratio = (returns.mean() / returns.std()) * (252 ** 0.5) if returns.std() > 0 else 0
        else:
            sharpe_ratio = 0
        
        return {
            'total_trades': total_trades,
            'total_return': total_return,
            'total_return_percentage': total_return_percentage,
            'win_rate': win_rate,
            'avg_win': avg_win,
            'avg_loss': avg_loss,
            'profit_factor': profit_factor,
            'max_drawdown': max_drawdown,
            'sharpe_ratio': sharpe_ratio,
            'gross_profit': gross_profit,
            'gross_loss': gross_loss
        }
