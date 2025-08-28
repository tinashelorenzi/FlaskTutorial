from flask import Flask, render_template, request, redirect, url_for
import os
from datetime import datetime

app = Flask(__name__)

# VULNERABILITY: No secret key set properly for session security
app.secret_key = 'weak-key'

@app.route('/')
def index():
    return render_template('vulnerable_form.html')

@app.route('/submit', methods=['POST'])
def submit_form():
    # Get form data - NO SANITIZATION
    name = request.form.get('name', '')
    email = request.form.get('email', '')
    message = request.form.get('message', '')
    
    # Save to text file (vulnerable to injection in file content)
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    data_entry = f"""
=== New Entry [{timestamp}] ===
Name: {name}
Email: {email}
Message: {message}
{'=' * 50}

"""
    
    filename = 'submissions.txt'
    with open(filename, 'a', encoding='utf-8') as file:
        file.write(data_entry)
    
    # VULNERABILITY: Pass unsanitized user input directly to template
    return render_template('vulnerable_success.html', 
                         user_name=name, 
                         user_email=email, 
                         user_message=message)

@app.route('/view_submissions')
def view_submissions():
    try:
        with open('submissions.txt', 'r', encoding='utf-8') as file:
            content = file.read()
        # VULNERABILITY: Display file content without escaping
        return render_template('view_submissions.html', submissions=content)
    except FileNotFoundError:
        return render_template('view_submissions.html', submissions="No submissions yet.")

@app.route('/search')
def search():
    query = request.args.get('q', '')
    # VULNERABILITY: Reflect search query without escaping
    return render_template('search_results.html', query=query)

if __name__ == '__main__':
    if not os.path.exists('templates'):
        os.makedirs('templates')
    
    # VULNERABILITY: Debug mode in production
    app.run(debug=True, host='0.0.0.0')