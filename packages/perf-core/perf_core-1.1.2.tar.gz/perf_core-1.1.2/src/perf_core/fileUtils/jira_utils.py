from logging import info

import requests
import hashlib
from datetime import datetime

JIRA_URL = "https://lastbrand.atlassian.net"
SEARCH_ENDPOINT = f"{JIRA_URL}/rest/api/2/search"
COMMENT_ENDPOINT = f"{JIRA_URL}/rest/api/2/issue/{{}}/comment"
CREATE_ISSUE_ENDPOINT = f"{JIRA_URL}/rest/api/2/issue"
BROWSE_ENDPOINT = f"{JIRA_URL}/browse/"

def jira_api_call(method, url, payload, auth):
    headers = {"Content-Type": "application/json"}
    if method == "POST":
        response = requests.post(url, json=payload, headers=headers, auth=auth)
    else:
        response = requests.get(url, headers=headers, params=payload, auth=auth)
    return response

def get_hash(input_string):
    return hashlib.sha256(input_string.encode()).hexdigest()


def create_jira_request_body(user_id, project_key, method_type, endpoint, jira_description, jira_identifier_hash):

    def truncate_string(input_str, max_length):
        return input_str[:max_length] if len(input_str) > max_length else input_str

    request_body = {
        "fields": {
            "assignee": {
                "id": user_id
            },
            "project": {
                "key": "TEQ"
            },
            "issuetype": {
                "name": "Bug"
            },
            "summary": truncate_string(f"Load Testing Failure - <{method_type}> {endpoint}",
                                       100),
            "description": truncate_string(jira_description, 50000),
            "labels": ["Load-testing", jira_identifier_hash]
        }
    }
    return request_body

def create_new_jira_issue( request_payload, auth):
    response = jira_api_call("POST", CREATE_ISSUE_ENDPOINT, request_payload,auth)
    jira_key = response.json()['key']
    jira_ticket_url = f"{BROWSE_ENDPOINT}{jira_key}"
    info(f"New Jira Ticket URL: {jira_ticket_url}")
    return response.json()

def get_search_jira_payload(hash_key, project_key):
    return {
        "fields": ["summary", "comment","status"],
        "fieldsByKeys": False,
        "jql": (f"project = {project_key} AND issuetype in (Bug) AND status not in "
                "(Done, DONE, Rejected) AND summary ~ \"Load Testing Failure\" "
                f"AND labels = {hash_key} order by created DESC"),
        "maxResults": 15,
        "startAt": 0
    }


def generate_jira(jira_description, jira_identifiers,method,endpoint,user_id,auth):
    jira_identifier_hash = get_hash(jira_identifiers)
    search_payload = get_search_jira_payload(jira_identifier_hash, "TEQ")
    search_response = jira_api_call("GET", SEARCH_ENDPOINT, search_payload,auth)
    search_results = search_response.json()
    jira_payload = create_jira_request_body(user_id,"TEQ",method,endpoint,jira_description,jira_identifier_hash)
    if search_results['total'] > 0:
        # Jira issue exists
        print("Jira ticket already exists")
        jira_key = search_results['issues'][0]['key']
        jira_ticket_url = f"{BROWSE_ENDPOINT}{jira_key}"
        print(f"Jira Ticket URL: {jira_ticket_url}")

        issue_status = search_results['issues'][0]['fields']['status']['name']
        if issue_status not in ["Closed", "Done","Resolved"]:
            comment_count = 0
            comments = search_results['issues'][0]['fields']['comment']['comments']
            if comments:
                comment_count = sum(
                    1 for comment in comments if comment['body'].startswith("Load Testing Failure")
                )
            comment_count += 1
            comment_text = f"Load Testing Failure Occurred Again at {datetime.now().strftime('%Y-%b-%d %I:%M:%S %p')}, Count: {comment_count}"+jira_description
            comment_payload = {"body": comment_text}
            comment_url = COMMENT_ENDPOINT.format(jira_key)
            comment_response = jira_api_call("POST", comment_url, comment_payload,auth)
            print(f"Added comment to Jira: {comment_text}")
        else:
            create_new_jira_issue(jira_payload,auth)
    else:
        create_new_jira_issue(jira_payload,auth)
