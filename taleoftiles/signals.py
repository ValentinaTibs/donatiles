from django.contrib.auth.signals import user_logged_in


def do_stuff(sender, user, request, **kwargs):
    print("MAMMAMIA DEGLI ABBA")

user_logged_in.connect(do_stuff)