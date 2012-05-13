"""check energy goal command"""
import datetime

from django.core import management
from apps.widgets.resource_goal import resource_goal


class Command(management.base.BaseCommand):
    """command"""
    help = 'Check the energy goal for all teams, award points for meeting the goal'

    def handle(self, *args, **options):
        """check the energy goal for all teams"""
        print '****** Processing check_energy_goal for %s *******\n' % datetime.datetime.today()

        resource_goal.check_all_daily_resource_goals("energy")
