"""Predicates indicating if a level or cell should be unlocked."""

from datetime import datetime, timedelta
from apps.widgets.smartgrid.models import Action, Category, Event


def completed_action(user, slug):
    """Returns true if the user complete the action."""
    return user.actionmember_set.filter(action__slug=slug).count() > 0


def completed_all_of(user, category_slug=None, action_type=None, resource=None):
    """Returns true if completed all of specified type."""

    if category_slug:
        return user.actionmember_set.filter(action__category__slug=category_slug).count() ==\
           Category.objects.filter(slug=category_slug).count()

    if action_type:
        return user.actionmember_set.filter(action__type=action_type).count() ==\
            Action.objects.filter(type=action_type).count()

    if resource:
        return user.actionmember_set.filter(action__related_resource=resource).count() ==\
            Action.objects.filter(related_resource=resource).count()

    return user.actionmember_set.all().count() ==\
           Action.objects.all().count()


def completed_some_of(user, some=1, category_slug=None, action_type=None, resource=None):
    """Returns true if completed some of the specified type.
    some is default to 1 if not specified."""
    if category_slug:
        return user.actionmember_set.filter(action__category__slug=category_slug).count() >= some

    if action_type:
        return user.actionmember_set.filter(action__type=action_type).count() >= some

    if resource:
        return user.actionmember_set.filter(action__related_resource=resource).count() >= some

    return user.actionmember_set.all().count() >= some


def completed_level(user, lvl=1):
    """Returns true if the user has performed all activities successfully, and
      attempted all commitments."""
    num_completed_activities = \
    user.actionmember_set.filter(action__type='activity', action__level__priority=lvl).count()
    num_attempted_commitments = \
    user.actionmember_set.filter(action__type='commitment', action__level__priority=lvl).count()
    num_level_activities = Action.objects.filter(type='activity', level__priority=lvl).count()
    num_level_commitments = Action.objects.filter(type='commitment', level__priority=lvl).count()
    ret = (num_completed_activities == num_level_activities) and \
    (num_attempted_commitments == num_level_commitments)
    return ret


def unlock_on_date(user, date_string):
    """Returns true if the current date is equal to or after the date_string."""
    _ = user
    today = datetime.today()
    unlock_date = datetime.strptime(date_string, "%m/%d/%y")
    return today >= unlock_date


def unlock_on_event(user, event_slug, days=0):
    """Returns true if the current date is equal to or after the date of the Event
    defined by the event_slug, optionally days before. days should be a negative number."""
    _ = user
    today = datetime.today()
    day_delta = timedelta(days=days)
    event = Event.objects.get(slug=event_slug)
    if event:
        unlock_date = event.event_date + day_delta
        return today >= unlock_date
    else:
        return True


def approved_action(user, slug):
    """Returns true if the action is approved."""
    return user.actionmember_set.filter(action__slug=slug, approval_status="approved").count() > 0


def approved_some_of(user, some=1, category_slug=None, action_type=None, resource=None):
    """Returns true if some actions of the specified type is approved."""

    if category_slug:
        return user.actionmember_set.filter(action__category__slug=category_slug,
                                            approval_status="approved").count() >= some

    if action_type:
        return user.actionmember_set.filter(action__type=action_type,
                                            approval_status="approved").count() >= some

    if resource:
        return user.actionmember_set.filter(action__related_resource=resource,
                                            approval_status="approved").count() >= some

    return user.actionmember_set.filter(approval_status="approved").count() >= some


def approved_all_of(user, category_slug=None, action_type=None, resource=None):
    """Returns true if all actions of the specified type is approved."""

    if category_slug:
        return user.actionmember_set.filter(action__category__slug=category_slug,
                                            approval_status="approved").count() ==\
               Category.objects.filter(slug=category_slug).count()

    if action_type:
        return user.actionmember_set.filter(action__type=action_type,
                                            approval_status="approved").count() ==\
               Action.objects.filter(type=action_type).count()

    if resource:
        return user.actionmember_set.filter(action__related_resource=resource,
                                            approval_status="approved").count() ==\
               Action.objects.filter(related_resource=resource).count()

    return user.actionmember_set.filter(approval_status="approved").count() ==\
           Action.objects.all().count()
