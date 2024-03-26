from dependencytrack import DependencyTrack
import argparse

# Magic number alert, this is the official API Key from our Dependency Track user interface
api_key = 'XrnGcCSFoCzhHFX7vWu0hD4IisDeFrQl'

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
# creates the required connection to Dependency track
dt = DependencyTrack(url, api_key)

response = dt.search_project(args.product_name)
prod_uuid = 0
for x in range(0, 10):
    if response[x]["version"] == args.product_version:
        prod_uuid = response[x]["uuid"]
        break

dt.get_project_vdr(prod_uuid)
