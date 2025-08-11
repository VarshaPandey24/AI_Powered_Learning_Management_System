# chatbot/views.py
import json
import google.generativeai as genai
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

# Configure the Gemini API
genai.configure(api_key=settings.GEMINI_API_KEY)

# This will hold the chat history for the session
# Note: For a real production app, you'd want to store this per-user, maybe in the session
chat_session = None

@csrf_exempt
def ask_gemini(request):
    global chat_session

    if request.method == 'POST':
        try:
            # Initialize the chat model if it doesn't exist
            if chat_session is None:
                # Use the updated model name here
                model = genai.GenerativeModel('gemini-2.5-flash')
                chat_session = model.start_chat(history=[])

            # Decode the request body to get the user's message
            data = json.loads(request.body.decode('utf-8'))
            user_message = data.get('message')

            if not user_message:
                return JsonResponse({'error': 'No message provided'}, status=400)

            # Send the message to Gemini and get the response
            response = chat_session.send_message(user_message)

            # Return the response text
            return JsonResponse({'response': response.text})

        except Exception as e:
            # Reset chat on error to start fresh next time
            chat_session = None 
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)