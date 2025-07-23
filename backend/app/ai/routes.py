from flask import Blueprint, request, jsonify, current_app
from flask_login import login_required, current_user
from extensions import db
from models import Conversation

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
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=150
        )

        reply = response['choices'][0]['message']['content']

        # Save the conversation to the database
        conv = Conversation(
            user_id=current_user.id,
            style=data.get('style'),
            model_used=data.get('model', 'gpt-3.5-turbo'),
            prompt=prompt,
            augmented_prompt=prompt,  # or the augmented version if using RAG
            output_text=reply
        )
        db.session.add(conv)
        db.session.commit()

        return jsonify({'response': reply}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
