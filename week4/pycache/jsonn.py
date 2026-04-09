import json

with open("Prac04/sample-data.json") as f:
    data = json.load(f)

print("Interface Status")
print("=" * 90)
print(f"{'DN':55} {'Description':15} {'Speed':10} {'MTU':5}")
print("-" * 90)

for item in data["imdata"]:
    attrs = item["l1PhysIf"]["attributes"]

    dn = attrs.get("dn", "")
    descr = attrs.get("descr", "")
    speed = attrs.get("speed", "")
    mtu = attrs.get("mtu", "")

    print(f"{dn:55} {descr:15} {speed:10} {mtu:5}")