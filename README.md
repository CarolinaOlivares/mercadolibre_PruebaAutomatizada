
# mercadolibre_PruebaAutomatizada

Este proyecto realiza scraping en MercadoLibre México para buscar productos "PlayStation 5", filtrar por estado "Nuevo" y ubicación "CDMX", y ordenarlos por mayor precio.

## Requisitos

- Python 3.7+
- Google Chrome
- ChromeDriver (automatizado por webdriver-manager)

## Instalación

```bash
pip install -r requirements.txt
```

## Ejecución

```bash
python main.py
python generate_report.py
```

## Estructura

- `main.py` – Scraping completo
- `generate_report.py` – Informe HTML
- `screenshots/` – Capturas de pantalla
- `output/` – CSV y HTML generados
