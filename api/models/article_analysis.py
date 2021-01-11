from djongo import models


class CrimeAnalysis(models.Model):
    location_of_crime = models.CharField(max_length=255, null=True, unique=False)
    age = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=255, null=True, unique=False)
    ethnicity = models.CharField(max_length=255, null=True, unique=False)
    severity_index = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.location_of_crime

    class Meta:
        db_table = 'db_person'


class Criminal(CrimeAnalysis):
    def __init__(self, *args, **kwargs):
        super(CrimeAnalysis, self).__init__(*args, **kwargs)
        self.type = "criminal"

    class Meta:
        db_table = 'db_criminal'


class Victim(CrimeAnalysis):
    def __init__(self, *args, **kwargs):
        super(CrimeAnalysis, self).__init__(*args, **kwargs)
        self.type = "victim"

    class Meta:
        db_table = 'db_victim'

# python manage.py makemigrations api  -> track changes
# python manage.py sqlmigrate api XXXX
# python manage.py migrate

# if db is deleted -> python manage.py createsuperuser

