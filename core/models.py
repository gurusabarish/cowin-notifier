from django.db import models


class States(models.Model):
    name = models.CharField(max_length=100)
    api_id = models.IntegerField(unique=True)


class Districts(models.Model):
    state = models.ForeignKey(States, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    api_id = models.IntegerField(unique=True)


class Email_users(models.Model):
    email = models.EmailField(max_length=150)
    age = models.IntegerField()
    state_name = models.CharField(max_length=100)
    state_id = models.IntegerField()
    district_name = models.CharField(max_length=100)
    district_id = models.IntegerField()


class District_ID(models.Model):
    api_id = models.IntegerField()


class District_data(models.Model):
    district = models.ForeignKey(District_ID, on_delete=models.CASCADE)
    hos_id = models.IntegerField(unique=True)
    hos_name = models.CharField(max_length=300)
    hos_address = models.CharField(max_length=500)
    hos_district = models.CharField(max_length=100)
    hos_state = models.CharField(max_length=100)
    min_age = models.IntegerField()
    block = models.CharField(max_length=200, null=True)
    pin = models.IntegerField(null=True)
    date = models.DateField(blank=True, null=True)
    dose1 = models.IntegerField()
    dose2 = models.IntegerField()
    avail = models.IntegerField()
