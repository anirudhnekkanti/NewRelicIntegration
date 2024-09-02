import sys
import socket
import datetime
import json
import logging

# Setup logging
logging.basicConfig(filename='log_monitor.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Check for Python version compatibility
if sys.version_info[0] < 3:
    # Python 2 imports
    import urllib2

    def make_post_request(url, data, headers):
        try:
            req = urllib2.Request(url, json.dumps(data), headers)
            response = urllib2.urlopen(req)
            return response.read()
        except urllib2.HTTPError as e:
            logging.error(f"HTTPError: {e.read()}")
            return e.read()
        except Exception as e:
            logging.error(f"Error: {str(e)}")
            return str(e)

else:
    # Python 3 imports
    import urllib.request as urllib2

    def make_post_request(url, data, headers):
        try:
            req = urllib2.Request(url, json.dumps(
                data).encode('utf-8'), headers)
            with urllib2.urlopen(req) as response:
                return response.read().decode('utf-8')
        except urllib2.HTTPError as e:
            logging.error(f"HTTPError: {e.read().decode('utf-8')}")
            return e.read().decode('utf-8')
        except Exception as e:
            logging.error(f"Error: {str(e)}")
            return str(e)

# Function to read log file and check for the keyword


def check_keyword_in_log(log_file_path, keyword):
    try:
        with open(log_file_path, 'r') as file:
            lines = file.readlines()
            for line in lines:
                if keyword in line:
                    return 1  # Keyword found
        return 0  # Keyword not found
    except Exception as e:
        logging.error(f"Error reading log file {log_file_path}: {str(e)}")
        return 0


try:
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

        # Check if the keyword is present in the log file
        keyword_present = check_keyword_in_log(log_file_path, keyword)

        # Define the URL, data, and headers
        url = 'https://api.example.com/endpoint'
        data = {
            'team': team,
            'hostname': hostname,
            'timestamp': current_time,
            'status': 'Processed',
            'value': keyword_present  # 1 if keyword found, otherwise 0
        }

        headers = {
            'api-key': 'your-api-key',
            'content-type': 'application/json'
        }

        # Make the POST request
        response = make_post_request(url, data, headers)
        logging.info(f"Response for {team}: {response}")

except Exception as e:
    logging.error(f"An unexpected error occurred: {str(e)}")
