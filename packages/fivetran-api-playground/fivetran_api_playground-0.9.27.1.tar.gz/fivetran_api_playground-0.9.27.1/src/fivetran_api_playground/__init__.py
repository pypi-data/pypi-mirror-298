import uuid
import argparse
from flask import Flask, jsonify, request, Response
from faker import Faker
from datetime import datetime, timedelta
import random
from collections import OrderedDict
import json

__version__ = "0.9.27.1"
VALID_COMMANDS = ["start"]

app = Flask(__name__)
fake = Faker()

# Sample data
items = []
MAX_RECORDS = 50
for index in range(MAX_RECORDS):
    record_creation_time = datetime.now() - timedelta(hours=MAX_RECORDS - index, minutes=random.randint(0, 59),
                                                      seconds=random.randint(0, 59))
    user = OrderedDict([
        ('id', str(uuid.uuid4())),
        ('name', fake.name()),
        ('email', fake.email()),
        ('address', fake.address()),
        ('company', fake.company()),
        ('job', fake.job()),
        ('createdAt', record_creation_time.strftime(
            '%Y-%m-%dT%H:%M:%SZ')),
        ('updatedAt',
         (record_creation_time + timedelta(minutes=random.randint(0, 59), seconds=random.randint(0, 59))).strftime(
             '%Y-%m-%dT%H:%M:%SZ'))
    ])
    items.append(user)

DEFAULT_ORDER_BY = 'updatedAt'
DEFAULT_ORDER_TYPE = 'asc'
DEFAULT_PAGE_SIZE = 10


# Custom JSON encoder to preserve order
class CustomJSONEncoder(json.JSONEncoder):
    def encode(self, obj):
        if isinstance(obj, OrderedDict):
            return json.dumps(obj, indent=4, separators=(',', ': '))
        return super().encode(obj)


@app.route('/pagination/next_page_url', methods=['GET'])
def get_items():
    # Get filters from query parameters
    order_by_arg = request.args.get('order_by', type=str,
                                    default=DEFAULT_ORDER_BY)  # createdAt, updatedAt [Default updatedAt]
    order_type_arg = request.args.get('order_type', type=str, default=DEFAULT_ORDER_TYPE)  # asc, desc [Default asc]
    per_page_arg = request.args.get('per_page', type=int, default=DEFAULT_PAGE_SIZE)  # [1-50] Default 10
    updated_since_arg = request.args.get('updated_since', type=str)

    # Validate `order_by` value
    if order_by_arg not in ['createdAt', 'updatedAt']:
        return jsonify({"error": "Invalid value for 'order_by'. Use 'createdAt' or 'updatedAt'"}), 400

    # Validate `order_type` value
    if order_type_arg not in ['asc', 'desc']:
        return jsonify({"error": "Invalid value for 'order_type'. Use 'asc' or 'desc'"}), 400

    # Validate `per_page` value
    if not (1 <= per_page_arg <= 50):
        return jsonify({"error": "Invalid value for 'per_page'. It should be between 1 and 50."}), 400

    # Filter items based on the updated_since parameter
    filtered_items = items
    if updated_since_arg:
        try:
            # Ensure the format ends with 'Z' indicating UTC
            if updated_since_arg.endswith('Z'):
                updated_since_arg = updated_since_arg[:-1]  # Strip the 'Z' before parsing
                updated_since_date = datetime.strptime(updated_since_arg, "%Y-%m-%dT%H:%M:%S")
                updated_since_date = updated_since_date.replace(tzinfo=None)  # Set the timezone to UTC
            else:
                return jsonify({"error": "Invalid date format for 'updated_since'. Must end with 'Z' for UTC"}), 400

            # Convert 'updatedAt' to datetime for comparison
            filtered_items = [item for item in items if
                              datetime.strptime(item['updatedAt'][:-1], "%Y-%m-%dT%H:%M:%S") >= updated_since_date]
        except ValueError:
            return jsonify({"error": "Invalid date format for 'updated_since'. Use 'YYYY-MM-DDTHH:MM:SSZ'"}), 400

    # Sort the filtered items
    reverse_order = (order_type_arg == 'desc')
    filtered_items.sort(key=lambda x: x[order_by_arg], reverse=reverse_order)

    # Pagination logic
    page = request.args.get('page', default=1, type=int)
    start_index = (page - 1) * per_page_arg
    end_index = start_index + per_page_arg
    paginated_items = filtered_items[start_index:end_index]

    # Next page logic
    next_page_url = None
    if end_index < len(filtered_items):
        next_page_url = f"{request.base_url}?page={page + 1}&per_page={per_page_arg}&order_by={order_by_arg}&order_type={order_type_arg}"
        if updated_since_arg:
            next_page_url += f"&updated_since={updated_since_arg}Z"  # Add 'Z' back for the next page

    response = {
        'data': paginated_items,
        'total_items': len(filtered_items),
        'page': page,
        'per_page': per_page_arg,
        'next_page_url': next_page_url
    }

    return Response(json.dumps(response, cls=CustomJSONEncoder), mimetype='application/json')


def main():
    """The main entry point for the script.
    Parses command line arguments and passes them to connector object methods
    """

    parser = argparse.ArgumentParser(allow_abbrev=False)

    parser.add_argument("command", help="|".join(VALID_COMMANDS))
    parser.add_argument("--port", type=int, default=None, help="Provide the port on which you want to run the API on "
                                                               "localhost")
    args = parser.parse_args()
    port = args.port if args.port else 5001

    if args.command.lower() == "start":
        print("Start Local API on port " + str(port) + "\n")
        print("You can read the API documentation on: "
              "https://gist.github.com/varundhall/7dfcfecf85fa35db4fa8bb58f5e7fbbb")
        app.run(debug=True, port=port)

    else:
        raise NotImplementedError(f"Invalid command: {args.command}, see `api_playground --help`")


if __name__ == "__main__":
    main()
