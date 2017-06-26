from django.db import models

class stop_locations(models.Model): #lat 53 long -6
    stop_id=models.CharField(max_length=10)
    stop_lat=models.CharField(max_length=20)
    stop_long=models.CharField(max_length=20)

    def __str__(self):
        return "Stop ID: "+str(self.stop_id)+" Lat: "+str(self.stop_lat)+" Long: "+str(self.stop_long)

class route_and_stop(models.Model):
    route_id=models.CharField(max_length=10)
    stop_id=models.CharField(max_length=10)
    stop_count=models.CharField(max_length=20)

    def __str__(self):
        return "Route "+str(self.route_id)+" and its associated stops"