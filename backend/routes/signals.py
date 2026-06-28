from flask import Blueprint, request, jsonify
from models.signal import Signal
from models.strategy import Strategy
from models.instrument import Instrument
from database import db
from routes.auth import token_required

signals_bp = Blueprint('signals', __name__)

@signals_bp.route('/', methods=['GET'])
@token_required
def get_signals():
    """Get signals with optional filters"""
    instrument_id = request.args.get('instrument_id')
    strategy_id = request.args.get('strategy_id')
    status = request.args.get('status', 'active')
    limit = request.args.get('limit', type=int)
    
    signal_model = Signal(db)
    signals = signal_model.get_signals(
        instrument_id=instrument_id,
        strategy_id=strategy_id,
        status=status,
        limit=limit
    )
    
    return jsonify({'signals': signals}), 200

@signals_bp.route('/<signal_id>', methods=['GET'])
@token_required
def get_signal(signal_id):
    """Get a specific signal"""
    signal_model = Signal(db)
    signal = signal_model.get_signal_by_id(signal_id)
    
    if not signal:
        return jsonify({'error': 'Signal not found'}), 404
    
    return jsonify({'signal': signal}), 200

@signals_bp.route('/generate', methods=['POST'])
@token_required
def generate_signal():
    """Generate a signal for a strategy and instrument"""
    data = request.get_json()
    
    if not data or not data.get('strategy_id') or not data.get('instrument_id'):
        return jsonify({'error': 'strategy_id and instrument_id are required'}), 400
    
    strategy_id = data['strategy_id']
    instrument_id = data['instrument_id']
    
    strategy_model = Strategy(db)
    signal_model = Signal(db)
    
    strategy = strategy_model.get_strategy_by_id(strategy_id)
    
    if not strategy:
        return jsonify({'error': 'Strategy not found'}), 404
    
    if not strategy['is_active']:
        return jsonify({'error': 'Strategy is not active'}), 400
    
    # Use strategy service to generate signal
    from services.strategy_service import StrategyService
    
    strategy_service = StrategyService()
    signal_data = strategy_service.generate_signal(strategy, instrument_id)
    
    if not signal_data:
        return jsonify({'error': 'Strategy conditions not met for this instrument'}), 400
    
    # Create signal in database
    signal = signal_model.create_signal(**signal_data)
    
    if signal:
        return jsonify({'signal': signal, 'message': 'Signal generated successfully'}), 201
    
    return jsonify({'error': 'Failed to generate signal'}), 500
