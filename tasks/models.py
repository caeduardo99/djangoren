from django.db import models

# Create your models here.



class Vgral(models.Model):
    nombrevend = models.CharField(db_column='NombreVend', max_length=255, blank=True,primary_key=True)  # Field name made lowercase.
    codlínea = models.FloatField(db_column='CodLínea', blank=True, null=True)  # Field name made lowercase.      
    desc_línea = models.CharField(db_column='Desc#Línea', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    coditem = models.FloatField(db_column='CodItem', blank=True, null=True)  # Field name made lowercase.        
    codalterno = models.CharField(db_column='CodAlterno', max_length=255, blank=True, null=True)  # Field name made lowercase.
    descitem = models.CharField(db_column='DescItem', max_length=255, blank=True, null=True)  # Field name made lowercase.
    nombreprovcli = models.CharField(db_column='NombreProvCli', max_length=255, blank=True, null=True)  # Field name made lowercase.
    codbodega = models.CharField(db_column='CodBodega', max_length=255, blank=True, null=True)  # Field name made lowercase.
    codformacontacto = models.CharField(db_column='CodFormaContacto', max_length=255, blank=True, null=True)  # Field name made lowercase.
    descripcion = models.CharField(db_column='Descripcion', max_length=255, blank=True, null=True)  # Field name made lowercase.
    cantidad = models.FloatField(db_column='Cantidad', blank=True, null=True)  # Field name made lowercase.      
    precioureal = models.FloatField(db_column='PrecioUReal', blank=True, null=True)  # Field name made lowercase.    
    preciotreal = models.FloatField(db_column='PrecioTReal', blank=True, null=True)  # Field name made lowercase.    
    costototalreal = models.FloatField(db_column='CostoTotalReal', blank=True, null=True)  # Field name made lowercase.
    utilidad = models.FloatField(db_column='Utilidad', blank=True, null=True)  # Field name made lowercase.      
    porutilidaduc = models.FloatField(db_column='PorUtilidadUC', blank=True, null=True)  # Field name made lowercase.
    porutilidadbasecosto = models.FloatField(db_column='PorUtilidadBaseCosto', blank=True, null=True)  # Field name made lowercase.
    fecha = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'VGral$'
        ordering=['desc_línea']
      

    
    def __str__(self): 
       return self.nombreprovcli 

 
    