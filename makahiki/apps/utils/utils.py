"""Provides common utility functions."""
from django.conf import settings
import os
import sys


def media_file_path(prefix=None):
    """return the path for the media file."""
    if prefix:
        return os.path.join(settings.MAKAHIKI_MEDIA_PREFIX, prefix)
    else:
        return settings.MAKAHIKI_MEDIA_PREFIX


def get_challenge_mgr_predicates():
    """Returns the predicates defined in smartgrid module."""
    from apps.managers.challenge_mgr.predicates import game_enabled, reached_round
    return {
            "game_enabled": game_enabled,
            "reached_round": reached_round,
            }


def get_smartgrid_predicates():
    """Returns the predicates defined in smartgrid module."""
    from apps.widgets.smartgrid.predicates import completed_action, approved_action, \
        completed_some_of, completed_all_of, completed_level, unlock_on_date, \
        unlock_on_event, approved_all_of, approved_some_of
    return {
            "completed_action": completed_action,
            "completed_some_of": completed_some_of,
            "completed_all_of": completed_all_of,
            "completed_level": completed_level,
            "unlock_on_date": unlock_on_date,
            "unlock_on_event": unlock_on_event,
            "approved_action": approved_action,
            "approved_some_of": approved_some_of,
            "approved_all_of": approved_all_of,
            }


def get_player_mgr_predicates():
    """Returns the predicates defined in player_mgr module."""
    from apps.managers.player_mgr.predicates import badge_awarded, posted_to_wall, \
        set_profile_pic, has_points, is_admin, allocated_ticket, daily_visit_count
    return {
        "is_admin": is_admin,
        "has_points": has_points,
        "allocated_ticket": allocated_ticket,
        "badge_awarded": badge_awarded,
        "posted_to_wall": posted_to_wall,
        "set_profile_pic": set_profile_pic,
        "daily_visit_count": daily_visit_count,
        }


def eval_predicates(predicates, user):
    """Returns the boolean evaluation result of the predicates against the user."""

    user_predicates = predicates.replace("(", "(user,")

    allow_dict = {"True": True, "False": False, "user": user}
    allow_dict.update(get_player_mgr_predicates())
    allow_dict.update(get_challenge_mgr_predicates())
    allow_dict.update(get_smartgrid_predicates())

    return eval(user_predicates, {"__builtins__": None}, allow_dict)


def validate_predicates(predicates):
    """Validate the predicates string."""
    from django.contrib.auth.models import User

    error_msg = None
    # Pick a user and see if the conditions result is true or false.
    user = User.objects.all()[0]
    try:
        result = eval_predicates(predicates, user)
        # Check if the result type is a boolean
        if type(result) != type(True):
            error_msg = "Expected boolean value but got %s" % type(result)
    except Exception:
        error_msg = "Received exception: %s" % sys.exc_info()[0]

    return error_msg


def validate_form_predicates(predicates):
    """validate the predicates in a form. if error, raise the form validation error."""
    from django import forms
    from django.contrib.auth.models import User

    # Pick a user and see if the conditions result is true or false.
    user = User.objects.all()[0]
    try:
        result = eval_predicates(predicates, user)
        # Check if the result type is a boolean
        if type(result) != type(True):
            raise forms.ValidationError("Expected boolean value but got %s" % type(result))
    except Exception:
        raise forms.ValidationError("Received exception: %s" % sys.exc_info()[0])
