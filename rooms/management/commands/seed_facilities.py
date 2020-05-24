from django.core.management.base import BaseCommand
from rooms.models import Facility


class Command(BaseCommand):
    help = "This command tells me that you love me"

    # def add_arguments(self, parser):
    #     parser.add_arguments("--times", help="How many times do you want me to tell you")

    def handle(self, *args, **options):

        facilities = [
            "Private entrance",
            "Paind parking on premises",
            "Paid parking off premises",
            "Elevator",
            "Parking",
            "Gym"
        ]

        for facility in facilities:
            Facility.objects.create(name=facility)

        self.stdout.write(self.style.SUCCESS(f"{len(facilities)} facilities created!"))
