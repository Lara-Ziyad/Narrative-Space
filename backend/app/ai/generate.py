from flask import Blueprint, request, jsonify, current_app
from flask_login import login_required, current_user
from backend.extensions import db
from backend.models import Conversation
from backend.prompts.templates import get_prompt_template
from backend.rag.retriever_factory import get_retriever
generate_bp = Blueprint("generate", __name__)

@generate_bp.route("/generate", methods=["POST"])
@login_required
def generate():
    data = request.get_json()

    prompt = data.get("prompt", "").strip()
    style = data.get("style", "poetic")
    retrieval_mode = data.get("retrieval_mode", "faiss")  # 👈 user can choose FAISS or Chroma

    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400

    # Select retriever based on user preference
    retriever = get_retriever(mode=retrieval_mode)

    # Retrieve context from knowledge base
    context_chunks = retriever.search(query=prompt, top_k=1)
    context = context_chunks[0] if context_chunks else ""

    # Inject context into prompt template
    template = get_prompt_template(style)
    final_prompt = template.format(context=context, prompt=prompt)

    # Generate output using OpenAI
    client = current_app.openai_client
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": final_prompt}
            ],
            temperature=0.7,
            max_tokens=300
        )
        reply = response.choices[0].message.content

        # Save to database
        conv = Conversation(
            user_id=current_user.id,
            style=style,
            model_used="gpt-4o-mini",
            prompt=prompt,
            augmented_prompt=final_prompt,
            output_text=reply
        )
        db.session.add(conv)
        db.session.commit()

        return jsonify({"output": reply}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
