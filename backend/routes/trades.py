from flask import Blueprint, request, jsonify
from models.trade import Trade
from models.instrument import Instrument
from database import db
from routes.auth import token_required

trades_bp = Blueprint('trades', __name__)

@trades_bp.route('/', methods=['GET'])
@token_required
def get_trades():
    """Get user's trades with optional filters"""
    status = request.args.get('status')
    instrument_id = request.args.get('instrument_id')
    limit = request.args.get('limit', type=int, default=50)
    offset = request.args.get('offset', type=int, default=0)
    
    trade_model = Trade(db)
    trades = trade_model.get_user_trades(
        user_id=request.user_id,
        status=status,
        instrument_id=instrument_id,
        limit=limit,
        offset=offset
    )
    
    return jsonify({'trades': trades}), 200

@trades_bp.route('/', methods=['POST'])
@token_required
def create_trade():
    """Create a new trade"""
    data = request.get_json()
    
    required_fields = ['instrument_id', 'trade_type', 'entry_price', 'quantity', 'entry_date']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'{field} is required'}), 400
    
    instrument_model = Instrument(db)
    instrument = instrument_model.get_instrument_by_id(data['instrument_id'])
    
    if not instrument:
        return jsonify({'error': 'Instrument not found'}), 404
    
    trade_model = Trade(db)
    trade = trade_model.create_trade(
        user_id=request.user_id,
        instrument_id=data['instrument_id'],
        trade_type=data['trade_type'],
        entry_price=data['entry_price'],
        quantity=data['quantity'],
        entry_date=data['entry_date'],
        stop_loss=data.get('stop_loss'),
        take_profit=data.get('take_profit'),
        setup_type=data.get('setup_type'),
        notes=data.get('notes'),
        signal_id=data.get('signal_id')
    )
    
    if trade:
        return jsonify({'trade': trade, 'message': 'Trade created successfully'}), 201
    
    return jsonify({'error': 'Failed to create trade'}), 500

@trades_bp.route('/<trade_id>', methods=['GET'])
@token_required
def get_trade(trade_id):
    """Get a specific trade"""
    trade_model = Trade(db)
    trade = trade_model.get_trade_by_id(trade_id, request.user_id)
    
    if not trade:
        return jsonify({'error': 'Trade not found'}), 404
    
    return jsonify({'trade': trade}), 200

@trades_bp.route('/<trade_id>', methods=['PUT'])
@token_required
def update_trade(trade_id):
    """Update a trade"""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    trade_model = Trade(db)
    success = trade_model.update_trade(trade_id, request.user_id, data)
    
    if success:
        return jsonify({'message': 'Trade updated successfully'}), 200
    
    return jsonify({'error': 'Failed to update trade'}), 500

@trades_bp.route('/<trade_id>/close', methods=['POST'])
@token_required
def close_trade(trade_id):
    """Close a trade"""
    data = request.get_json()
    
    if not data or 'exit_price' not in data or 'exit_date' not in data:
        return jsonify({'error': 'exit_price and exit_date are required'}), 400
    
    trade_model = Trade(db)
    success = trade_model.close_trade(
        trade_id=trade_id,
        user_id=request.user_id,
        exit_price=data['exit_price'],
        exit_date=data['exit_date']
    )
    
    if success:
        return jsonify({'message': 'Trade closed successfully'}), 200
    
    return jsonify({'error': 'Failed to close trade'}), 500

@trades_bp.route('/performance', methods=['GET'])
@token_required
def get_performance():
    """Get user's performance metrics"""
    trade_model = Trade(db)
    performance = trade_model.get_user_performance(request.user_id)
    
    return jsonify({'performance': performance}), 200
