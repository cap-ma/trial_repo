from django.db import models

# Create your models here.
class Product(models.Model):
    name=models.CharField("name",max_length=128)
    code=models.CharField("code",max_length=128)

    def __str__(self) -> str:
        return self.name
    

class Material(models.Model):
    name=models.CharField("name",max_length=128)
    type=models.CharField(max_length=28)#indicats what is label of material like (metr,litr or any other meausurment type)
    product=models.ManyToManyField(Product,through="ProductMaterial")

    def __str__(self) -> str:
        return self.name

class ProductMaterial(models.Model):
    product=models.ForeignKey(Product,related_name='product',on_delete=models.DO_NOTHING)
    material=models.ForeignKey(Material,related_name='material',on_delete=models.DO_NOTHING)
    quantity=models.FloatField()

    def __str__(self) -> str:
        return f"{self.product} and {self.material}"

class Warehouse(models.Model):
    material=models.ForeignKey(Material,on_delete=models.DO_NOTHING)
    remainder=models.FloatField()
    price=models.DecimalField(max_digits=16, decimal_places=2,null=True)

    def __str__(self):
        return self.material.name



