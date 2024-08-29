import sys
import socket
import datetime
import json

# Check for Python version compatibility
if sys.version_info[0] < 3:
    # Python 2 imports
    import urllib2
    import json

    def make_post_request(url, data, headers):
        req = urllib2.Request(url, json.dumps(data), headers)
        try:
            response = urllib2.urlopen(req)
            return response.read()
        except urllib2.HTTPError as e:
            return e.read()

else:
    # Python 3 imports
    import urllib.request as urllib2
    import json

    def make_post_request(url, data, headers):
        req = urllib2.Request(url, json.dumps(data).encode('utf-8'), headers)
        try:
            with urllib2.urlopen(req) as response:
                return response.read().decode('utf-8')
        except urllib2.HTTPError as e:
            return e.read().decode('utf-8')

# Function to read log file and extract data based on keyword


def read_log_file(log_file_path, keyword):
    extracted_data = {}

    with open(log_file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            if keyword in line:
                # Extract the required information
                extracted_data['extracted_value'] = line.split(
                    keyword + ': ')[-1].strip()
                break  # Assuming you need only the first match

    return extracted_data


# Fetch the hostname and current date and time
hostname = socket.gethostname()
current_time = datetime.datetime.now().isoformat()

# Load the configuration file
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

# Iterate over each team's configuration
for team, settings in config.items():
    log_file_path = settings['log_file_path']
    keyword = settings['keyword']

    # Extract data from the log file
    log_data = read_log_file(log_file_path, keyword)

    # Define the URL, data, and headers
    url = 'https://api.example.com/endpoint'
    data = {
        'team': team,
        'hostname': hostname,
        'current_time': current_time
    }
    # Merge the extracted log data into the main data dictionary
    data.update(log_data)

    headers = {
        'api-key': 'your-api-key',
        'content-type': 'application/json'
    }

    # Make the POST request
    response = make_post_request(url, data, headers)
    print(f"Response for {team}: {response}")
