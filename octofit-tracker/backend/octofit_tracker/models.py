from djongo import models



class Team(models.Model):
    id = models.ObjectIdField(primary_key=True, editable=False)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name




class User(models.Model):
    id = models.ObjectIdField(primary_key=True, editable=False)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    team = models.ForeignKey(Team, to_field='id', on_delete=models.CASCADE, related_name='members')
    is_leader = models.BooleanField(default=False)

    def __str__(self):
        return self.name




class Activity(models.Model):
    id = models.ObjectIdField(primary_key=True, editable=False)
    user = models.ForeignKey(User, to_field='id', on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(max_length=100)
    duration_minutes = models.PositiveIntegerField()
    date = models.DateField()

    def __str__(self):
        return f"{self.user.name} - {self.activity_type}"



class Workout(models.Model):
    id = models.ObjectIdField(primary_key=True, editable=False)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    suggested_for = models.ManyToManyField(User, related_name='suggested_workouts', blank=True)

    def __str__(self):
        return self.name




class Leaderboard(models.Model):
    id = models.ObjectIdField(primary_key=True, editable=False)
    team = models.ForeignKey(Team, to_field='id', on_delete=models.CASCADE, related_name='leaderboards')
    total_points = models.PositiveIntegerField(default=0)
    week = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.team.name} - Week {self.week}"
