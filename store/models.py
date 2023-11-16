from django.db import models
from users.models import User
import uuid

class Category(models.Model):
	name = models.CharField(max_length=40)

	class Meta:
		verbose_name_plural='Categories'

	def __str__(self):
		return self.name



class Order(models.Model):
	id = models.CharField(primary_key=True, max_length=100)
	user = models.ForeignKey(User, related_name="orders" ,on_delete=models.SET_NULL, null=True, blank=True)
	date_ordered = models.DateTimeField(auto_now_add=True)
	complete = models.BooleanField(default=False)
	total = models.DecimalField(max_digits=10, decimal_places=2)


	class Meta:
		ordering = ['-date_ordered']

	def __str__(self):
		return f'{self.id} hecha por {self.user}'
		
	""" @property
	def shipping(self):
		shipping = False
		for item in self.items:
			if item.digital == False:
				shipping = True
		return shipping """

	""" 	@property
		def get_cart_total(self):
			#orderitems = self.items.all()
			total = sum([item.get_total for item in self.items])
			return total  """

	""" @property
	def get_cart_items(self):
		#orderitems = self.orderitems.all()
		total = sum([item.quantity for item in self.items])
		return total  """



class OrderItem(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4)
	product = models.CharField(max_length=100)
	user = models.ForeignKey(User, related_name="orderitems", on_delete=models.SET_NULL, null=True)
	price = models.DecimalField(max_digits=10, decimal_places=2)
	quantity = models.IntegerField(default=0, null=True, blank=True)
	digital = models.BooleanField(default=False)
	date_added = models.DateTimeField(auto_now_add=True)


	class Meta:
		ordering = ['-date_added']

	def __str__(self):
		return f'{self.product} - {self.quantity}'

	@property
	def get_total(self):
		total = self.price * self.quantity
		return total




class ShippingAddress(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4)
	user = models.ForeignKey(User, related_name="shippings" ,on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey(Order, related_name="shippings" ,on_delete=models.SET_NULL, null=True)
	address = models.CharField(max_length=200, null=False)
	city = models.CharField(max_length=200, null=False)
	state = models.CharField(max_length=200, null=False)
	zipcode = models.CharField(max_length=200, null=False)
	date_added = models.DateTimeField(auto_now_add=True)

	class Meta:
		verbose_name_plural = "Shipping Addresses"
		ordering = ['-date_added']

	def __str__(self):
		return f'A {self.address} hecha por {self.user}'