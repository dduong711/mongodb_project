from django.db import models
from typing import List

class MongoDB(models.Model):
    db_name = models.CharField(max_length=256)
    db_user = models.CharField(max_length=256)
    db_password = models.CharField(max_length=256)
    srv = models.BooleanField(default=True)

    def __str__(self):
        return str(self.id)

    @property
    def connection_string(self):
        hosts = []
        print(self.host.all())
        for h in self.host.all():
            print(h)
            hosts.append(f"{h.host_name}:{h.port}")
        return MongoDB.generate_connection_string(hosts, self.srv, self.db_name, self.db_user, self.db_password)

    @staticmethod
    def generate_connection_string(host=None, srv=True, db_name=None, db_user=None, db_password=None):
        if not host:
            raise Exception("Cannot generate connection string!") 
        if srv:
            host_name = host[-1].split(":")[0]
            return f"mongodb+srv://{db_user}:{db_password}@{host_name}/{db_name}"
        conn_str = f"mongodb://{db_user}:{db_password}@"
        for h in host:
            temp = host.split(":")
            host_name = temp[0]
            port = temp[1] if len(temp) == 2 else None
            conn_str += f"{host_name}:{port},"
        conn_str = conn_str[:len(con_str)-2] + f"/{db_name}"
        return conn_str
        

class Host(models.Model):
    host_name = models.CharField(max_length=1024)
    port = models.IntegerField(null=True, blank=True)
    db = models.ForeignKey(MongoDB, on_delete=models.CASCADE, related_name="host")

    def __str__(self):
        return self.host_name