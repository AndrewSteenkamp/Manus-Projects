'''
# Director's Dashboard - Web Interface
# A simple Flask app to control the Autonomous UGC Agency.

from flask import Flask, render_template, request, jsonify
import sys
import os

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the main agency class
from autonomous_agency import AutonomousAgency

app = Flask(__name__)

# Initialize the agency - this creates a single instance for the web app
print("Initializing Autonomous Agency for the web dashboard...")
agency = AutonomousAgency()
print("Agency initialized.")

# Store reports in memory for the session
reports = []

@app.route('/')
def dashboard():
    """Render the main dashboard page."""
    # Pass the list of reports to the template
    return render_template('index.html', reports=reports)

@app.route('/run_daily_operations', methods=['POST'])
def run_daily_operations():
    """Endpoint to trigger one day of autonomous operations."""
    data = request.get_json()
    mode = data.get('mode', 'test') # 'test' or 'live'
    
    print(f"\n--- Received request to run daily operations in {mode.upper()} MODE ---")
    
    # In a real application, the mode would trigger different logic
    # For now, we run the same core logic but could add payment processing for 'live'
    if mode == 'live':
        print("WARNING: Live mode selected. Real transactions would be processed.")
    else:
        print("INFO: Test mode selected. No real money will be used.")

    # Run the agency's daily operations
    try:
        daily_report = agency.run_daily_operations()
        
        # Add a summary to the report for display
        report_summary = {
            "date": daily_report['date'],
            "ceo_decision": daily_report['ceo_decision']['decision'],
            "leads_found": daily_report['sales_results']['results']['total_leads_found'],
            "clients_onboarded": 1 if agency.clients else 0, # Simple logic for demo
            "revenue": daily_report['financial_status']['revenue'],
            "profit": daily_report['financial_status']['profit']
        }
        reports.insert(0, report_summary) # Add to the beginning of the list
        
        return jsonify({'status': 'success', 'report': report_summary})
    except Exception as e:
        print(f"ERROR: An error occurred during daily operations: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    # Create the templates directory and index.html if they don't exist
    if not os.path.exists('templates'):
        os.makedirs('templates')
    if not os.path.exists('templates/index.html'):
        with open('templates/index.html', 'w') as f:
            f.write('''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Director's Dashboard - Autonomous UGC Agency</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; background-color: #f0f2f5; color: #1c1e21; margin: 0; padding: 20px; }
        .container { max-width: 900px; margin: auto; background: #fff; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        h1, h2 { color: #0056b3; }
        h1 { text-align: center; }
        .controls { text-align: center; margin-bottom: 20px; padding: 20px; background: #f7f8fa; border-radius: 8px; border: 1px solid #ddd; }
        #run-button { background-color: #007bff; color: white; padding: 15px 30px; border: none; border-radius: 6px; font-size: 18px; cursor: pointer; transition: background-color 0.3s; }
        #run-button:hover { background-color: #0056b3; }
        #run-button:disabled { background-color: #ccc; cursor: not-allowed; }
        .toggle-switch { display: flex; justify-content: center; align-items: center; margin-bottom: 20px; }
        .toggle-switch span { margin: 0 10px; font-weight: bold; }
        .switch { position: relative; display: inline-block; width: 60px; height: 34px; }
        .switch input { opacity: 0; width: 0; height: 0; }
        .slider { position: absolute; cursor: pointer; top: 0; left: 0; right: 0; bottom: 0; background-color: #ccc; transition: .4s; border-radius: 34px; }
        .slider:before { position: absolute; content: ""; height: 26px; width: 26px; left: 4px; bottom: 4px; background-color: white; transition: .4s; border-radius: 50%; }
        input:checked + .slider { background-color: #28a745; }
        input:checked + .slider:before { transform: translateX(26px); }
        #reports-container { margin-top: 20px; }
        table { width: 100%; border-collapse: collapse; margin-top: 20px; }
        th, td { border: 1px solid #ddd; padding: 12px; text-align: left; }
        th { background-color: #f2f2f2; }
        .status { text-align: center; margin-top: 10px; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Director's Dashboard</h1>
        <h2>Autonomous UGC Agency</h2>

        <div class="controls">
            <div class="toggle-switch">
                <span id="test-label" style="color: #007bff;">🧪 Test Mode</span>
                <label class="switch">
                    <input type="checkbox" id="mode-toggle">
                    <span class="slider"></span>
                </label>
                <span id="live-label" style="color: #ccc;">💰 Live Mode</span>
            </div>
            <button id="run-button">Run 1 Day of Autonomous Operations</button>
            <div id="status" class="status"></div>
        </div>

        <div id="reports-container">
            <h2>Daily Reports</h2>
            <table>
                <thead>
                    <tr>
                        <th>Date</th>
                        <th>CEO Decision</th>
                        <th>Leads Found</th>
                        <th>Revenue</th>
                        <th>Profit</th>
                    </tr>
                </thead>
                <tbody id="reports-table-body">
                    <!-- Reports will be injected here by JavaScript -->
                </tbody>
            </table>
        </div>
    </div>

    <script>
        const runButton = document.getElementById('run-button');
        const statusDiv = document.getElementById('status');
        const modeToggle = document.getElementById('mode-toggle');
        const testLabel = document.getElementById('test-label');
        const liveLabel = document.getElementById('live-label');
        const reportsTableBody = document.getElementById('reports-table-body');

        let reports = [];

        modeToggle.addEventListener('change', function() {
            if(this.checked) {
                liveLabel.style.color = '#28a745';
                testLabel.style.color = '#ccc';
            } else {
                testLabel.style.color = '#007bff';
                liveLabel.style.color = '#ccc';
            }
        });

        runButton.addEventListener('click', function() {
            runButton.disabled = true;
            statusDiv.textContent = 'Running daily operations... Please wait.';
            statusDiv.style.color = '#ffc107';

            const mode = modeToggle.checked ? 'live' : 'test';

            fetch('/run_daily_operations', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ mode: mode })
            })
            .then(response => response.json())
            .then(data => {
                if(data.status === 'success') {
                    statusDiv.textContent = 'Daily operations completed successfully!';
                    statusDiv.style.color = '#28a745';
                    // Add new report to the top of the list
                    reports.unshift(data.report);
                    renderReports();
                } else {
                    statusDiv.textContent = `Error: ${data.message}`;
                    statusDiv.style.color = '#dc3545';
                }
            })
            .catch(error => {
                statusDiv.textContent = 'An unexpected error occurred.';
                statusDiv.style.color = '#dc3545';
                console.error('Error:', error);
            })
            .finally(() => {
                runButton.disabled = false;
            });
        });

        function renderReports() {
            reportsTableBody.innerHTML = ''; // Clear existing rows
            reports.forEach(report => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${new Date(report.date).toLocaleString()}</td>
                    <td>${report.ceo_decision}</td>
                    <td>${report.leads_found}</td>
                    <td>R ${report.revenue.toFixed(2)}</td>
                    <td style="color: ${report.profit >= 0 ? 'green' : 'red'};">R ${report.profit.toFixed(2)}</td>
                `;
                reportsTableBody.appendChild(row);
            });
        }

        // Initial render
        renderReports();
    </script>
</body>
</html>''')
    app.run(host='0.0.0.0', port=5000, debug=True)
'''
