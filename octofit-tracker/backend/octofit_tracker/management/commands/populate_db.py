from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from activities.models import Activity
from django.db import transaction

# Si tienes modelos Team, Leaderboard, Workout, impórtalos aquí
def get_or_create_team_model():
    try:
        from activities.models import Team
        return Team
    except ImportError:
        return None

def get_or_create_leaderboard_model():
    try:
        from activities.models import Leaderboard
        return Leaderboard
    except ImportError:
        return None

def get_or_create_workout_model():
    try:
        from activities.models import Workout
        return Workout
    except ImportError:
        return None

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    @transaction.atomic
    def handle(self, *args, **options):
        User = get_user_model()
        Team = get_or_create_team_model()
        Leaderboard = get_or_create_leaderboard_model()
        Workout = get_or_create_workout_model()

        self.stdout.write(self.style.WARNING('Deleting old data...'))
        Activity.objects.all().delete()
        if Team:
            Team.objects.all().delete()
        if Leaderboard:
            Leaderboard.objects.all().delete()
        if Workout:
            Workout.objects.all().delete()
        User.objects.exclude(is_superuser=True).delete()

        self.stdout.write(self.style.SUCCESS('Creating teams...'))
        marvel = Team.objects.create(name='Marvel') if Team else None
        dc = Team.objects.create(name='DC') if Team else None

        self.stdout.write(self.style.SUCCESS('Creating users...'))
        users = [
            {'username': 'ironman', 'email': 'ironman@marvel.com', 'team': marvel},
            {'username': 'spiderman', 'email': 'spiderman@marvel.com', 'team': marvel},
            {'username': 'batman', 'email': 'batman@dc.com', 'team': dc},
            {'username': 'superman', 'email': 'superman@dc.com', 'team': dc},
        ]
        user_objs = []
        for u in users:
            user = User.objects.create_user(username=u['username'], email=u['email'], password='password123')
            if Team and u['team']:
                user.team = u['team']
                user.save()
            user_objs.append(user)

        self.stdout.write(self.style.SUCCESS('Creating activities...'))
        Activity.objects.create(user=user_objs[0], activity_type='Run', duration_minutes=30, distance_km=5, timestamp='2025-11-01T10:00:00Z', notes='Morning run')
        Activity.objects.create(user=user_objs[1], activity_type='Swim', duration_minutes=45, distance_km=2, timestamp='2025-11-02T11:00:00Z', notes='Pool session')
        Activity.objects.create(user=user_objs[2], activity_type='Bike', duration_minutes=60, distance_km=20, timestamp='2025-11-03T12:00:00Z', notes='Road cycling')
        Activity.objects.create(user=user_objs[3], activity_type='Yoga', duration_minutes=50, distance_km=0, timestamp='2025-11-04T13:00:00Z', notes='Stretching')

        if Workout:
            self.stdout.write(self.style.SUCCESS('Creating workouts...'))
            Workout.objects.create(name='Full Body', description='All muscle groups')
            Workout.objects.create(name='Cardio Blast', description='High intensity cardio')
        if Leaderboard:
            self.stdout.write(self.style.SUCCESS('Creating leaderboard...'))
            Leaderboard.objects.create(user=user_objs[0], score=100)
            Leaderboard.objects.create(user=user_objs[1], score=90)
            Leaderboard.objects.create(user=user_objs[2], score=80)
            Leaderboard.objects.create(user=user_objs[3], score=70)

        self.stdout.write(self.style.SUCCESS('Test data created successfully!'))
