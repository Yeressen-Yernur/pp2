import json

with open(r"C:\Users\PC\Desktop\pp2\practice 4\JSON\sample-data.json") as f:
    data = json.load(f)

print("Interface Status")
print("=" * 80)
print("{:<50} {:<20} {:<7} {:<6}".format("DN", "Description", "Speed", "MTU"))
print("-" * 80)

for item in data["imdata"]:
    attr = item["l1PhysIf"]["attributes"]
    print("{:<50} {:<20} {:<7} {:<6}".format(attr["dn"], attr["descr"], attr["speed"], attr["mtu"]))