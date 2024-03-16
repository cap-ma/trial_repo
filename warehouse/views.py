from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Warehouse,Product,ProductMaterial


class WarehouseGetListView(APIView):
    def get(self,request,*args,**kwargs):
        
        product_names=request.query_params.getlist("product_name")
        product_quantity=request.query_params.getlist('product_quantity')
        main_res=[]
        
        all_materials= Warehouse.objects.filter(id__gt=0)#to get copy of data from database because of lazy loading functionality

        for name, quantity in zip(product_names, product_quantity):
            results = []

            try:
                product = Product.objects.get(name=name)
            except Product.DoesNotExist:
                continue
            materials = ProductMaterial.objects.filter(product=product)#get materials of product user inserted
       
            for material in materials:
                warehouse_materials = [y for y in all_materials if y.material == material.material]
             
                total_qty=material.quantity * float(quantity)
                
                for index, x in enumerate(warehouse_materials):
               
                    if total_qty>=x.remainder :
                        if x.remainder==0:
                            continue
                        res=total_qty-x.remainder
                        if index!=len(warehouse_materials)-1:#to check if material does not exists in db it makes null value 
                            my_result={"warehouse_id":x.pk,"material_name":x.material.name,"qty":x.remainder,"price":x.price}
                            total_qty=res
                            x.remainder=0
                            results.append(my_result)
                        else:
                            my_result={"warehouse_id":x.pk,"material_name":x.material.name,"qty":x.remainder,"price":x.price}
                            results.append(my_result)
                            my_result={"warehouse_id":None,"material_name":x.material.name,"qty":res,"price":None}
                            results.append(my_result)

                    else:
                        x.remainder=x.remainder-total_qty
                        my_result={"warehouse_id":x.pk,"material_name":x.material.name,"qty":total_qty,"price":x.price}
                        results.append(my_result)

            main_res.append({"product_name":name,"product_quantity":quantity,'product_materials':results})

        return Response({"result":main_res})


    