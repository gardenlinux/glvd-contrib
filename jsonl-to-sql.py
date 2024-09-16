import json
import string
import html

printable = set(string.printable)

def attribute_value_or_null(obj, attr):
    try:
        val = obj[attr]
        if isinstance(val, list):
            # fixme: handle cases of array length != 1
            element = val[0]
            values = ', '.join('\'' + item + '\'' for item in element.values())
            return f"ARRAY[({values})::{attr}]"

        # metrics is a dict
        # converting this seems to me more complex
        # if isinstance(val, dict):
        #     return 'foo'

        if isinstance(val, str):
            txt = html.escape(val, True)
            txt = ''.join(filter(lambda x: x in printable, txt))
            return f"'{txt}'"
    except:
        return 'null'


def object_to_sql_insert(table_name, obj, columns):
    values = []
    for c in columns:
        values.append(attribute_value_or_null(obj, c))
    return f'INSERT INTO {table_name} ({",".join(columns)}) VALUES ({",".join(values)});'


with open('few-cve.jsonl', 'r') as f:
    for line in f:
        cve = json.loads(line)
        print(object_to_sql_insert('cve_item', cve, 
            ['id', 'sourceIdentifier', 'vulnStatus', 'published', 'lastModified', 'evaluatorComment',
                'evaluatorSolution', 'cisaExploitAdd', 'cisaActionDue', 'cisaRequiredAction', 'cisaVulnerabilityName',
                'cveTags', 'descriptions', 'references']
                                    )
        )
