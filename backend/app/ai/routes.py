from flask import Blueprint, request, jsonify, current_app
from flask_login import login_required, current_user
from backend.extensions import db
from backend.models import Conversation
from flask import make_response

ai_bp = Blueprint('ai', __name__)


@ai_bp.route('/history', methods=['GET'])
@login_required
def history():
    print("📥 /history was called")
    try:
        conversations = (
            Conversation.query
            .filter_by(user_id=current_user.id)
            .order_by(Conversation.timestamp.desc())
            .all()
        )

        history_data = [
            {
                'id': conv.id,
                'prompt': conv.prompt,
                'response': conv.output_text,
                'model': conv.model_used,
                'style': conv.style,
                'timestamp': conv.timestamp.isoformat() if conv.timestamp else None
            }
            for conv in conversations
        ]
        # Force UTF-8 encoding for browser compatibility
        response = make_response(jsonify(history_data))
        response.headers["Content-Type"] = "application/json; charset=utf-8"
        return jsonify(history_data), 200

    except Exception as e:
        print("🔥 Error in /history:", str(e))
        return jsonify({'error': str(e)}), 500

