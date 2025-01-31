import pandas as pd
from datetime import datetime
from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
from collections import defaultdict


DATE_OF_CREATION = 1920


def get_years_text(year_with_us):
    if 11 <= year_with_us % 100 <= 14:
        return f"Уже {year_with_us} лет с вами"
    elif year_with_us % 10 == 1:
        return f"Уже {year_with_us} год с вами"
    elif 2 <= year_with_us % 10 <= 4:
        return f"Уже {year_with_us} года с вами"
    else:
        return f"Уже {year_with_us} лет с вами"


def main():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('template.html')
    year_with_us = datetime.now().year - DATE_OF_CREATION
    wine_excel = pd.read_excel('wine.xlsx', keep_default_na=False)
    products = wine_excel.to_dict(orient='records')
    products_by_category = defaultdict(list)
    for row in products:
        products_by_category[row['Категория']].append(row)
    rendered_page = template.render(
        products_by_category=products_by_category,
        year_with_us=get_years_text(year_with_us),
    )
    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)
    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == '__main__':
    main()
