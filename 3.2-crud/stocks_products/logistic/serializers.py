from rest_framework import serializers

from logistic.models import Product, Stock, StockProduct


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class ProductPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockProduct
        fields = "__all__"


class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True)

    class Meta:
        model = Stock
        fields = "__all__"

    def create(self, validated_data):
        # достаем связанные данные для других таблиц
        positions = validated_data.pop('positions')
        # создаем склад по его параметрам
        stock = super().create(validated_data)
        # здесь вам надо заполнить связанные таблицы
        # в нашем случае: таблицу StockProduct
        # с помощью списка positions
        for position in positions:
            # StockProduct.objects.create(stock=stock, **position)
            product = Product.objects.filter(id=position.get('product'))
            StockProduct.objects.get_or_create(
                stock=stock,
                product=product,
                quantity=position.get('quantity'),
                price=position.get('price'),
            )
        return stock

    def update(self, instance, validated_data):
        # достаем связанные данные для других таблиц
        positions = validated_data.pop('positions')
        print(positions)
        # обновляем склад по его параметрам
        stock = super().update(instance, validated_data)
        # здесь вам надо обновить связанные таблицы
        # в нашем случае: таблицу StockProduct
        # с помощью списка positions
        for position in positions:
            product = Stock.objects.filter(id=position.get('product'))
            StockProduct.objects.update_or_create(
                stock=stock,
                product=product,
                quantity=position.get('quantity'),
                price=position.get('price'),
            )
        return stock
