from flask import Blueprint, request, jsonify
from services.data_service import DataService
from database import db
from routes.auth import token_required

data_bp = Blueprint('data', __name__)

@data_bp.route('/update', methods=['POST'])
@token_required
def update_data():
    """Update EOD data for instruments"""
    data = request.get_json()
    
    symbol = data.get('symbol')  # If provided, update only this symbol
    days = data.get('days', 252)
    use_real_data = data.get('use_real_data', True)
    
    data_service = DataService()
    
    try:
        if symbol:
            count = data_service.update_single_instrument(symbol, days, use_real_data)
            return jsonify({'message': f'Updated {symbol}: {count} records', 'count': count}), 200
        else:
            count = data_service.update_all_instruments(days, use_real_data)
            return jsonify({'message': f'Updated all instruments: {count} total records', 'count': count}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@data_bp.route('/instruments', methods=['GET'])
@token_required
def get_instruments():
    """Get list of instruments"""
    from models.instrument import Instrument
    
    instrument_model = Instrument(db)
    instruments = instrument_model.get_all_instruments(active_only=True)
    
    return jsonify({'instruments': instruments}), 200

@data_bp.route('/instruments/<symbol>/data', methods=['GET'])
@token_required
def get_instrument_data(symbol):
    """Get OHLCV data for an instrument"""
    from models.instrument import Instrument
    
    instrument_model = Instrument(db)
    instrument = instrument_model.get_instrument_by_symbol(symbol)
    
    if not instrument:
        return jsonify({'error': 'Instrument not found'}), 404
    
    data_service = DataService()
    timeframe = request.args.get('timeframe', '1D')
    limit = request.args.get('limit', type=int, default=252)
    
    data = data_service.get_ohlcv_data(instrument['id'], timeframe=timeframe, limit=limit)
    
    if data.empty:
        return jsonify({'error': 'No data available for this instrument'}), 404
    
    return jsonify({'data': data.to_dict('records')}), 200
