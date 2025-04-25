
import pandas as pd
from datetime import datetime
df = pd.read_csv('output/results.csv')
html_content = """
<!DOCTYPE html>
<html lang="es"><head><meta charset="UTF-8"><title>Informe</title></head><body>
<h1>Informe Scraping MercadoLibre</h1><p>Fecha: 2025-04-25 00:27:07</p>
<table border="1"><tr><th>#</th><th>Nombre</th><th>Precio</th></tr>
"""
for i, row in df.iterrows():
    html_content += f"<tr><td>{i+1}</td><td>{row['Nombre']}</td><td>${row['Precio']}</td></tr>"
html_content += "</table></body></html>"
with open("output/report.html", "w", encoding="utf-8") as f:
    f.write(html_content)
