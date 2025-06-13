# app.py - Flask Backend for Sentiment Analysis and Dashboard Serving

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import requests
import json
import os
from collections import Counter # To count sentiment occurrences

# Use __app_id for the app name in Canvas environment if available, otherwise use __name__.
# This fixes the NameError when running locally.
app = Flask(__name__ if '__app_id__' not in globals() else __app_id__)
CORS(app) # Enable CORS for all routes, important for frontend communication

# IMPORTANT: In a real application, you would load your API key securely,
# e.g., from environment variables, not hardcoded.
# For this Canvas environment, the API key is handled automatically by the platform
# when making fetch calls within the frontend, but for a backend, you would
# typically provide it here if you were running this independently.
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "") # Get from environment or leave empty for Canvas

# Log the API key status for debugging
if not GEMINI_API_KEY:
    print("WARNING: GEMINI_API_KEY environment variable is not set. "
          "AI model calls might fail if running outside Canvas without an API key.")
else:
    print("GEMINI_API_KEY is loaded.")


@app.route('/')
def home():
    """Basic route to confirm the server is running or serve the dashboard."""
    # Ensure 'dashboard.html' is in a 'templates' folder in the same directory as app.py
    return render_template('dashboard.html')

@app.route('/analyze_sentiment', methods=['POST'])
def analyze_sentiment():
    """
    API endpoint to receive a single movie review text, call the Gemini API for sentiment,
    and return the predicted sentiment.
    """
    if not request.is_json:
        print("Error: Request is not JSON.")
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.get_json()
    review_text = data.get('review_text')

    if not review_text:
        print("Error: Missing 'review_text' in request data.")
        return jsonify({"error": "Missing 'review_text' in request"}), 400

    # Ensure API key is available before making the request
    if not GEMINI_API_KEY:
        print("Error: Gemini API Key is not set, cannot proceed with AI model call.")
        return jsonify({"error": "Gemini API key is missing. Please set the GEMINI_API_KEY environment variable."}), 500

    try:
        # Construct the prompt for the LLM
        # We ask the LLM to classify sentiment as 'positive', 'negative', or 'neutral'
        # and to respond ONLY with one of those words.
        prompt = (
            f"Classify the sentiment of the following movie review as either "
            f"'positive', 'negative', or 'neutral'. "
            f"Respond with only one word: positive, negative, or neutral.\n\n"
            f"Review: \"{review_text}\""
        )

        chat_history = [{"role": "user", "parts": [{"text": prompt}]}]
        payload = {"contents": chat_history}

        # Gemini API URL
        gemini_api_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
        gemini_api_url += f"?key={GEMINI_API_KEY}" # Always append key as it's checked above

        headers = {
            'Content-Type': 'application/json'
        }

        print(f"Making call to Gemini API for review: '{review_text[:50]}...'")
        # Make the request to the Gemini API
        response = requests.post(gemini_api_url, headers=headers, data=json.dumps(payload))
        response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)

        gemini_result = response.json()
        print(f"Received response from Gemini API: {gemini_result}")

        # Parse the Gemini API response
        sentiment = "unknown" # Default sentiment
        if gemini_result.get('candidates') and len(gemini_result['candidates']) > 0:
            first_candidate = gemini_result['candidates'][0]
            if first_candidate.get('content') and first_candidate['content'].get('parts'):
                first_part = first_candidate['content']['parts'][0]
                if first_part.get('text'):
                    sentiment = first_part['text'].lower().strip()
        else:
            print(f"Warning: Gemini API response did not contain expected 'candidates' structure: {gemini_result}")
            return jsonify({"error": "Failed to parse AI model response. Unexpected structure."}), 500

        print(f"Predicted sentiment: {sentiment}")
        return jsonify({"sentiment": sentiment}), 200

    except requests.exceptions.RequestException as e:
        error_message = f"Error calling Gemini API: {e}"
        if response and response.text:
            error_message += f" (Response: {response.text[:200]})"
        print(error_message)
        return jsonify({"error": f"Failed to connect to AI model or AI model returned an error: {e}"}), 500
    except json.JSONDecodeError as e:
        print(f"JSON decoding error from Gemini API response: {e}")
        return jsonify({"error": f"Failed to decode AI model response. It might not be JSON: {e}"}), 500
    except Exception as e:
        print(f"An unexpected internal server error occurred: {e}", exc_info=True)
        return jsonify({"error": f"An unexpected internal server error occurred: {e}"}), 500


@app.route('/analyze_bulk_reviews', methods=['POST'])
def analyze_bulk_reviews():
    """
    API endpoint to receive a list of movie review texts,
    call the Gemini API for sentiment for each, and return aggregated sentiment counts.
    """
    if not request.is_json:
        print("Error: Bulk request is not JSON.")
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.get_json()
    reviews = data.get('reviews')

    if not reviews or not isinstance(reviews, list):
        print("Error: Missing or invalid 'reviews' list in bulk request.")
        return jsonify({"error": "Missing or invalid 'reviews' list"}), 400

    if not GEMINI_API_KEY:
        print("Error: Gemini API Key is not set for bulk analysis.")
        return jsonify({"error": "Gemini API key is missing. Please set the GEMINI_API_KEY environment variable."}), 500

    sentiment_counts = Counter()
    processed_reviews = 0
    errors_encountered = 0

    for review_text in reviews:
        if not isinstance(review_text, str) or not review_text.strip():
            print(f"Skipping invalid review in bulk analysis: {review_text}")
            continue # Skip empty or non-string reviews

        try:
            prompt = (
                f"Classify the sentiment of the following movie review as either "
                f"'positive', 'negative', or 'neutral'. "
                f"Respond with only one word: positive, negative, or neutral.\n\n"
                f"Review: \"{review_text}\""
            )
            chat_history = [{"role": "user", "parts": [{"text": prompt}]}]
            payload = {"contents": chat_history}

            gemini_api_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
            gemini_api_url += f"?key={GEMINI_API_KEY}"

            headers = {
                'Content-Type': 'application/json'
            }

            response = requests.post(gemini_api_url, headers=headers, data=json.dumps(payload), timeout=30) # Add timeout
            response.raise_for_status()

            gemini_result = response.json()

            sentiment = "neutral" # Default to neutral if AI cannot classify or unexpected format
            if gemini_result.get('candidates') and len(gemini_result['candidates']) > 0:
                first_candidate = gemini_result['candidates'][0]
                if first_candidate.get('content') and first_candidate['content'].get('parts'):
                    first_part = first_candidate['content']['parts'][0]
                    if first_part.get('text'):
                        determined_sentiment = first_part['text'].lower().strip()
                        # Only count expected sentiments, default others to 'neutral' for charting
                        if determined_sentiment in ['positive', 'negative', 'neutral']:
                            sentiment = determined_sentiment
            
            sentiment_counts[sentiment] += 1
            processed_reviews += 1

        except requests.exceptions.RequestException as e:
            print(f"Error analyzing review '{review_text[:50]}...': {e}")
            sentiment_counts['error'] += 1 # Count errors
            errors_encountered += 1
        except Exception as e:
            print(f"Unexpected error for review '{review_text[:50]}...': {e}", exc_info=True)
            sentiment_counts['error'] += 1
            errors_encountered += 1

    print(f"Bulk analysis complete. Processed {processed_reviews} reviews with {errors_encountered} errors.")
    return jsonify({
        "sentiment_distribution": dict(sentiment_counts),
        "total_processed": processed_reviews,
        "total_errors": errors_encountered
    }), 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
