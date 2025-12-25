import csv
import json
from io import StringIO
from typing import List, Any

def to_json(data: List[Any]) -> str:
    return json.dumps(data, indent=4, ensure_ascii=False)

def to_csv(data: List[dict]) -> str:
    if not data:
        return ""
    
    output = StringIO()
    writer = csv.DictWriter(output, fieldnames=data[0].keys())
    writer.writeheader()
    writer.writerows(data)
    return output.getvalue()