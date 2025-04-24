# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class EventParticipants(models.Model):
    pk = models.CompositePrimaryKey('event_id', 'participant_id')
    event = models.ForeignKey('Events', models.DO_NOTHING)
    participant = models.ForeignKey('Users', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'event_participants'
        unique_together = (('event', 'participant'),)


class Events(models.Model):
    event_id = models.AutoField(primary_key=True)
    host = models.ForeignKey('Users', models.DO_NOTHING)
    title = models.TextField()
    activity = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    description = models.TextField()

    class Meta:
        managed = False
        db_table = 'events'
        unique_together = (('host', 'start_time'),)


class FitnessLog(models.Model):
    pk = models.CompositePrimaryKey('user_id', 'start_time', 'end_time')
    # user = models.ForeignKey('Users', models.DO_NOTHING)
    user = models.ForeignKey('Users', on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    activity = models.TextField()
    description = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fitness_log'
        unique_together = (('user', 'start_time', 'end_time'),)


class Foods(models.Model):
    food_id = models.AutoField(primary_key=True)
    food_item = models.TextField(blank=True, null=True)
    food_category = models.TextField(blank=True, null=True)
    per_100_units = models.TextField(blank=True, null=True)
    calories_per_100 = models.IntegerField(blank=True, null=True)
    kj_per_100 = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'foods'

    def __str__(self):
        return self.food_item


class Goals(models.Model):
    GOAL_TYPE_CHOICES = [
        ('fitness', 'Fitness'),
        ('nutrition', 'Nutrition'),
        ('sleep', 'Sleep'),
        ('wellness', 'Wellness'),
    ]

    # pk = models.CompositePrimaryKey('goal_id', 'user_id')
    goal_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('Users', models.DO_NOTHING)
    goal_type = models.CharField(max_length=20, choices=GOAL_TYPE_CHOICES)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(blank=True, null=True)
    completed = models.BooleanField()
    description = models.TextField()

    class Meta:
        managed = False
        db_table = 'goals'

class NutritionGoals(Goals):
    food = models.ForeignKey(Foods, models.DO_NOTHING, null=True)
    lower_grams = models.IntegerField()
    upper_grams = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'nutrition_goals'
class FitnessGoals(Goals):
    activity = models.CharField(max_length=20, null=True)
    target_minutes = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'fitness_goals'
class SleepGoals(Goals):
    target_quality = models.DecimalField(max_digits=4, decimal_places=2)
    target_hours = models.DecimalField(max_digits=4, decimal_places=2)

    class Meta:
        managed = True
        db_table = 'sleep_goals'
class NutritionLog(models.Model):
    pk = models.CompositePrimaryKey('user_id', 'food_id', 'time_of_consumption')
    # user = models.ForeignKey('Users', models.DO_NOTHING)
    user = models.ForeignKey('Users', on_delete=models.CASCADE)
    food = models.ForeignKey(Foods, models.DO_NOTHING)
    time_of_consumption = models.DateTimeField()
    num_grams_consumed = models.IntegerField()
    source = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'nutrition_log'
        unique_together = (('user', 'food', 'time_of_consumption'),)


class SleepLog(models.Model):
    pk = models.CompositePrimaryKey('user_id', 'start_time', 'end_time')
    # user = models.ForeignKey('Users', models.DO_NOTHING)
    user = models.ForeignKey('Users', on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    sleep_quality = models.IntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sleep_log'
        unique_together = (('user', 'start_time', 'end_time'),)


class Users(models.Model):
    user_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30, null=True)
    email = models.CharField(max_length=100)
    phone_number = models.TextField(blank=True, null=True)
    city = models.TextField(blank=True, null=True)
    state = models.TextField(blank=True, null=True)
    country = models.TextField()

    class Meta:
        managed = False
        db_table = 'users'
