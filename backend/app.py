from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os

# Import blueprints
from routes.auth import auth_bp
from routes.signals import signals_bp
from routes.trades import trades_bp
from routes.strategies import strategies_bp
from routes.data import data_bp
from routes.journal import journal_bp

load_dotenv()

app = Flask(__name__)
CORS(app)

# Configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
app.config['DATABASE_URL'] = os.getenv('DATABASE_URL', 'postgresql://localhost/trading_platform')

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(signals_bp, url_prefix='/api/signals')
app.register_blueprint(trades_bp, url_prefix='/api/trades')
app.register_blueprint(strategies_bp, url_prefix='/api/strategies')
app.register_blueprint(data_bp, url_prefix='/api/data')
app.register_blueprint(journal_bp, url_prefix='/api/journal')

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'service': 'indian-trading-platform-backend',
        'version': '0.1.0'
    })

@app.route('/api', methods=['GET'])
def api_root():
    return jsonify({
        'message': 'Indian AI Trading Platform API',
        'endpoints': {
            'health': '/api/health',
            'auth': '/api/auth/*',
            'signals': '/api/signals/*',
            'trades': '/api/trades/*',
            'strategies': '/api/strategies/*',
            'analytics': '/api/analytics/*'
        }
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
