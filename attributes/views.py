from django.shortcuts import get_object_or_404, render
from .models import Family, Category, Brand, Product, ProductAttribute
from .serializers import FamilySerializer, CategorySerializer, BrandSerializer, ProductSerializer, ProductAttributeSerializer
from rest_framework import generics, status,serializers
from rest_framework.response import Response
from django.views import View
from django.http import Http404, JsonResponse
from django.db.models import Q

class HomePageView(View):
    def get(self, request):
        families = Family.objects.all()
        categories = []
        brands = []
        products = []
        selected_family = request.GET.get('family')
        selected_category = request.GET.get('category')
        selected_brand = request.GET.get('brand')

        if selected_family:
            categories = Category.objects.filter(family=selected_family)
            if selected_category:
                brands = Brand.objects.filter(Q(category__family=selected_family) & Q(category=selected_category))
                if selected_brand:
                    products = Product.objects.filter(brand=selected_brand)
            else:
                brands = Brand.objects.filter(category__family=selected_family)
        else:
            categories = Category.objects.all()
            brands = Brand.objects.all()

        context = {'families': families, 'categories': categories, 'brands': brands, 'products': products}
        return render(request, 'home.html', context)

    
    # def update_product_attributes(request, product_id):
    #     product = get_object_or_404(Product, id=product_id)
    #     print(product)
    #     if request.method == 'PATCH':
    #         attributes = request.POST.get('attributes')
    #         print(attributes)

    #         for attr_name, attr_value in attributes.items():
    #             # Get or create the product attribute
    #             product_attribute, created = ProductAttribute.objects.get_or_create(
    #                 product=product,
    #                 name=attr_name
    #             )

    #             # Update the attribute value and save the product attribute
    #             product_attribute.value = attr_value
    #             product_attribute.save()

    #         response_data = {
    #             'status': 'success',
    #             'message': 'Product attributes updated successfully.',
    #         }

    #         return JsonResponse(response_data)





# Familiy List and Create views 

class FamilyList(generics.ListCreateAPIView):
    queryset = Family.objects.all()
    serializer_class = FamilySerializer

    def get(self, request, *args, **kwargs):
        try:
            families = self.get_queryset()
            serializer = self.serializer_class(families, many=True)
            response_data = {
                'status': 'success',
                'message': 'All Families retrieved successfully.',
                'data': serializer.data
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                serializer.save()
                response_data = {
                    'status': 'success',
                    'message': f'Familiy "{serializer.data["name"]}" Created successfully.',
                }
                return Response(response_data, status=status.HTTP_201_CREATED)  
        except serializers.ValidationError as e:
            error_message = e.detail[0] if isinstance(e.detail, list) else e.detail
            return Response({'message': error_message}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Family Retrive Update and delete views
class FamilyDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Family.objects.all()
    serializer_class = FamilySerializer

    def get(self, request, *args, **kwargs):
        try:
            family = self.get_object()
            serializer = self.serializer_class(family)
            response_data = {
                'status': 'success',
                'message': 'Family retrieved successfully.',
                'data': serializer.data
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except Family.DoesNotExist:
            return Response({'message': 'Family not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, *args, **kwargs):
        try:
            family = self.get_object()
            print(request.data)
            serializer = self.serializer_class(family, data=request.data)
            if serializer.is_valid():
                serializer.save()
                response_data = {
                    'status': 'success',
                    'message': f"Family '{serializer.data['name']}' Updated successfully.",
                    'data': serializer.data
                }
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Family.DoesNotExist:
            return Response({'message': 'Family not found.'}, status=status.HTTP_404_NOT_FOUND)
        except serializers.ValidationError as e:
            error_message = e.detail[0] if isinstance(e.detail, list) else e.detail
            return Response({'message': error_message}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



    def delete(self, request, *args, **kwargs):
        try:
            family = self.get_object()
            family.delete()
            response_data = {
                'status': 'success',
                'message': 'Family deleted successfully.'
            }
            return Response(response_data, status=status.HTTP_204_NO_CONTENT)
        except Family.DoesNotExist:
            return Response({'message': 'Family not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Category  list and create Views
class CategoryList(generics.ListCreateAPIView):
    serializer_class = CategorySerializer

    def get_queryset(self):
        family_id = self.request.query_params.get('family', None)
        if family_id is not None:
            queryset = Category.objects.filter(family=family_id)
        else:
            queryset = Category.objects.all()
        return queryset

    def get(self, request, *args, **kwargs):
        try:
            # get the selected family id from the query parameters
            family_id = request.query_params.get('family', None)
            
            # filter the queryset based on the selected family
            if family_id is not None:
                categories = Category.objects.filter(family=family_id)
            else:
                categories = self.get_queryset()
            
            serializer = self.serializer_class(categories, many=True)
            response_data = {
                'status': 'success',
                'message': 'Categories retrieved successfully.',
                'data': serializer.data
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            error_message = 'An error occurred while retrieving categories. Please try again later.'
            return Response({'message': error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



    def post(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                serializer.save()
                response_data = {
                    'status': 'success',
                    'message': f"Category '{serializer.data['name']}' created successfully.",
                    'data': serializer.data
                }
                return Response(response_data, status=status.HTTP_201_CREATED)     
        except serializers.ValidationError as e:
            error_message = e.detail[0] if isinstance(e.detail, list) else e.detail
            return Response({'message': error_message}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            error_message = 'An error occurred while creating the category. Please try again later.'
            return Response({'message': error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Category Retrive Update and delete views
class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get(self, request, *args, **kwargs):
        try:
            category = self.get_object()
            serializer = self.serializer_class(category)
            response_data = {
                'status': 'success',
                'message': 'Category retrieved successfully.',
                'data': serializer.data
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            error_message = 'An error occurred while retrieving the category. Please try again later.'
            return Response({'message': error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, *args, **kwargs):
        try:
            category = self.get_object()
            serializer = self.serializer_class(category, data=request.data)
            if serializer.is_valid():
                serializer.save()
                response_data = {
                    'status': 'success',
                    'message': f"Category '{serializer.data['name']}' updated successfully.",
                    'data': serializer.data
                }
                return Response(response_data, status=status.HTTP_200_OK)
        except serializers.ValidationError as e:
            error_message = e.detail[0] if isinstance(e.detail, list) else e.detail
            return Response({'message': error_message}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            error_message = 'An error occurred while updating the category. Please try again later.'
            return Response({'message': error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, *args, **kwargs):
        try:
            category = self.get_object()
            category.delete()
            response_data = {
                'status': 'success',
                'message': 'Category deleted successfully.'
            }
            return Response(response_data, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            error_message = 'An error occurred while deleting the category. Please try again later.'
            return Response({'message': error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Brand List  and Create views
class BrandList(generics.ListCreateAPIView):
    serializer_class = BrandSerializer

    def get_queryset(self):
        queryset = Brand.objects.all()
        family_id = self.request.query_params.get('family', None)
        category_id = self.request.query_params.get('category', None)
        
        if family_id is not None:
            queryset = queryset.filter(product__category__family=family_id)
        if category_id is not None:
            queryset = queryset.filter(product__category=category_id)

        return queryset.distinct()




    def get(self, request, *args, **kwargs):
        try:
            brands = self.get_queryset()
            serializer = self.serializer_class(brands, many=True)
            response_data = {
                'status': 'success',
                'message': 'Brand list retrieved successfully.',
                'data': serializer.data
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            error_message = 'An error occurred while retrieving the brand list. Please try again later.'
            return Response({'message': error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def post(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                serializer.save()
                response_data = {
                    'status': 'success',
                    'message': f"Brand '{serializer.data['name']}' created successfully.",
                    'data': serializer.data
                }
                return Response(response_data, status=status.HTTP_201_CREATED)
        except serializers.ValidationError as e:
            error_message = e.detail[0] if isinstance(e.detail, list) else e.detail
            return Response({'message': error_message}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            error_message = 'An error occurred while creating the brand. Please try again later.'
            return Response({'message': error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        
# Brand Retrive Update and delete Views
class BrandDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer

    def get(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.serializer_class(instance)
            response_data = {
                'status': 'success',
                'message': 'Brand retrieved successfully.',
                'data': serializer.data
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            error_message = 'An error occurred while retrieving the brand. Please try again later.'
            return Response({'message': error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

    def put(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.serializer_class(instance, data=request.data)
            if serializer.is_valid():
                serializer.save()
                response_data = {
                    'status': 'success',
                    'message': f"Brand '{serializer.data['name']}' updated successfully.",
                    'data': serializer.data
                }
                return Response(response_data, status=status.HTTP_200_OK)
        except serializers.ValidationError as e:
            error_message = e.detail[0] if isinstance(e.detail, list) else e.detail
            return Response({'message': error_message}, status=status.HTTP_400_BAD_REQUEST)   
        except Exception as e:
            error_message = 'An error occurred while updating the brand. Please try again later.'
            return Response({'message': error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

    def delete(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.delete()
            success_message = 'Brand deleted successfully.'
            response_data = {
                'status': 'success',
                'message': success_message
            }
            return Response(response_data, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            error_message = 'An error occurred while deleting the brand. Please try again later.'
            return Response({'message': error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class ProductList(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get(self, request, *args, **kwargs):
        try:
            brand_id = request.query_params.get('brand', None)
            family_id = request.query_params.get('family', None)

            # filter the queryset based on the selected brand and family
            queryset = self.get_queryset()
            if brand_id is not None:
                queryset = queryset.filter(brand=brand_id)
            if family_id is not None:
                queryset = queryset.filter(category__family=family_id)

            serializer = self.serializer_class(queryset, many=True)
            response_data = {
                'status': 'success',
                'message': 'Products retrieved successfully.',
                'data': serializer.data
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            error_message = 'An error occurred while retrieving the products. Please try again later.'
            return Response({'message': error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)






    def post(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                serializer.save()
                success_message = f'Product "{serializer.data["name"]}" created successfully.'
                response_data = {
                    'status': 'success',
                    'message': success_message,
                    'data': serializer.data
                }
                return Response(response_data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except serializers.ValidationError as e:
            error_message = e.detail[0] if isinstance(e.detail, list) else e.detail
            return Response({'message': error_message}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            error_message = f'An error occurred while creating the product. Error message: {str(e)}'
            return Response({'message': error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Product Retrive Update and Delete views
class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.serializer_class(instance)
            response_data = {
                'status': 'success',
                'message': 'Product retrieved successfully.',
                'data': serializer.data
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            error_message = 'The product you are looking for does not exist.'
            return Response({'message': error_message}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            error_message = 'An error occurred while retrieving the product. Please try again later.'
            return Response({'message': error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.serializer_class(instance, data=request.data)
            if serializer.is_valid():
                print(serializer.validated_data)  # <-- Add this line
                serializer.save()
                response_data = {
                    'status': 'success',
                    'message': f'Product "{serializer.data["name"]}" updated successfully.',
                    'data': serializer.data
                }
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except serializers.ValidationError as e:
            print(str(e))
            error_message = e.detail[0] if isinstance(e.detail, list) else e.detail
            return Response({'message': error_message}, status=status.HTTP_400_BAD_REQUEST)
        except Product.DoesNotExist:
            error_message = 'The product you are trying to update does not exist.'
            return Response({'message': error_message}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            error_message = f'An error occurred while updating the product. Error message: {str(e)}'
            print(error_message)
            return Response({'message': error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


        
    def patch(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.serializer_class(instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                response_data = {
                    'status': 'success',
                    'message': f'Product "{serializer.data["name"]}" attributes updated successfully.',
                    'data': serializer.data
                }
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Product.DoesNotExist:
            error_message = 'The product you are trying to update does not exist.'
            return Response({'message': error_message}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            error_message = f'An error occurred while updating the product . Error message: {str(e)}'
            print(error_message)
            return Response({'message': error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

   


    def delete(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            success_message = f'Product "{instance.name}" deleted successfully.'
            instance.delete()
            response_data = {
                'status': 'success',
                'message': success_message
            }
            return Response(response_data, status=status.HTTP_204_NO_CONTENT)
        except Product.DoesNotExist:
            error_message = 'The product you are trying to delete does not exist.'
            return Response({'message': error_message}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            error_message = 'An error occurred while deleting the product. Please try again later.'
            return Response({'message': error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Product Attributes List and Create Views
class ProductAttributeList(generics.ListCreateAPIView):
    queryset = ProductAttribute.objects.all()
    serializer_class = ProductAttributeSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        product_id = self.request.query_params.get('product', None)
        if product_id:
            queryset = queryset.filter(product_id=product_id)
        return queryset
    
    def get(self, request, *args, **kwargs):
        attributes = self.get_queryset()
        serializer = self.serializer_class(attributes, many=True)
        return Response({
            "status": "success",
            "message": "Product attributes retrieved successfully.",
            "data": serializer.data
        }, status=status.HTTP_200_OK)


    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": "success",
                "message": "Product attribute created successfully.",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                "status": "error",
                "message": "Unable to create product attribute.",
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

# Product Attributes Retrive update and delete views
class ProductAttributeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProductAttribute.objects.all()
    serializer_class = ProductAttributeSerializer

    def get_queryset(self):
        return ProductAttribute.objects.all()

    def get_object(self):
        attribute_id = self.kwargs.get('pk')
        try:
            attribute = ProductAttribute.objects.get(id=attribute_id)
        except ProductAttribute.DoesNotExist:
            raise Http404
        return attribute

    def get(self, request, *args, **kwargs):
        try:
            attribute = self.get_object()
            serializer = self.serializer_class(attribute)
            response_data = {
                'status': 'success',
                'message': 'Product attribute retrieved successfully.',
                'data': serializer.data
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except Http404:
            error_message = 'The product attribute you are looking for does not exist.'
            return Response({'message': error_message}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            error_message = 'An error occurred while retrieving the product attribute. Please try again later.'
            return Response({'message': error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




    def put(self, request, *args, **kwargs):
        attribute = self.get_object()
        serializer = self.serializer_class(attribute, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": "success",
                "message": "Product attribute updated successfully.",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "status": "error",
                "message": "Unable to update product attribute.",
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, *args, **kwargs):
        attribute = self.get_object()
        serializer = self.serializer_class(attribute, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": "success",
                "message": "Product attribute updated successfully.",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "status": "error",
                "message": "Unable to update product attribute.",
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        try:
            attribute = self.get_object()
        except Http404:
            return Response({"message": "The product attribute you are trying to delete does not exist."}, status=status.HTTP_404_NOT_FOUND)
        
        attribute.delete()
        
        return Response({
            "status": "success",
            "message": "Product attribute deleted successfully."
        }, status=status.HTTP_204_NO_CONTENT)

