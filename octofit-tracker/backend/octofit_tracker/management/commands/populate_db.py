
from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Workout, Leaderboard
from django.utils import timezone
from django.db import connection

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **kwargs):
        # Drop collections directly to avoid ORM delete issues
        db = connection.cursor().db_conn.client[connection.settings_dict['NAME']]
        db.activity.drop()
        db.leaderboard.drop()
        db.workout.drop()
        db.user.drop()
        db.team.drop()

        # Create Teams
        marvel = Team.objects.create(name='Marvel', description='Marvel Superheroes')
        dc = Team.objects.create(name='DC', description='DC Superheroes')

        # Create Users
        users = [
            User.objects.create(name='Iron Man', email='ironman@marvel.com', team=marvel, is_leader=True),
            User.objects.create(name='Captain America', email='cap@marvel.com', team=marvel),
            User.objects.create(name='Spider-Man', email='spiderman@marvel.com', team=marvel),
            User.objects.create(name='Batman', email='batman@dc.com', team=dc, is_leader=True),
            User.objects.create(name='Superman', email='superman@dc.com', team=dc),
            User.objects.create(name='Wonder Woman', email='wonderwoman@dc.com', team=dc),
        ]

        # Create Activities
        Activity.objects.create(user=users[0], activity_type='Running', duration_minutes=30, date=timezone.now().date())
        Activity.objects.create(user=users[1], activity_type='Cycling', duration_minutes=45, date=timezone.now().date())
        Activity.objects.create(user=users[3], activity_type='Swimming', duration_minutes=60, date=timezone.now().date())
        Activity.objects.create(user=users[4], activity_type='Yoga', duration_minutes=40, date=timezone.now().date())

        # Create Workouts
        w1 = Workout.objects.create(name='Super Strength', description='Strength workout for heroes')
        w2 = Workout.objects.create(name='Agility Training', description='Agility and speed workout')
        w1.suggested_for.set([users[0], users[3]])
        w2.suggested_for.set([users[2], users[4]])

        # Create Leaderboard
        Leaderboard.objects.create(team=marvel, total_points=150, week=1)
        Leaderboard.objects.create(team=dc, total_points=120, week=1)

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data.'))
