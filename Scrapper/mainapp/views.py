from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .serializers import AmazonProductSerializer, FlipkartProductSerializer
import requests
from bs4 import BeautifulSoup

@api_view(['GET'])

def mainapp(request, search_query):
    HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US, en;q=0.5'
    }

    #amazon portion
    urlamazon = f"https://www.amazon.in/s?k={search_query.replace(' ', '+')}"
    response = requests.get(urlamazon, headers=HEADERS)
    print(response)
    soup = BeautifulSoup(response.text, 'html.parser')
    search_results = soup.select_one('.a-link-normal.s-underline-text.s-underline-link-text.s-link-style.a-text-normal')
    product_title = soup.select_one(".a-size-medium.a-color-base.a-text-normal")
    product_price = soup.select_one(".a-price-whole")
    product_img = soup.select_one(".a-section.aok-relative.s-image-fixed-height")
    img_tag = product_img.find('img')
    product_img_src = img_tag.get('src')

    #Flipkart portion
    urlflipkart = f"https://www.flipkart.com/search?q={search_query.replace(' ', '+')}"
    responsef = requests.get(urlflipkart, headers=HEADERS)
    print(responsef)
    soup = BeautifulSoup(responsef.text, 'html.parser')
    product_titlef = soup.select_one("._4rR01T")
    product_pricef = soup.select_one("._30jeq3._1_WHN1")
    product_imgf = soup.select_one(".CXW8mj")
    img_tagf = product_imgf.find('img')
    product_img_srcf = img_tagf.get('src')
    amazon_data = {
        "title": product_title.text,
        "price": product_price.text,
        "img": product_img_src
    }
    flipkart_data = {
        "title": product_titlef.text,
        "price": product_pricef.text,
        "img": product_img_srcf
    }

    amazon_serializer = AmazonProductSerializer(data=amazon_data)
    flipkart_serializer = FlipkartProductSerializer(data=flipkart_data)

    # Validate and return serialized data
    if amazon_serializer.is_valid() and flipkart_serializer.is_valid():
        serialized_data = {
            "amazon": amazon_serializer.data,
            "flipkart": flipkart_serializer.data
        }
        return Response(serialized_data)
    else:
        return Response({"error": "Serialization failed"}, status=status.HTTP_400_BAD_REQUEST)
