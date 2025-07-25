# airline_demand_app/app.py
import os
import random
import datetime
import json
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS # Import CORS
import requests

app = Flask(__name__)
CORS(app) # Enable CORS for all routes

# --- Mock Data Generation ---
def generate_mock_data(num_routes=5, num_days=30):
    """Generates mock airline booking demand data."""
    cities = ["Sydney", "Melbourne", "Brisbane", "Perth", "Adelaide", "Gold Coast", "Canberra", "Hobart"]
    routes = []
    for _ in range(num_routes):
        origin = random.choice(cities)
        destination = random.choice([c for c in cities if c != origin])
        routes.append({'origin': origin, 'destination': destination})

    data = {
        'popular_routes': [],
        'price_trends': [],
        'high_demand_periods': []
    }

    # Generate popular routes with simulated demand
    for i, route in enumerate(routes):
        demand = random.randint(500, 2000) + (i * 200) # Some routes are more popular
        data['popular_routes'].append({
            'route': f"{route['origin']}-{route['destination']}",
            'demand': demand,
            'avg_price': round(random.uniform(150, 600), 2)
        })
    # Sort popular routes by demand
    data['popular_routes'] = sorted(data['popular_routes'], key=lambda x: x['demand'], reverse=True)

    # Generate price trends for each popular route
    start_date = datetime.date.today() - datetime.timedelta(days=num_days)
    for route_data in data['popular_routes']:
        route_name = route_data['route']
        base_price = route_data['avg_price']
        for i in range(num_days):
            current_date = start_date + datetime.timedelta(days=i)
            # Simulate price fluctuations
            price_change = random.uniform(-0.1, 0.1) * base_price
            current_price = max(100, base_price + price_change) # Ensure price doesn't go too low
            # Add a peak for weekends or specific dates
            if current_date.weekday() >= 4 or current_date.day in [1, 15]: # Friday, Saturday, or specific dates
                current_price *= random.uniform(1.05, 1.2)
            data['price_trends'].append({
                'date': current_date.strftime('%Y-%m-%d'),
                'route': route_name,
                'price': round(current_price, 2)
            })

    # Generate high demand periods/locations
    demand_factors = {
        'Christmas Holidays': 1.8, 'New Year': 1.7, 'Easter Break': 1.5,
        'School Holidays (Jan)': 1.4, 'Long Weekends': 1.3
    }
    locations_with_events = ["Sydney", "Melbourne", "Gold Coast"]
    for period, factor in demand_factors.items():
        location = random.choice(locations_with_events)
        data['high_demand_periods'].append({
            'period': period,
            'location': location,
            'demand_factor': factor,
            'notes': f"Expect {int((factor-1)*100)}% higher demand in {location} during {period}."
        })

    return data

# --- Gemini API Integration ---
def get_gemini_insights(data):
    """Calls Gemini API to get insights from processed data."""
    # Construct a detailed prompt based on the mock data
    prompt = "Analyze the following airline booking market demand data and provide actionable insights.\n\n"
    prompt += "Popular Routes:\n"
    for route in data['popular_routes']:
        prompt += f"- {route['route']}: Demand {route['demand']}, Avg Price ${route['avg_price']}\n"

    prompt += "\nPrice Trends (sample for first few entries):\n"
    for i, trend in enumerate(data['price_trends'][:10]): # Limit to first 10 for brevity in prompt
        prompt += f"- {trend['date']} {trend['route']}: ${trend['price']}\n"
    if len(data['price_trends']) > 10:
        prompt += "(... more price trend data ...)\n"

    prompt += "\nHigh Demand Periods:\n"
    for period in data['high_demand_periods']:
        prompt += f"- {period['period']} in {period['location']}: Demand Factor {period['demand_factor']} ({period['notes']})\n"

    prompt += "\nBased on this data, provide insights on:\n"
    prompt += "1. Overall demand trends (e.g., growing, stable, declining).\n"
    prompt += "2. Key popular routes and why they might be popular.\n"
    prompt += "3. Price changes and patterns (e.g., peak times, dips).\n"
    prompt += "4. Specific high-demand periods/locations and their implications for hostels.\n"
    prompt += "5. Any actionable recommendations for hostels based on these trends.\n"
    prompt += "Keep the response concise and focused on market demand for hostels."

    # Use the provided API call structure for Gemini
    chat_history = [{ "role": "user", "parts": [{ "text": prompt }] }]
    payload = { "contents": chat_history }
    api_key = os.environ.get("GEMINI_API_KEY", "") # Get API key from environment variable
    api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"

    try:
        response = requests.post(api_url, headers={'Content-Type': 'application/json'}, json=payload)
        response.raise_for_status()  # Raise an exception for HTTP errors
        result = response.json()
        if result.get('candidates') and result['candidates'][0].get('content') and result['candidates'][0]['content'].get('parts'):
            return result['candidates'][0]['content']['parts'][0]['text']
        else:
            return "Could not generate insights. Unexpected API response structure."
    except requests.exceptions.RequestException as e:
        print(f"Error calling Gemini API: {e}")
        return f"Error connecting to AI service: {e}. Please ensure your GEMINI_API_KEY is set correctly."
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return f"An unexpected error occurred: {e}"


# --- Flask Routes ---
@app.route('/')
def index():
    """Renders the main web application page."""
    return render_template('index.html')

@app.route('/api/data')
def get_data():
    """Endpoint to provide mock data to the frontend."""
    mock_data = generate_mock_data()
    return jsonify(mock_data)

@app.route('/api/insights', methods=['POST'])
def get_insights():
    """Endpoint to get AI-generated insights."""
    data = request.json
    if not data:
        return jsonify({'error': 'No data provided for insights'}), 400

    insights = get_gemini_insights(data)
    return jsonify({'insights': insights})

if __name__ == '__main__':
    # For local development, you can set GEMINI_API_KEY in your environment
    # Example: export GEMINI_API_KEY='YOUR_API_KEY_HERE'
    # Or, for quick testing, uncomment the line below and replace with your key
    # os.environ['GEMINI_API_KEY'] = 'YOUR_GEMINI_API_KEY'
    app.run(debug=True, port=5000)

