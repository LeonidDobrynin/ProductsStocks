from rest_framework import serializers

from logistic.models import Product, StockProduct, Stock


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['title', 'description']

    def create(self, validated_data):
        stock = super().create(validated_data)
        return stock

    def update(self, instance, validated_data):
        stock = super().update(instance, validated_data)
        return stock


    # настройте сериализатор для продукта


class ProductPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model =  StockProduct
        fields = ['product','quantity','price']

    # настройте сериализатор для позиции продукта на складе


class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True)
    class Meta:
        model = Stock
        fields = ['id','address','positions']
    # настройте сериализатор для склада

    def create(self, validated_data):
        # достаем связанные данные для других таблиц
        positions = validated_data.pop('positions')

        # создаем склад по его параметрам
        stock = super().create(validated_data)

        for position in positions:
            StockProduct.objects.create(stock=stock, **position)
        # здесь вам надо заполнить связанные таблицы
        # в нашем случае: таблицу StockProduct
        # с помощью списка positions

        return stock

    def update(self, instance, validated_data):
        # достаем связанные данные для других таблиц
        positions = validated_data.pop('positions')

        # обновляем склад по его параметрам
        stock = super().update(instance, validated_data)


        for position in positions:
            i = position['product']
            StockProduct.objects.update_or_create(stock=stock, product=Product.objects.get(id=i.id), defaults={'quantity': position['quantity'], 'price': position['price']})

        # здесь вам надо обновить связанные таблицы
        # в нашем случае: таблицу StockProduct
        # с помощью списка positions

        return stock
