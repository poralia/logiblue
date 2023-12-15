import requests
import os

from whoosh import fields
from whoosh.fields import Schema
from whoosh.index import create_in
from whoosh.qparser import QueryParser

from django.conf import settings
from django.db.models import F

from apps.tracking.models import Category


class RajaOngkir:
    apikey = '61dedaeff0758d8ab4b11135231059e1'
    base_url_api = 'https://api.rajaongkir.com/starter'
    search_city_scheme = Schema(
        city_id=fields.TEXT(stored=True),
        province_id=fields.TEXT(stored=True),
        province=fields.TEXT(stored=True),
        type=fields.TEXT(stored=True),
        city_name=fields.TEXT(stored=True),
        postal_code=fields.TEXT(stored=True),
    )
    default_origin = "152"  # from Jakarta Pusat

    def __init__(self) -> None:
        pass

    @property
    def session(self):
        s = requests.Session()
        s.headers.update({'key': self.apikey})

        return s

    def get_cities(self, search=None):
        url = self.base_url_api + '/city'
        r = self.session.get(url)
        results = r.json().get('rajaongkir', {}).get('results', [])
        search_results = self.search_city(search, results)
        ret = {
            'status_code': r.status_code,
            'data': search_results,
        }

        return ret

    def search_city(self, search, documents):
        results = []
        index_file = settings.BASE_DIR.parent.parent / 'search-index'
        if not os.path.exists(index_file):
            os.mkdir(index_file)

        index = create_in(index_file, self.search_city_scheme)
        writer = index.writer()

        for doc in documents:
            writer.add_document(
                city_id=doc['city_id'],
                city_name=doc['city_name'],
                province_id=doc['province_id'],
                province=doc['province'],
                type=doc['type'],
                postal_code=doc['postal_code']
            )
        writer.commit()

        if search is not None:
            query_parser = QueryParser('city_name', self.search_city_scheme)
            query = query_parser.parse(search)

            with index.searcher() as searcher:
                res = searcher.search(query, limit=5, terms=True)
                for r in res:
                    results.append(dict(r))

            return results
        return documents

    def get_tiki(self, x):
        if x.get('code') == 'tiki':
            return x
        return None

    def get_tiki_eco(self, x):
        if x.get('service') == 'ECO':
            return x
        return None

    def calculate(self, country_code, category_id, weight, destination_id):
        category = Category.objects \
            .prefetch_related('country') \
            .select_related('country') \
            .filter(country__iso_code=country_code, id=category_id) \
            .annotate(cost=F('price_per_kilo') * weight) \
            .first()

        if not category:
            return None

        url = self.base_url_api + '/cost'
        payload = {
            'origin': self.default_origin,
            'destination': destination_id,
            'weight': weight,
            'courier': ["tiki"],
        }

        r = self.session.post(url, data=payload)
        rajaongkir = r.json().get('rajaongkir', {})
        results = rajaongkir.get('results', [])
        origin_details = rajaongkir.get('origin_details', {})
        destination_details = rajaongkir.get('destination_details', {})

        # use ECO service from TIKI
        # for demo purpose only
        tiki = next(filter(self.get_tiki, results), None)
        tiki_eco = next(filter(self.get_tiki_eco, tiki.get('costs', [])), None)
        tiki_eco_cost = tiki_eco.get('cost')[0].get('value')

        ret = {
            'status_code': r.status_code,
            'data': {
                'origin': category.country.name,
                'origin_details': origin_details,
                'destination_details': destination_details,
                'destination': destination_id,
                'category_name': category.title,
                'international_shipping_price': category.cost,
                'domestic_price': tiki_eco_cost,
                'total_price': tiki_eco_cost + category.cost,
                # 'domestic_shippings': results,
            },
        }

        return ret
