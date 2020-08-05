from django.db import models
from django.contrib.auth.models import User


# from django.db.models import signals
# from django.db.models.signals import post_save
# from django.dispatch import receiver


class School(models.Model):
    name_school = models.CharField(max_length=50)
    mobile_school = models.CharField(max_length=11)
    lat = models.CharField(max_length=50)
    lng = models.CharField(max_length=50)

    def delete_link(self):
        return "/school/?delete=%s" % self.id

    def update_link(self):
        return "/school/update/%s/" % self.id


class SchoolHeadmaster(models.Model):
    headmaster = models.ForeignKey(User, related_name="Sh_headmaster_users_id", on_delete=models.CASCADE)
    school = models.ForeignKey(School, related_name="Sh_school_users_id", on_delete=models.CASCADE)


class SchoolDriver(models.Model):
    driver = models.ForeignKey(User, related_name="Sd_driver_users_id", on_delete=models.CASCADE)
    school = models.ForeignKey(School, related_name="Ds_school_users_id", on_delete=models.CASCADE)


class Destination(models.Model):
    title = models.CharField(max_length=50)
    latitude = models.CharField(max_length=50)
    longitude = models.CharField(max_length=50)
    latitudeDelta = models.CharField(max_length=50)
    longitudeDelta = models.CharField(max_length=50)
    is_active = models.BooleanField(default=False, null=True)


class Trip(models.Model):
    pass


class Position(models.Model):
    # status_TYPE = (
    #     (1, "حاضر"),
    #     (2, "غایب"),
    # )
    bus_to_home = models.CharField(max_length=50, null=True)  # Date and time of student entry and exit
    bus_to_school = models.CharField(max_length=50, null=True)
    home_to_bus = models.CharField(max_length=50, null=True)
    school_to_bus = models.CharField(max_length=50, null=True)
    status = models.CharField(max_length=50, null=True)


class Student(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(null=True)
    className = models.CharField(null=True, max_length=100)
    school = models.ForeignKey(School, related_name="SSt_users_id", on_delete=models.CASCADE)
    location = models.ForeignKey(Destination, related_name="DSt_users_id", on_delete=models.CASCADE)
    position = models.ForeignKey(Position, related_name="StP_users_id", on_delete=models.CASCADE)


class DriverStudent(models.Model):
    student = models.OneToOneField(Student, related_name="Ds_student_users_id", on_delete=models.CASCADE, unique=True)
    driver = models.ForeignKey(User, related_name="Ds_driver_users_id", on_delete=models.CASCADE)


class SchoolStudent(models.Model):
    student = models.ForeignKey(Student, related_name="Ss_student_users_id", on_delete=models.CASCADE)
    school = models.ForeignKey(School, related_name="Ss_school_users_id", on_delete=models.CASCADE)


class UserProfile(models.Model):
    USER_TYPE = (
        (1, "مدیر"),
        (3, "راننده"),
        (4, "والدین"),
        (5, "ادمین"),
    )
    user = models.OneToOneField(User, related_name="Up_users_id", on_delete=models.CASCADE)
    mobile = models.CharField(max_length=11)
    user_type = models.SmallIntegerField(choices=USER_TYPE)
    school = models.ForeignKey(School, related_name="SPO_users_id", on_delete=models.CASCADE)

    # driver = models.ForeignKey("self", related_name="driver_users_id", on_delete=models.CASCADE,null=True)

    def delete_link(self):
        if self.user_type == 4:
            return "/parent/?delete=%s" % self.user.id
        elif self.user_type == 1:
            return "/headmaster/add/?delete=%s" % self.user.id
        elif self.user_type == 2:
            return "/student/?delete=%s" % self.user.id
        elif self.user_type == 3:
            return "/driver/?delete=%s" % self.user.id

    def update_link(self):
        if self.user_type == 4:
            return "/parent/update/%s/" % self.user_id
        elif self.user_type == 1:
            return "/headmaster/update/%s/" % self.id
        elif self.user_type == 2:
            return "/student/update/%s/" % self.id
        elif self.user_type == 3:
            return "/driver/update/%s/" % self.id

    def add_link(self):
        if self.user_type == 4:
            return "/parent/add"
        elif self.user_type == 1:
            return "/headmaster/add"
        elif self.user_type == 2:
            return "/student/add"
        elif self.user_type == 3:
            return "/driver/add"


class ParentsStudent(models.Model):
    user_student = models.ForeignKey(Student, related_name="PSS_users_id", on_delete=models.CASCADE)
    student_id = models.CharField(max_length=50)
    parents_id = models.CharField(max_length=50)

# #Signal
# @receiver(signals.post_save, sender=User)
# def create_customer(sender, instance, created, **kwargs):
#     if created:
#         temp = UserProfile(user_type=1,user=instance,mobile=9128387233)
#         temp.save()
#
