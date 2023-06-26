from django.db import models

# Create your models here.
class Products_updates(models.Model): 
    Id_update = models.AutoField(primary_key=True,db_column='Id_update')
    Updated_at=models.DateTimeField(db_column='Updated_at')
    Product_name = models.CharField(max_length=250,db_column='Product_name') 
    Product_description = models.TextField(db_column='Product_description') 
    Product_id = models.CharField(max_length=15,db_column='Product_id') 
    

    def __str__(self): 
        return str(self.Id_update)
   
    class Meta:
        db_table = 'Products_updates_log'
