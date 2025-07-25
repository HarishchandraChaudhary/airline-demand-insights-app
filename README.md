Airline Booking Market Demand Dashboard
Project Overview
This web application is designed to provide hostel owners in Australia with actionable insights into airline booking market demand trends. By analyzing key metrics like popular routes, price fluctuations, and high-demand periods, the tool aims to help hostels strategically adjust their offerings and pricing.

Important Note: Due to the inherent challenges and cost associated with accessing real-time, comprehensive, and free airline booking APIs, this demonstration utilizes robustly simulated market demand data. This approach allows for a full showcase of the application's core functionality, including data processing, visualization, and AI-driven insights, without relying on external, often paid, data sources.

Key Features
Data Simulation: Generates realistic mock data covering popular routes, historical price trends, and identified high-demand periods/locations.

AI-Powered Insights: Integrates with the Google Gemini API to intelligently analyze the simulated data, extracting concise and actionable insights relevant to the hostel industry (e.g., overall demand trends, specific route popularity drivers, price patterns, and implications of peak periods).

Intuitive Web Interface: A user-friendly dashboard built with Flask, HTML, Tailwind CSS, and Chart.js, providing clear visualizations through:

Interactive tables for popular routes and high-demand periods.

A dynamic line chart illustrating flight price trends over time for various routes.

A dedicated section for displaying AI-generated market analysis.

Actionable Data Processing: Cleans and processes the raw (simulated) data to highlight:

Top popular routes.

Evolution of prices for key routes.

Identified high-demand periods and their associated locations.

Responsive Design: The interface is designed to be fully responsive, ensuring optimal viewing and usability across various devices (mobile, tablet, desktop).

Demo
(Optional: If you deploy your app, replace this with a live demo link and a screenshot.)

Live Demo: [Link to your live deployed application (e.g., Heroku, Render)]

Screenshot:
(Replace this with an actual screenshot of your running application)

Project Structure
airline_demand_app/
├── app.py                  # Flask backend application logic
├── requirements.txt        # Python dependencies
├── templates/
│   └── index.html          # Frontend HTML template
└── static/
    ├── css/
    │   └── style.css       # Custom CSS (minimal, mostly Tailwind)
    └── js/
        └── app.js          # Frontend JavaScript for data fetching and charts

Setup and Running Instructions
Follow these steps to get the application running on your local machine.

Prerequisites
Python 3.7+

pip (Python package installer)

git (for cloning the repository)

1. Clone the Repository
Open your terminal or command prompt and run:

git clone https://github.com/HarishchandraChaudhary/airline-demand-insights-app
cd airline-demand-insights-app

(Important: Replace YourUsername with your actual GitHub username and airline-demand-insights-app with your repository's exact name.)

2. Set Up a Virtual Environment (Recommended)
It's best practice to use a virtual environment to manage project dependencies, keeping them isolated from your system's global Python packages.

python3 -m venv venv

Activate the virtual environment:

On macOS/Linux:

source venv/bin/activate

On Windows (Command Prompt):

venv\Scripts\activate.bat

On Windows (PowerShell):

.\venv\Scripts\Activate.ps1

You'll know it's active when you see (venv) at the beginning of your terminal prompt.

3. Install Dependencies
With your virtual environment activated, install the required Python libraries listed in requirements.txt:

pip install -r requirements.txt

4. Obtain a Google Gemini API Key
This application uses the Google Gemini API to generate insights. You'll need an API key to use this service.

Go to Google AI Studio.

Sign in with your Google account.

Generate a new API key. Copy this key.

5. Set the Gemini API Key Environment Variable
The application reads the Gemini API key from an environment variable named GEMINI_API_KEY. This is the most secure way to handle API keys and prevents them from being exposed in your code.

On macOS/Linux:

export GEMINI_API_KEY='YOUR_GEMINI_API_KEY_HERE'

On Windows (Command Prompt):

set GEMINI_API_KEY=YOUR_GEMINI_API_KEY_HERE

On Windows (PowerShell):

$env:GEMINI_API_KEY='YOUR_GEMINI_API_KEY_HERE'

Important: Replace YOUR_GEMINI_API_KEY_HERE with the actual API key you obtained in Step 4. This command sets the variable for the current terminal session. If you open a new terminal, you'll need to set it again. For persistence across sessions, you would typically add this line to your shell's profile file (e.g., .bashrc, .zshrc, config.fish, or set it as a permanent System Environment Variable on Windows).

6. Run the Flask Application
Make sure you are in the airline-demand-insights-app directory and your virtual environment is activated.

python app.py

You should see output similar to this, indicating the Flask development server is running:

 * Serving Flask app 'app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: XXX-XXX-XXX

7. Access the Web Application
Open your web browser and navigate to:

http://127.0.0.1:5000/ or http://localhost:5000/

Usage
Upon loading the application, you will see a dashboard populated with simulated data for popular routes, high-demand periods, and an interactive chart showing price trends. To get AI-powered analysis of this data, simply click the "Generate Insights" button at the bottom of the page. The AI-generated insights will appear in the "AI-Generated Market Insights" section.

Technologies Used
Backend: Python 3.x, Flask (Web Framework), requests (for API calls), Flask-CORS

Frontend: HTML5, Tailwind CSS (for rapid styling), JavaScript, Chart.js (for data visualization), Luxon (for date handling in charts)

AI Integration: Google Gemini API (for natural language processing and insights generation)

Problem-Solving & Design Choices
Data Source Limitation: The core challenge was the unavailability of free, real-time, and comprehensive airline booking data APIs. My solution addresses this by implementing a robust mock data generation system within app.py. This allows the application to fully demonstrate its data processing, visualization, and AI integration capabilities, fulfilling the project's requirements without incurring costs or relying on unreliable external sources. This approach ensures the application's functionality is proven, and it can be easily adapted to real data if a suitable source becomes available in the future.

AI Integration: The Gemini API was chosen for its strong natural language understanding and generation capabilities, enabling the extraction of meaningful, actionable insights from the structured data.

User Experience (UX): The interface prioritizes clarity and ease of use. Tailwind CSS was chosen for rapid and responsive styling, ensuring a clean and modern look across devices. Chart.js provides interactive and clear data visualizations.

Modularity: The project is structured into logical components (backend, templates, static assets) for maintainability and scalability.

Future Improvements
Integration with Real Data: Explore partnerships or paid APIs for actual airline booking data to transition from simulated data.

Advanced Filtering: Implement more granular filtering options for routes, dates, and demand factors.

Historical Data Analysis: Store and analyze historical data to identify long-term trends and seasonality more accurately.

User Authentication: Add user login capabilities to save preferences or custom reports.

Alerts & Notifications: Implement a system to notify hostel owners about significant price changes or demand spikes.

More Sophisticated Data Scraping: If allowed, develop custom scrapers for publicly available, non-API flight data sources, being mindful of terms of service and ethical scraping practices.

Feel free to customize any part of this README.md to better reflect your specific implementation or additional insights you gained during the project!
