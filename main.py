from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/parse', methods=['POST'])
def parse():
    try:
        json_data = request.json['jsonData']
        parsed_data = []

        for data in json_data:
            parsed = json.loads(data)
            parsed_data.append(parsed)

        vlan_ids = []

        for parsed_item in parsed_data:
            if isinstance(parsed_item, dict) and 'items' in parsed_item:
                items = parsed_item['items']
                vlan_ids.extend([
                    item['vn_instance']['vlan_id'] for item in items
                    if 'vn_instance' in item and 'vlan_id' in item['vn_instance'] and item['vn_instance']['vlan_id'] is not None
                ])

        # Remove duplicates and order the VLAN IDs numerically
        vlan_ids = sorted(set(vlan_ids))

        total_count = len(vlan_ids)

        return jsonify({'total_count': total_count, 'vlan_ids': vlan_ids})

    except ValueError:
        error_message = 'Invalid JSON data. Please check your input.'
        return jsonify({'error': error_message}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)