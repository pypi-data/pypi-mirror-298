import json
import csv
import requests



def write_output_to_file(out_data, filename="data_output.json"):
    with open(filename, "w") as json_file:
        json.dump(out_data, json_file)


def write_html_report(file_path, url):
    response =requests.get(url, stream=True)
    if response.status_code == 200:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(response.text)
        print(f"Report saved to {file_path}")
    else:
        print(f"Failed to fetch the report. Status code: {response.status_code}")


def remove_options_method(data):
    method_list = data.get('Method', [])
    indices_to_remove = [i for i, method in enumerate(method_list) if method.strip().lower() == 'options']

    if not indices_to_remove:
        return data
    filtered_data = {}
    for key, value_list in data.items():
        filtered_data[key] = [v for i, v in enumerate(value_list) if i not in indices_to_remove]

    return filtered_data


def parse_csv(file_path):
    parsed_data = []

    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            method = row['Method']
            name = row['Name']
            error = row['Error']

            # Find the endpoint starting from the first '/'
            endpoint_start = name.find('/')
            if endpoint_start != -1:
                endpoint = name[endpoint_start:]  # Extracting from '/' onwards
                # Append [method, endpoint, error] as a single sublist
                parsed_data.append([method, endpoint, error])

    return parsed_data

