import re

with open("raw.txt", "r", encoding="utf-8") as file:
    text = file.read()
#1
prices = re.findall(r"\d[\d\s]*,\d{2}", text)

print(prices)

#2
products = re.findall(r"\d+\.\s+(.*?)\n\d+,\d{3}", text , re.DOTALL)

print(products)

#3
matches = re.findall(r"(\d+,\d+) x (\d[\d\s]*,\d{2})", text)

total = 0

for qty_str, price_str in matches:
    qty = float(qty_str.replace(",","."))
    price = float(price_str.replace(" ","").replace(",","."))

    total += qty * price

print(total)

#4
match = re.search(r"Время:\s*(\d{2}\.\d{2}\.\d{4})\s+(\d{2}:\d{2}:\d{2})", text)

date = match.group(1)
time = match.group(2)
print(f"Date: {date}")
print(f"Time: {time}")

#5
payment_method = re.findall(r"Банковская карта|Наличные", text)
p = payment_method[0]
print(f"Payment method: {p}")

#6
import json

items = []

for i in range(len(products)):
    unit_price = float(prices[i].replace(" ","").replace(",","."))
    items.append({
        "name": products[i].strip(),
        "unit_price": unit_price
    })
receipt_data = {
    "date": date,
    "time": time,
    "items": items,
    "total_amount": total,
    "payment_method": p
}

print(json.dumps(receipt_data,ensure_ascii=False, indent=4))