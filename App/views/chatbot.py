from flask import Blueprint, render_template
from flask import Blueprint, render_template, request

chatbot_views = Blueprint('chatbot_views', __name__, template_folder='../templates')

from App.controllers import (
    get_ai_response,
    start_conversation,
    call_until_return_response
    
)

@chatbot_views.route("/chatbot", methods=["GET", "POST"])
def chatbox_index():
    conversation_id = request.form.get("conversation_id", "")
    user_input = request.form.get("user_input", "")
    conversation_history = request.form.get("conversation_history", "")
    if request.method == "POST":
        if user_input.strip():
            conversation_history += f"\nUser: {user_input}\nAI:"
            ai_response = call_until_return_response(get_ai_response,conversation_history,user_input)
            conversation_history += ai_response
        return render_template("chatbot.html", conversation_id=conversation_id, conversation_history=conversation_history)
    else:
        conversation_id = start_conversation()
        conversation_history = f"AI: {conversation_id}"
        return render_template("chatbot.html", conversation_id=conversation_id, conversation_history=conversation_history)

@chatbot_views.route('/end_conversation', methods=['POST'])
def end_conversation():
    conversation_history = "AI: Hello, how can I help you?"
    conversation_id = ""
    return render_template('chatbot.html', conversation_id=conversation_id, conversation_history=conversation_history)