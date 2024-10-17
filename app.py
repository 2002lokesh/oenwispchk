import platform
import subprocess
from flask import Flask, render_template, request

app = Flask(__name__)

# Function to run a Ping command with IPv4 or IPv6
def ping(host, ip_version):
    if platform.system() == "Windows":
        command = ['ping', '-6', host] if ip_version == 'ipv6' else ['ping', host]
    else:
        # Use '-c 4' to send 4 packets in Linux/Mac
        command = ['ping', '-c', '4', '-6', host] if ip_version == 'ipv6' else ['ping', '-c', '4', host]
    
    try:
        result = subprocess.run(command, capture_output=True, text=True, timeout=90)  # Timeout set to 10 seconds
        return result.stdout
    except subprocess.TimeoutExpired:
        return "Ping command timed out."

# Function to run Traceroute command with IPv4 or IPv6 and extended timeout
def traceroute(host, ip_version):
    if platform.system() == "Windows":
        command = ['tracert', '-6', host] if ip_version == 'ipv6' else ['tracert', host]
    else:
        command = ['traceroute', '-6', host, '-w', '4'] if ip_version == 'ipv6' else ['traceroute', host, '-w', '4']

    try:
        # Remove the timeout argument to let it take as long as needed
        result = subprocess.run(command, capture_output=True, text=True)
        return result.stdout
    except Exception as e:
        return f"Error running traceroute: {str(e)}"

# Function to simulate a BGP query (mockup)
def bgp_query(host):
    return f"Simulated BGP query for {host}."

@app.route('/', methods=['GET', 'POST'])
def index():
    output = None
    if request.method == 'POST':
        query_type = request.form['query_type']
        host = request.form['host']
        ip_version = request.form.get('ip_version', 'ipv4')  # Default to 'ipv4'
        
        if query_type == 'ping':
            output = ping(host, ip_version)
        elif query_type == 'traceroute':
            output = traceroute(host, ip_version)
        elif query_type == 'bgp':
            output = bgp_query(host)
        else:
            output = 'Invalid query type selected.'
    
    return render_template('index.html', output=output)

if __name__ == '__main__':
    app.run(debug=True)
