from django.db import models
from django.conf import settings
from django.utils.functional import cached_property

from mainapp.models import Product

# Способ управления количеством товара при удалении/оформлении корзины
# class BasketQuerySet(models.QuerySet):
#
#     def delete(self):
#         for object in self:
#             object.product.quantity += object.quantity
#             object.product.save()
#
#         super().delete()


class Basket(models.Model):
    # objects = BasketQuerySet.as_manager()

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='basket')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='количество', default=0)
    add_datetime = models.DateTimeField(verbose_name='время добавления', auto_now_add=True)

    @cached_property
    def get_items_cached(self):
        return self.user.basket.select_related()

    def get_product_cost(self):
        "return cost of all products this type"
        return self.product.price * self.quantity
    
    product_cost = property(get_product_cost)

    def get_total_quantity(self):
        "return total quantity for user"
        _items = self.get_items_cached
        _totalquantity = sum(list(map(lambda x: x.quantity, _items)))
        return _totalquantity
        
    # total_quantity = property(get_total_quantity)

    def get_total_cost(self):
        "return total cost for user"
        _items = self.get_items_cached
        _totalcost = sum(list(map(lambda x: x.product_cost, _items)))
        return _totalcost
        
    # total_cost = property(get_total_cost)

    # def delete(self):
    #     self.product.quantity += self.quantity
    #     self.product.save()
    #     super().delete()

    @staticmethod
    def get_item(pk):
        return Basket.objects.filter(pk=pk).first()

    @staticmethod
    def get_items(user):
        return Basket.objects.filter(user=user).order_by('product__category').select_related()
