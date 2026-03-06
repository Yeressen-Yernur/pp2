import json
import re

with open(r"C:\Users\PC\Desktop\pp2\practice 5\raw.txt", "r", encoding="utf-8") as f:
    text = f.read()

text = text.replace("\r\n", "\n")

prices = re.findall(r'\b\d[\d\s]*,\d{2}\b', text)
prices = [float(p.replace(" ", "").replace(",", ".")) for p in prices]

products = []
product_matches = re.findall(r'\n\d+\.\n(.*?)(?=\n\d+,\d{2}|\n\d+\.\n|\nСтоимость)', text, re.DOTALL)
for p in product_matches:
    products.append(p.strip().replace("\n", " "))

total_match = re.search(r'ИТОГО:\s*[\n ]*([\d\s]+,\d{2})', text)
total_amount = float(total_match.group(1).replace(" ", "").replace(",", ".")) if total_match else None

datetime_match = re.search(r'\d{2}\.\d{2}\.\d{4}\s+\d{2}:\d{2}:\d{2}', text)
datetime_info = datetime_match.group(0) if datetime_match else None

payment_match = re.search(r'Банковская карта', text)
payment_method = "Bank Card" if payment_match else "Unknown"

receipt_data = {
    "products": products,
    "prices": prices,
    "total_amount": total_amount,
    "datetime": datetime_info,
    "payment_method": payment_method
}

print(json.dumps(receipt_data, ensure_ascii=False, indent=4))