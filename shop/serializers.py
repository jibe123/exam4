from rest_framework import serializers

from .models import Shop, Product, Supplies, Sales


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('title', )


class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('title', 'description', 'price')


class SuppliesSerializer(serializers.ModelSerializer):
    product = serializers.StringRelatedField()

    class Meta:
        model = Supplies
        fields = ('product_id', 'product', 'quantity')


class SuppliesCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplies
        fields = ('product', 'shop', 'quantity')

    def create(self, validated_data):
        try:
            instance = Supplies.objects.get(
                product=validated_data['product'],
                shop=validated_data['shop'])
            if instance:
                instance.quantity += validated_data['quantity']
                instance.save()
                return instance
        except Supplies.DoesNotExist:
            return super().create(validated_data)


class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = '__all__'


class ShopDetailSerializer(serializers.ModelSerializer):
    supplies = SuppliesSerializer(many=True)

    class Meta:
        model = Shop
        fields = ('id', 'title', 'address', 'supplies')


class SalesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sales
        fields = ('product', 'shop', 'quantity')

    def create(self, validated_data):
        instance = Supplies.objects.get(
            product=validated_data['product'],
            shop=validated_data['shop'])
        if instance:
            if instance.quantity >= validated_data['quantity']:
                instance.quantity -= validated_data['quantity']
                instance.save()
                return validated_data
            else:
                raise serializers.ValidationError(
                    "Sorry, the quantity of product you requested is currently not available!")
