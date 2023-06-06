from django.db import models


class propsale(models.Model):
    seller = models.CharField(max_length=100)
    date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    sector = models.CharField(max_length=50)
    street = models.CharField(max_length=100)
    plotid = models.IntegerField()
    plotnum = models.CharField(max_length=20)

class sectora(models.Model):
    gid = models.AutoField(primary_key=True)
    sector = models.CharField(max_length=50, blank=True, null=True)
    plot_no = models.FloatField(blank=True, null=True)
    street_no = models.CharField(db_column='street_no', max_length=50, blank=True, null=True)  # Field renamed because it ended with '_'.
    id = models.FloatField(blank=True, null=True)
    area = models.FloatField(blank=True, null=True)
    plotsize = models.FloatField(blank=True, null=True)
    areamarla = models.FloatField(blank=True, null=True)
    geom = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False