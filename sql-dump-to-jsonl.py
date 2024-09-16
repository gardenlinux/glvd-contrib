import json

"""
Script to convert a database dump into a jsonl file tht contains the results from the NIST api.
"""

with open('glvd.sql', 'r') as f:
    for line in f:
        if 'sourceIdentifier' in line:
            elements = line.split('\t')
            cve_json = elements[2].replace('\\"', '\"')
            try:
                cve = json.loads(cve_json)
            except:
                print(cve_json)
                continue
            with open('all-cve.jsonl', 'a+') as ff:
                ff.write(cve_json)
