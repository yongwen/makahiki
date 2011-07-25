from django.core import management
from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib.sites.models import Site
from django.template.loader import render_to_string

from components.makahiki_profiles.models import Profile
from components.makahiki_notifications.models import UserNotification

class Command(management.base.BaseCommand):
  help = 'Cleans out users with duplicate ids.  Renames users with duplicate display names.'
  
  def handle(self, *args, **options):
    """
    Adds the top users to the canopy.
    """
    if len(args) != 1:
      self.stdout.write("Usage: python manage.py add_canopy_members <percent>\n")
      return
      
    percent = 0
    try:
      percent = int(args[0])
    except ValueError:
      self.stdout.write("Percent must be an integer value\n")
      return
      
    if percent <= 0:
      self.stdout.write("Percent must be greater than 0\n")
      return
      
    count = Profile.objects.count() * percent / 100
    eligible_members = Profile.objects.order_by("-points")[:count]
    self.stdout.write("%d members are eligible for the canopy.\n" % count)
    for member in eligible_members:
      if member.canopy_member:
        self.stdout.write("'%s' is already a member.  Skipping\n" % member.name)
      else:
        self.__create_notifications(member.user)
        member.canopy_member = True
        member.save()
        
  def __create_notifications(self, user):
    message = "Congratulations! You have been added to the canopy!  Click <a href='%s'>here</a> to enter!" % (reverse("canopy_index")) 
    
    UserNotification.create_success_notification(user, message)

    if user.email and len(user.email) > 0:
      subject = "[%s] Congratulations! You have been added to the canopy!" % (settings.COMPETITION_NAME,) 
      current_site = Site.objects.get(id=settings.SITE_ID)
      message = render_to_string("email/added_to_canopy.txt", {
          "user": user,
          "competition_name": settings.COMPETITION_NAME,
          "domain": current_site.domain,
      })
      html_message = render_to_string("email/added_to_canopy.html", {
          "user": user,
          "competition_name": settings.COMPETITION_NAME,
          "domain": current_site.domain,
      })

      UserNotification.create_email_notification(user, subject, message, html_message)
      
    else:
      self.stdout.write("'%s' does not have a valid email address.  Skipping\n" % user.username)