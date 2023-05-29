from rest_framework import serializers
from .models import Family, Category, Brand, Product, ProductAttribute


class FamilySerializer(serializers.ModelSerializer):
    class Meta:
        model = Family
        fields = ('id', 'name')

    def create(self, validated_data):
        name = validated_data['name']
        try:
            family = Family.objects.get(name=name)
        except Family.DoesNotExist:
            family = Family.objects.create(**validated_data)
            return family
        raise serializers.ValidationError(f"Family with name '{name}' already exists.")

    def update(self, instance, validated_data):
        try:
            name = validated_data.get('name', instance.name)
            if Family.objects.filter(name=name).exclude(id=instance.id).exists():
                raise serializers.ValidationError(f"Family with name '{name}' already exists.")
            
            instance.name = name
            instance.save()
            return instance
        except Exception:
            raise serializers.ValidationError(f"Family with name '{name}' already exists.")


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'family')

    def create(self, validated_data):
        try:
            name = validated_data['name']
            family = validated_data['family']
            if Category.objects.filter(name=name, family=family).exists():
                raise serializers.ValidationError(f"Category with name '{name}' already exists for family {family}.")
            category = Category.objects.create(name=name, family=family)
            return category
        except Exception :
            raise serializers.ValidationError(f"Category with name '{name}' already exists for family {family}.")

    def update(self, instance, validated_data):
        try:
            name = validated_data.get('name', instance.name)
            family = validated_data.get('family', instance.family)
            if Category.objects.filter(name=name, family=family).exclude(id=instance.id).exists():
                raise serializers.ValidationError(f"Category with name '{name}' already exists in this family.")
            return super().update(instance, validated_data)
        except Exception:
            raise serializers.ValidationError(f"Category with name '{name}' already exists for family {family}.")


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ('id', 'name')
        
    def create(self, validated_data):
        name = validated_data['name']
        try:
            brand = Brand.objects.get(name=name)
        except Brand.DoesNotExist:
            brand = Brand.objects.create(**validated_data)
            return brand
        error_message = f"A brand with the name '{name}' already exists."
        raise serializers.ValidationError(error_message)

    def update(self, instance, validated_data):
        try:
            name = validated_data.get('name', instance.name)
            if Brand.objects.filter(name=name).exclude(id=instance.id).exists():
                raise serializers.ValidationError(f"A brand with the name '{name}' already exists.")
            
            instance.name = name
            instance.save()
            return instance
        except Exception:
            raise serializers.ValidationError(f"A brand with the name '{name}' already exists.")


class ProductAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAttribute
        fields = ('id', 'name', 'value', 'product')
        extra_kwargs = {
            'name': {'required': False},
            'value': {'required': False},
            'product': {'required': False},
        }

    def validate(self, attrs):
        instance = self.instance
        name = attrs.get('name')
        value = attrs.get('value')

        # Check if the attribute name and value are unique for this product
        if instance and name and value:
            existing_attrs = instance.product.attributes.filter(
                name=name, value=value).exclude(id=instance.id)
            if existing_attrs.exists():
                raise serializers.ValidationError(
                    f'The attribute "{name}" with value "{value}" already exists for this product.')

        return attrs



        


class ProductSerializer(serializers.ModelSerializer):
    attributes = ProductAttributeSerializer(many=True, required=False)

    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'price','family', 'category', 'brand', 'attributes')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        try:
            category = instance.category
            if category is not None:
                representation['category'] = category.name
        except Category.DoesNotExist:
            representation['category'] = None
        try:
            brand = instance.brand
            if brand is not None:
                representation['brand'] = brand.name
        except Brand.DoesNotExist:
            representation['brand'] = None
        # try:
        #     family = instance.family
        #     if family is not None:
        #         representation['family'] = family.name
        # except Family.DoesNotExist:
        #     representation['family'] = None
        attributes = representation['attributes']
        
        for attr in attributes:
            if 'name' in attr:
                name = attr.pop('name', None)
                attr_dict = {
                    'id': attr.get('id'),
                    name: attr.pop('value', None),
                }
                attr.clear()
                attr.update(attr_dict)
        return representation



    def create(self, validated_data):
        name = validated_data['name']
        try:
            product = Product.objects.get(name=name)
            raise serializers.ValidationError(f"A product with the name '{name}' already exists.")
        except Product.DoesNotExist:
            attributes_data = validated_data.pop('attributes', [])
            product = Product.objects.create(**validated_data)
            for attribute_data in attributes_data:
                name = attribute_data.get('name')
                value = attribute_data.get('value')
                if name and value:
                    existing_attrs = product.attributes.filter(name=name, value=value)
                    if existing_attrs.exists():
                        raise serializers.ValidationError(
                            f'The attribute "{name}" with value "{value}" Duplicate  for this product.')
                ProductAttribute.objects.create(product=product, **attribute_data)
            return product

    def update(self, instance, validated_data):
        attributes_data = validated_data.pop('attributes', [])
        instance = super().update(instance, validated_data)

        # Update or create new attributes
        for attribute_data in attributes_data:
            name = attribute_data.get('name')
            value = attribute_data.get('value')
            if name is not None:
                try:
                    attribute = instance.attributes.get(name=name)
                    attribute.value = value
                    attribute.save()
                except ProductAttribute.DoesNotExist:
                    ProductAttribute.objects.get_or_create(product=instance, **attribute_data)

        return instance
    

    def validate(self, data):
        attributes = data.get('attributes', [])
        names = set()
        for attribute in attributes:
            name = attribute.get('name')
            if name in names:
                raise Exception(f"Attribute name '{name}' appears multiple times")
            else:
                names.add(name)
        return data

    


