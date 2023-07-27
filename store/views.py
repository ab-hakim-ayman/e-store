from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.db.models import Q
from django.utils import timezone
from django.http import Http404
from .models import *
from .serializers import *


class CategoryView(APIView):
    def get_category(self, pk):
        return Category.objects.get(id=pk)
    
    def get(self, request, pk=None):
        context = {
            'request':request
        }  
        if pk:
            category = self.get_category(pk)
            serializer = CategorySerializer(category, context=context)
        else:
            category = Category.objects.all()
            serializer = CategorySerializer(category, many=True, context=context)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, pk=None):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):
        category = self.get_category(pk)
        serializer = CategorySerializer(category, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        category = self.get_category(pk)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
        
class BrandView(APIView):
    def get_brand(self, pk):
        try:
            return Brand.objects.get(id=pk)
        except Brand.DoesNotExist:
            raise Http404
        
    def get(self, request, pk=None):
        context = {
            'request': request
        }
        if pk:
            brand = self.get_brand(pk)
            serializer = BrandSerializer(brand, context=context)
        else:
            brand = Brand.objects.all()
            serializer = BrandSerializer(brand, many=True, context=context)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, pk=None):
        serializer = BrandSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self,request, pk):
        brand = self.get_brand(pk)
        serializer = BrandSerializer(brand, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        brand = self.get_brand(pk)
        brand.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
class ProductView(APIView):
    def get_product(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            raise Http404
    
    def get(self, request, pk=None):
        context = {
            'request': request
        }
        if pk:
            product = self.get_product(pk)
            serializer = ProductSerializer(product, context=context)
        else:
            product = Product.objects.all()
            serializer = ProductSerializer(product, many=True, context=context)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, pk=None):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):
        product = self.get_product(pk)
        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        product = self.get_product(pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class CategoryProductView(APIView):
    def get(self, request):
        context = {
            'request': request
        }
        categories = Category.objects.all()
        category_serializer = CategorySerializer(categories, many=True).data
        data = []
        for ctg in category_serializer:
            product_objects = Product.objects.filter(category=ctg['id'])
            ctg['products'] = ProductSerializer(product_objects, many=True, context=context).data
            data.append(ctg['products'])
        return Response(data)


class SingleCategoryProductView(APIView):
    def get(self, request, pk=None):
        context = {
          'request': request
        }
        category = Category.objects.get(id=pk)
        category_serializer = CategorySerializer(category).data
        data = []
        product_objects = Product.objects.filter(category=category_serializer['id'])
        products = ProductSerializer(product_objects, many=True, context=context).data
        data.append(products)
        return Response(data)
    
class BrandProductView(APIView):
    def get(self, request):
        context = {
           'request': request
        }
        brands = Brand.objects.all()
        brand_serializer = BrandSerializer(brands, many=True).data
        data = []
        for brand in brand_serializer:
            product_objects = Product.objects.filter(brand=brand['id'])
            brand['products'] = ProductSerializer(product_objects, many=True, context=context).data
            data.append(brand['products'])
        return Response(data)
    
class SingleBrandProductView(APIView):
    def get(self, request, pk=None):
        context = {
         'request': request
        }
        brand = Brand.objects.get(id=pk)
        brand_serializer = BrandSerializer(brand).data
        data = []
        product_objects = Product.objects.filter(brand=brand_serializer['id'])
        products = ProductSerializer(product_objects, many=True, context=context).data
        data.append(products)
        return Response(data)
    

class Visits(APIView):
    def get(self, request, pk=None):
        context = {
            'request' : request
        }
        data = []
        products = Product.objects.get(id=pk)
        product_serializer = ProductSerializer(products, context=context).data
        print(product_serializer)
        # return Response(product_serializer['id'])
        visit = Visit.objects.filter(product=product_serializer['id'])
        visit_serializer = VisitSerializer(visit, many=True).data
        print(visit)
        # if visit:
        #     visit['view'] = visit.view
        # else:
        #     visit['view'] = 0
        # review_objects = Review.objects.filter(product=product_serializer['id'])
        # review = ReviewSerializer(review_objects).data
        # data.append(review)
        return Response(visit_serializer)