from flask import Blueprint, request, jsonify
from models.journal_entry import JournalEntry
from database import db
from routes.auth import token_required

journal_bp = Blueprint('journal', __name__)

@journal_bp.route('/entries', methods=['GET'])
@token_required
def get_entries():
    """Get user's journal entries"""
    entry_type = request.args.get('entry_type')
    trade_id = request.args.get('trade_id')
    limit = request.args.get('limit', type=int, default=50)
    offset = request.args.get('offset', type=int, default=0)
    
    journal_model = JournalEntry(db)
    entries = journal_model.get_user_entries(
        user_id=request.user_id,
        entry_type=entry_type,
        trade_id=trade_id,
        limit=limit,
        offset=offset
    )
    
    return jsonify({'entries': entries}), 200

@journal_bp.route('/entries', methods=['POST'])
@token_required
def create_entry():
    """Create a new journal entry"""
    data = request.get_json()
    
    if not data or not data.get('notes'):
        return jsonify({'error': 'notes are required'}), 400
    
    journal_model = JournalEntry(db)
    entry = journal_model.create_entry(
        user_id=request.user_id,
        notes=data['notes'],
        entry_type=data.get('entry_type', 'general'),
        trade_id=data.get('trade_id'),
        mood=data.get('mood'),
        tags=data.get('tags')
    )
    
    if entry:
        return jsonify({'entry': entry, 'message': 'Journal entry created successfully'}), 201
    
    return jsonify({'error': 'Failed to create journal entry'}), 500

@journal_bp.route('/entries/<entry_id>', methods=['GET'])
@token_required
def get_entry(entry_id):
    """Get a specific journal entry"""
    journal_model = JournalEntry(db)
    entry = journal_model.get_entry_by_id(entry_id, request.user_id)
    
    if not entry:
        return jsonify({'error': 'Entry not found'}), 404
    
    return jsonify({'entry': entry}), 200

@journal_bp.route('/entries/<entry_id>', methods=['PUT'])
@token_required
def update_entry(entry_id):
    """Update a journal entry"""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    journal_model = JournalEntry(db)
    success = journal_model.update_entry(entry_id, request.user_id, data)
    
    if success:
        return jsonify({'message': 'Journal entry updated successfully'}), 200
    
    return jsonify({'error': 'Failed to update journal entry'}), 500

@journal_bp.route('/entries/<entry_id>', methods=['DELETE'])
@token_required
def delete_entry(entry_id):
    """Delete a journal entry"""
    journal_model = JournalEntry(db)
    success = journal_model.delete_entry(entry_id, request.user_id)
    
    if success:
        return jsonify({'message': 'Journal entry deleted successfully'}), 200
    
    return jsonify({'error': 'Failed to delete journal entry'}), 500
