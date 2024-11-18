import yaml

# very rough prototype
# purpose:
# take triage/cve context data from a yaml file and insert it into the glvd db

items = yaml.load(open('sample.yaml'), Loader=yaml.FullLoader)

for item in items:
    # dists = item['dists']
    # for dist in dists:
    dist_id = 14 #fixme hardcoded for now

    cve_id = item['cve_id']
    for cve in cve_id:

        stmt = f"INSERT INTO public.cve_context (dist_id, cve_id, context_descriptor, description, is_resolved) VALUES('{dist_id}', '{cve}', '{item['descriptor']}', '{item['description']}', {item['is_resolved']});"

        print(stmt)
        # print(f"psql -t -U glvd -c \" {stmt} \" glvd")
