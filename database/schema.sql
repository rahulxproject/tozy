-- Indian Trading Platform Database Schema
-- PostgreSQL Schema

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Exchanges
CREATE TABLE exchanges (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    code VARCHAR(10) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    country VARCHAR(100),
    timezone VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Instruments (Stocks, Indices)
CREATE TABLE instruments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    symbol VARCHAR(10) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    exchange_id UUID REFERENCES exchanges(id),
    sector VARCHAR(100),
    market_cap DECIMAL(20, 2),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- OHLCV Data (Open, High, Low, Close, Volume)
CREATE TABLE ohlcv_data (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    instrument_id UUID NOT NULL REFERENCES instruments(id) ON DELETE CASCADE,
    date DATE NOT NULL,
    timeframe VARCHAR(10) NOT NULL, -- 1D, 1W, 1M
    open DECIMAL(12, 2) NOT NULL,
    high DECIMAL(12, 2) NOT NULL,
    low DECIMAL(12, 2) NOT NULL,
    close DECIMAL(12, 2) NOT NULL,
    volume BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(instrument_id, date, timeframe)
);

-- Index for OHLCV queries
CREATE INDEX idx_ohlcv_instrument_date ON ohlcv_data(instrument_id, date DESC);
CREATE INDEX idx_ohlcv_date ON ohlcv_data(date DESC);

-- Users
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    name VARCHAR(255),
    subscription_tier VARCHAR(20) DEFAULT 'free', -- free, basic, pro
    subscription_status VARCHAR(20) DEFAULT 'active', -- active, cancelled, expired
    preferences JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Strategies
CREATE TABLE strategies (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    user_id UUID REFERENCES users(id) ON DELETE SET NULL, -- NULL for system strategies
    is_system BOOLEAN DEFAULT TRUE,
    entry_conditions JSONB NOT NULL,
    exit_conditions JSONB NOT NULL,
    risk_parameters JSONB NOT NULL,
    timeframe VARCHAR(10) NOT NULL,
    instrument_filters JSONB,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Signals
CREATE TABLE signals (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    strategy_id UUID NOT NULL REFERENCES strategies(id) ON DELETE CASCADE,
    instrument_id UUID NOT NULL REFERENCES instruments(id) ON DELETE CASCADE,
    signal_type VARCHAR(10) NOT NULL CHECK (signal_type IN ('BUY', 'SELL')),
    entry_price DECIMAL(12, 2) NOT NULL,
    stop_loss DECIMAL(12, 2) NOT NULL,
    take_profit DECIMAL(12, 2) NOT NULL,
    confidence_score DECIMAL(3, 2) NOT NULL CHECK (confidence_score >= 0 AND confidence_score <= 1),
    reasoning TEXT,
    generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NOT NULL,
    status VARCHAR(20) DEFAULT 'active' CHECK (status IN ('active', 'expired', 'executed'))
);

-- Index for signal queries
CREATE INDEX idx_signals_instrument_date ON signals(instrument_id, generated_at DESC);
CREATE INDEX idx_signals_strategy_date ON signals(strategy_id, generated_at DESC);
CREATE INDEX idx_signals_status ON signals(status, expires_at);

-- Trades
CREATE TABLE trades (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    instrument_id UUID NOT NULL REFERENCES instruments(id),
    signal_id UUID REFERENCES signals(id) ON DELETE SET NULL,
    trade_type VARCHAR(10) NOT NULL CHECK (trade_type IN ('LONG', 'SHORT')),
    entry_price DECIMAL(12, 2) NOT NULL,
    exit_price DECIMAL(12, 2),
    quantity INTEGER NOT NULL,
    entry_date DATE NOT NULL,
    exit_date DATE,
    stop_loss DECIMAL(12, 2),
    take_profit DECIMAL(12, 2),
    pnl DECIMAL(12, 2),
    pnl_percentage DECIMAL(8, 4),
    setup_type VARCHAR(100),
    mistake_tags JSONB,
    notes TEXT,
    status VARCHAR(20) DEFAULT 'open' CHECK (status IN ('open', 'closed', 'cancelled')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Index for trade queries
CREATE INDEX idx_trades_user_date ON trades(user_id, entry_date DESC);
CREATE INDEX idx_trades_user_status ON trades(user_id, status);

-- Journal Entries
CREATE TABLE journal_entries (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    trade_id UUID REFERENCES trades(id) ON DELETE SET NULL,
    entry_type VARCHAR(20) NOT NULL CHECK (entry_type IN ('pre_trade', 'post_trade', 'general')),
    notes TEXT NOT NULL,
    mood VARCHAR(20) CHECK (mood IN ('confident', 'fearful', 'greedy', 'neutral', 'frustrated', 'excited')),
    tags JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Index for journal queries
CREATE INDEX idx_journal_user_date ON journal_entries(user_id, created_at DESC);

-- AI Analysis Logs (for cost tracking)
CREATE TABLE ai_analysis_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    analysis_type VARCHAR(50) NOT NULL,
    prompt TEXT NOT NULL,
    response TEXT,
    tokens_used INTEGER,
    cost DECIMAL(10, 6),
    model_used VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Audit Logs (for compliance)
CREATE TABLE audit_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    action VARCHAR(100) NOT NULL,
    entity_type VARCHAR(50),
    entity_id UUID,
    changes JSONB,
    ip_address VARCHAR(50),
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Index for audit log queries
CREATE INDEX idx_audit_user_date ON audit_logs(user_id, created_at DESC) WHERE user_id IS NOT NULL;
CREATE INDEX idx_audit_action_date ON audit_logs(action, created_at DESC);

-- Sample Data: Exchanges
 INTO exchanges (code, name, country, timezone) VALUES
('NSE', 'National Stock Exchange of India', 'India', 'Asia/Kolkata'),
('BSE', 'Bombay Stock Exchange', 'India', 'Asia/Kolkata'),
('MCX', 'Multi Commodity Exchange', 'India', 'Asia/Kolkata');

-- Sample Data: Top NSE Instruments (will be expanded)
INSERT INTO instruments (symbol, name, exchange_id, sector, is_active) VALUES
('RELIANCE', 'Reliance Industries Ltd', (SELECT id FROM exchanges WHERE code = 'NSE'), 'Energy', TRUE),
('TCS', 'Tata Consultancy Services', (SELECT id FROM exchanges WHERE code = 'NSE'), 'IT', TRUE),
('HDFCBANK', 'HDFC Bank', (SELECT id FROM exchanges WHERE code = 'NSE'), 'Banking', TRUE),
('INFY', 'Infosys Ltd', (SELECT id FROM exchanges WHERE code = 'NSE'), 'IT', TRUE),
('ICICIBANK', 'ICICI Bank', (SELECT id FROM exchanges WHERE code = 'NSE'), 'Banking', TRUE),
('SBIN', 'State Bank of India', (SELECT id FROM exchanges WHERE code = 'NSE'), 'Banking', TRUE),
('BHARTIARTL', 'Bharti Airtel', (SELECT id FROM exchanges WHERE code = 'NSE'), 'Telecom', TRUE),
('ITC', 'ITC Ltd', (SELECT id FROM exchanges WHERE code = 'NSE'), 'FMCG', TRUE),
('KOTAKBANK', 'Kotak Mahindra Bank', (SELECT id FROM exchanges WHERE code = 'NSE'), 'Banking', TRUE),
('LICI', 'Life Insurance Corporation', (SELECT id FROM exchanges WHERE code = 'NSE'), 'Insurance', TRUE);

-- Sample Data: System Strategies (5 pre-built strategies for v1)
INSERT INTO strategies (name, description, is_system, entry_conditions, exit_conditions, risk_parameters, timeframe, is_active) VALUES
(
    'EMA Pullback',
    'Buy when price pulls back to 20 EMA in uptrend',
    TRUE,
    '{"rules": [{"indicator": "EMA", "params": {"period": 20}, "condition": "price_above", "value": "EMA_20"}, {"indicator": "EMA", "params": {"period": 50}, "condition": "trend_up", "value": "EMA_20_gt_EMA_50"}, {"indicator": "price", "condition": "pullback_to", "value": "EMA_20", "tolerance": "0.02"}], "logic": "AND"}'::jsonb,
    '{"rules": [{"indicator": "price", "condition": "target", "value": "entry_plus_2x_risk"}, {"indicator": "price", "condition": "stop_loss", "value": "entry_minus_1x_risk"}], "logic": "OR"}'::jsonb,
    '{"stop_loss_method": "atr", "stop_loss_value": 2, "take_profit_method": "risk_reward", "take_profit_value": 2, "position_sizing_method": "risk_percent", "position_sizing_value": 1}'::jsonb,
    '1D',
    TRUE
),
(
    'Breakout',
    'Buy when price breaks above resistance with high volume',
    TRUE,
    '{"rules": [{"indicator": "price", "condition": "breakout", "value": "20_day_high"}, {"indicator": "volume", "condition": "greater_than", "value": "2x_average"}], "logic": "AND"}'::jsonb,
    '{"rules": [{"indicator": "price", "condition": "target", "value": "next_resistance"}, {"indicator": "price", "condition": "stop_loss", "value": "below_breakout"}], "logic": "OR"}'::jsonb,
    '{"stop_loss_method": "atr", "stop_loss_value": 2, "take_profit_method": "risk_reward", "take_profit_value": 2, "position_sizing_method": "risk_percent", "position_sizing_value": 1}'::jsonb,
    '1D',
    TRUE
),
(
    'RSI Reversal',
    'Buy when RSI is oversold and shows divergence',
    TRUE,
    '{"rules": [{"indicator": "RSI", "params": {"period": 14}, "condition": "oversold", "value": "30"}, {"indicator": "price", "condition": "divergence", "value": "bullish"}], "logic": "AND"}'::jsonb,
    '{"rules": [{"indicator": "price", "condition": "target", "value": "RSI_50"}, {"indicator": "price", "condition": "stop_loss", "value": "recent_low"}], "logic": "OR"}'::jsonb,
    '{"stop_loss_method": "atr", "stop_loss_value": 2, "take_profit_method": "risk_reward", "take_profit_value": 2, "position_sizing_method": "risk_percent", "position_sizing_value": 1}'::jsonb,
    '1D',
    TRUE
),
(
    'Volume Breakout',
    'Buy breakouts with unusually high volume',
    TRUE,
    '{"rules": [{"indicator": "price", "condition": "breakout", "value": "resistance"}, {"indicator": "volume", "condition": "spike", "value": "3x_average"}], "logic": "AND"}'::jsonb,
    '{"rules": [{"indicator": "price", "condition": "target", "value": "range_height"}, {"indicator": "price", "condition": "stop_loss", "value": "middle_of_range"}], "logic": "OR"}'::jsonb,
    '{"stop_loss_method": "atr", "stop_loss_value": 2, "take_profit_method": "risk_reward", "take_profit_value": 2, "position_sizing_method": "risk_percent", "position_sizing_value": 1}'::jsonb,
    '1D',
    TRUE
),
(
    'Swing Retracement',
    'Buy retracements in larger uptrend',
    TRUE,
    '{"rules": [{"indicator": "EMA", "params": {"period": 50}, "condition": "trend_up", "value": "price_above"}, {"indicator": "price", "condition": "retracement", "value": "38_61_percent", "context": "of_swing"}], "logic": "AND"}'::jsonb,
    '{"rules": [{"indicator": "price", "condition": "target", "value": "swing_high"}, {"indicator": "price", "condition": "stop_loss", "value": "below_61_percent"}], "logic": "OR"}'::jsonb,
    '{"stop_loss_method": "atr", "stop_loss_value": 2, "take_profit_method": "risk_reward", "take_profit_value": 2, "position_sizing_method": "risk_percent", "position_sizing_value": 1}'::jsonb,
    '1D',
    TRUE
);
