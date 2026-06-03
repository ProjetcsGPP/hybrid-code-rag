from collections import Counter
import json

with open("report_artifacts/external_nodes.json") as f:
    data = json.load(f)

counter = Counter()

for item in data:
    if not item.startswith("external::UNRESOLVED::"):
        continue

    symbol = item.split("::")[-1]

    if "." in symbol:
        counter[symbol.split(".")[-1]] += 1
    else:
        counter[symbol] += 1

for name, qty in counter.most_common(100):
    print(f"{qty:4d} {name}")
