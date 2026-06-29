from flask import Blueprint, request, jsonify
from models.strategy import Strategy
from database import db
from routes.auth import token_required

strategies_bp = Blueprint('strategies', __name__)

@strategies_bp.route('/', methods=['GET'])
@token_required
def get_strategies():
    """Get strategies (system and user's custom strategies)"""
    system_only = request.args.get('system_only', 'false').lower() == 'true'
    
    strategy_model = Strategy(db)
    strategies = strategy_model.get_all_strategies(
        user_id=request.user_id,
        active_only=True,
        system_only=system_only
    )
    
    return jsonify({'strategies': strategies}), 200

@strategies_bp.route('/<strategy_id>', methods=['GET'])
@token_required
def get_strategy(strategy_id):
    """Get a specific strategy"""
    strategy_model = Strategy(db)
    strategy = strategy_model.get_strategy_by_id(strategy_id)
    
    if not strategy:
        return jsonify({'error': 'Strategy not found'}), 404
    
    return jsonify({'strategy': strategy}), 200

@strategies_bp.route('/', methods=['POST'])
@token_required
def create_strategy():
    """Create a custom strategy"""
    data = request.get_json()
    
    required_fields = ['name', 'entry_conditions', 'exit_conditions', 'risk_parameters', 'timeframe']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'{field} is required'}), 400
    
    strategy_model = Strategy(db)
    strategy = strategy_model.create_strategy(
        user_id=request.user_id,
        name=data['name'],
        description=data.get('description'),
        entry_conditions=data['entry_conditions'],
        exit_conditions=data['exit_conditions'],
        risk_parameters=data['risk_parameters'],
        timeframe=data['timeframe'],
        instrument_filters=data.get('instrument_filters')
    )
    
    if strategy:
        return jsonify({'strategy': strategy, 'message': 'Strategy created successfully'}), 201
    
    return jsonify({'error': 'Failed to create strategy'}), 500

@strategies_bp.route('/<strategy_id>', methods=['PUT'])
@token_required
def update_strategy(strategy_id):
    """Update a strategy"""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    strategy_model = Strategy(db)
    
    # Check if user owns this strategy or if it's a system strategy
    strategy = strategy_model.get_strategy_by_id(strategy_id)
    if not strategy:
        return jsonify({'error': 'Strategy not found'}), 404
    
    if strategy['is_system']:
        return jsonify({'error': 'Cannot modify system strategies'}), 403
    
    if strategy['(user_id)'] != request.user_id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    success = strategy_model.update_strategy(strategy_id, data)
    
    if success:
        return jsonify({'message': 'Strategy updated successfully'}), 200
    
    return jsonify({'error': 'Failed to update strategy'}), 500

@strategies_bp.route('/<strategy_id>', methods=['DELETE'])
@token_required
def delete_strategy(strategy_id):
    """Delete a custom strategy"""
    strategy_model = Strategy(db)
    
    # Check if user owns this strategy
    strategy = strategy_model.get_strategy_by_id(strategy_id)
    if not strategy:
        return jsonify({'error': 'Strategy not found'}), 404
    
    if strategy['is_system']:
        return jsonify({'error': 'Cannot delete system strategies'}), 403
    
    if strategy['(user_id)'] != request.user_id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    success = strategy_model.delete_strategy(strategy_id, request.user_id)
    
    if success:
        return jsonify({'message': 'Strategy deleted successfully'}), 200
    
    return jsonify({'error': 'Failed to delete strategy'}), 500

@strategies_bp.route('/<strategy_id>/backtest', methods=['POST'])
@token_required
def backtest_strategy(strategy_id):
    """Run a backtest for a strategy"""
    data = request.get_json()
    
    if not data or not data.get('instrument_id'):
        return jsonify({'error': 'instrument_id is required'}), 400
    
    instrument_id = data['instrument_id']
    start_date = data.get('start_date')
    end_date = data.get('end_date')
    initial_capital = data.get('initial_capital', 100000)
    
    strategy_model = Strategy(db)
    strategy = strategy_model.get_strategy_by_id(strategy_id)
    
    if not strategy:
        return jsonify({'error': 'Strategy not found'}), 404
    
    if not strategy['is_active']:
        return jsonify({'error': 'Strategy is not active'}), 400
    
    from services.backtest_service import BacktestService
    
    backtest_service = BacktestService()
    results = backtest_service.run_backtest(
        strategy=strategy,
        instrument_id=instrument_id,
        start_date=start_date,
        end_date=end_date,
        initial_capital=initial_capital
    )
    
    if 'error' in results:
        return jsonify({'error': results['error']}), 400
    
    return jsonify({'backtest': results}), 200
