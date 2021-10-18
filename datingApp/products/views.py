from django.shortcuts import render
from bs4 import BeautifulSoup
import requests

from products.models import CategoryLevel1, CategoryLevel2, Product
from rest_framework import status

from rest_framework.response import Response
from rest_framework.views import APIView


class ParseCategories(APIView):
    def get(self, request, format=None):
        url = 'https://www.citilink.ru/catalog/'
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        for a in soup.find_all('a', class_='CatalogLayout__link_level-1'):
            url = a['href']
            name = a.find('span', class_='CatalogLayout__category-title').getText()
            name = ' '.join(name.split())

            r = requests.get(url)
            soup = BeautifulSoup(r.text, 'html.parser')

            category_level_1 = CategoryLevel1(name=name, url=url)
            category_level_1.save()
            for a in soup.find_all('a', class_='CatalogCategoryCard__link'):
                url = a['href']
                name = a.getText()
                name = ' '.join(name.split())
                category_level_2 = CategoryLevel2(name=name, url=url)
                category_level_2.save()
                category_level_1.categories_child.add(category_level_2)
            category_level_1.save()

        return Response(status=status.HTTP_200_OK)


class ParseCategory(APIView):
    def get(self, request, slug, *args, **kwargs):
        url = f'https://www.citilink.ru/catalog/{slug}/'
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        for product in soup.find_all('div', class_='product_data__gtm-js'):
            title = product.find('a', class_='ProductCardHorizontal__title').getText().replace('  ', ' ')
            price = product.find('span', class_='ProductCardHorizontal__price_current-price').getText().replace(' ', '').replace('\n', '')
            img_url = product.find('img', class_='ProductCardHorizontal__image')['src']

            #  если по выбранному url нету категории в бд, то объект product сохраняется без этого поля
            try:
                category = CategoryLevel2.objects.get(url=url)
                product = Product(title=title, price=price, photo_url=img_url, category=category)
                # category = get_object_or_404(CategoryLevel2, url=url)
            except Exception:
                product = Product(title=title, price=price, photo_url=img_url)

            product.save()

        return Response(status=status.HTTP_200_OK)
