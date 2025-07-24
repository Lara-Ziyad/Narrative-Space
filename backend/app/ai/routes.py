from flask import Blueprint, request, jsonify, current_app
from flask_login import login_required, current_user
from backend.extensions import db
from backend.models import Conversation
from flask import make_response

ai_bp = Blueprint('ai', __name__)

@ai_bp.route('/models', methods=['GET'])
@login_required
def list_models():
    client = current_app.openai_client
    try:
        models = client.models.list()
        return jsonify([model.id for model in models]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@ai_bp.route('/generate', methods=['POST'])
@login_required
def generate():
    data = request.get_json()
    prompt = data.get('prompt')

    if not prompt:
        return jsonify({'error': 'Prompt is required'}), 400
    client = current_app.openai_client
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=150
        )

        reply = response.choices[0].message.content

        # Save the conversation to the database
        conv = Conversation(
            user_id=current_user.id,
            style=data.get('style') or data.get('type'),
            model_used=data.get('model', 'gpt-4o-mini'),
            prompt=prompt,
            augmented_prompt=prompt,  # or the augmented version if using RAG
            output_text=reply
        )
        db.session.add(conv)
        db.session.commit()


        return jsonify({'response': reply}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

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

