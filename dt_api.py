import argparse

import dependencytrack

# Magic number alert, this is the official API Key from our Dependency Track user interface
# for the instance on rdapps.bbraunlab.com use the Administrator Team and enable the following capabilities
#    POLICY_MANAGEMENT
#    POLICY_VIOLATION_ANALYSIS
#    VIEW_POLICY_VIOLATION

api_key = 'odt_mFmihpi8eKqFsrhj2xeIbkQQ0nMzD2h7'

# user input is needed for the following
# 1. the server name/ip address
# 2. the project name

parser = argparse.ArgumentParser(description="<DepTrack IP address> and <product name>")
parser.add_argument("user_url", type=str)
parser.add_argument("product_name", type=str)
parser.add_argument("product_version", type=str)
args = parser.parse_args()
print(args.user_url)
print(args.product_name)
print(args.product_version)

# Be certain that the following url does not end with a forward slash "/'
url = "http://" + str(args.user_url) + ":8081"

try:
    # creates the required connection to Dependency track
    dt = dependencytrack.DependencyTrack(url, api_key)
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
