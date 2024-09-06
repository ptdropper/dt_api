import argparse
import configparser
import os

import dependencytrack


# Use the Dependency Track Administrator Team and enable the following capabilities

#    POLICY_MANAGEMENT
#    POLICY_VIOLATION_ANALYSIS
#    VIEW_POLICY_VIOLATION


def dt_api_read_config():
    """Read configuration data from a file

    :return: a list of configuration data
    :rtype: list()
    :raises DependencyTrackApiError: if the REST call failed
    """
    path = 'config.ini'
    isExist = os.path.isfile(path)
    if (isExist == False):
        print('Creating config.ini with default content, please edit the file to add values.')
        f = open(path, "w")
        f.write("[Dependency_Track_Server_Host]\n")
        f.write("host_name = <replace with server hosting Dependency Track>\n")
        f.write("api_key = <replace with the Administrator Team API Key value>\n")
        f.close()
        exit(1)
    # Create a ConfigParser object
    config = configparser.ConfigParser()
    config.read(path)

    # Access values from the configuration file
    host_name = config.get('Dependency_Track_Server_Host', 'host_name')
    api_key = config.get('Dependency_Track_Server_Host', 'api_key')

    # Return a dictionary with the retrieved values
    config_values = {
        'host_name': host_name,
        'api_key': api_key,
    }
    return config_values


# user input is needed for the following
# 1. the server name/ip address provided by config.ini
# 2. the Dependency Track project name
# 3. the project version

config_data = dt_api_read_config()
dt_api_host_name = config_data['host_name']
dt_api_key = config_data['api_key']

parser = argparse.ArgumentParser(description="<product name> <product version>")
parser.add_argument("product_name", type=str)
parser.add_argument("product_version", type=str)
args = parser.parse_args()

print(args.product_name)
print(args.product_version)

# Be certain that the following url does not end with a forward slash "/'
url = "http://" + str(dt_api_host_name) + ":8081"

try:
    # creates the required connection to Dependency track
    dt = dependencytrack.DependencyTrack(url, dt_api_key)
except:
    print("Cannot connect to server.")
    exit(-1)

try:
    response = []
    response = dt.search_project(args.product_name)
except dependencytrack.DependencyTrackApiError:
    print("Cannot find project doing a search on the name provided.")
    exit(-2)

prod_uuid = 0
x = len(response)
if len == 0:
    print("Nothing found for this search ")
    exit(-3)

for x in range(x):
    response_dict = {}
    response_dict = dict(response.pop())
    prod_version = str(args.product_version)
    found_version = str(response_dict["version"])
    if prod_version == found_version:
        prod_uuid = response_dict["uuid"]
        print("Found version ", response_dict["version"], "match to uuid", prod_uuid)
        break

dt.get_project_vdr(prod_uuid, args.product_name, args.product_version)
dt.get_product_policy_violations(prod_uuid, args.product_name, args.product_version)
