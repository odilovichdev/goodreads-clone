# from django.db.models.signals import post_save
# from django.dispatch import receiver
#
# from users.models import CustomUser
# from users.tasks import send_email

# @receiver(post_save, sender=CustomUser)
# def welcome_send_email(sender, instance, created, **kwargs):
#     if created:
#         send_email.delay(
#             "Welcome to Goodreads clone",
#             f"Hi {instance.username}. Welcome to Goodreads clone.Enjoy the books and reviews",
#             [instance.email]
#         )
