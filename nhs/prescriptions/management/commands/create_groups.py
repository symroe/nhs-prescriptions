"""
Create our editorial product groupings on a new db
"""
from django.core.management.base import BaseCommand

from nhs.prescriptions.models import Product, Group

class Command(BaseCommand):
    """
    Our command!

    We will call each method on SELF named group_*
    which should create one group.
    """

    def handle(self, **options):
        "IDjangoManagementCommand Entrypoint!"
        for attr in dir(self):
            if attr.startswith('group_') and callable(getattr(self, attr)):
                print "Creating/Updating {0}".format(attr.split('_')[1])
                getattr(self, attr)()

    def group_statins(self):
        """
        Create our Statin group pleaze!

        Return: None
        Exceptions: None
        """
        statinz = Product.objects.filter(name__icontains="statin")
        statbucket = Group.objects.get_or_create(name="statins")[0]
        for s in statinz:
            statbucket.drugs.add(s)
        statbucket.save()





