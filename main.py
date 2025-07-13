# Content of main.py
import csv
import os # Import the 'os' module to access environment variables
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def web_calculator():
    names_data = {}
    rates_data = {}
    
    # Inlined CSV loading
    try:
        with open('names.csv', mode='r', newline='', encoding='utf-8') as f:
            names_data = {r['code'].strip(): r['name'].strip() for r in csv.DictReader(f)}
        with open('rates.csv', mode='r', newline='', encoding='utf-8') as f:
            rates_data = {r['code'].strip(): float(r['rate'].strip()) for r in csv.DictReader(f)}
    except Exception as e:
        return render_template('index.html', error_message=f"Server Error loading data: {e}")

    result = None
    error_message = None

    if request.method == 'POST':
        employee_code = request.form.get('employee_code', '').strip()
        rate_code = request.form.get('rate_code', '').strip()
        hours_str = request.form.get('hours_worked', '').strip()

        hours = 0.0
        try:
            hours = float(hours_str)
        except ValueError:
            error_message = "Invalid hours. Please enter a number."
            
        if not error_message:
            name = names_data.get(employee_code)
            rate = rates_data.get(rate_code)

            if name is None:
                error_message = f"Error: Employee code '{employee_code}' not found."
            elif rate is None:
                error_message = f"Error: Rate code '{rate_code}' not found."
            else:
                final_salary = rate * hours
                result = {
                    "name": name,
                    "employee_code": employee_code,
                    "salary": final_salary
                }
        
    return render_template('index.html', result=result, error_message=error_message)

# *** CRITICAL CHANGE HERE ***
# Get the port from the environment variable (Render provides this)
port = int(os.environ.get("PORT", 5000)) # Default to 5000 if not found (for local testing)
app.run(host='0.0.0.0', port=port)
