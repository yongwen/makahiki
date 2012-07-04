"""Views handler for Badge widget rendering."""

from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from apps.widgets.badges.models import Badge, BadgeAward
from apps.managers.player_mgr.models import Profile


def supply(request, page_name):
    """Supply view_objects for widget rendering.
       :return: empty dictionary."""
    _ = page_name

    return get_badge_catalog(request)


@login_required
def badge_catalog(request):
    """Handle the badge catalog request."""
    badges_view_objects = {"badges": get_badge_catalog(request)}

    return render_to_response("badge-catalog.html", {
        "view_objects": badges_view_objects,
        }, context_instance=RequestContext(request))


def get_badge_catalog(request):
    """Returns the badge catalog."""

    user = request.user
    profile = user.get_profile()
    awarded_badges = []
    locked_badges = []

    for awarded in BadgeAward.objects.filter(profile=profile):
        awarded_badges.append(awarded.badge)

    awarded_badges = sorted(awarded_badges, key=lambda badge: badge.priority)
    awarded_badges.reverse()

    for badge in Badge.objects.order_by('-priority'):
        if not badge in awarded_badges:
            locked_badges.append(badge)

    # For each badge, get the number of people who have the badge.
    team = profile.team
    for badge in awarded_badges:
        badge.total_users = BadgeAward.objects.filter(badge=badge).count()
        badge.team_users = Profile.objects.filter(badgeaward__badge=badge, team=team)
    for badge in locked_badges:
        badge.total_users = BadgeAward.objects.filter(badge=badge).count()
        badge.team_users = Profile.objects.filter(badgeaward__badge=badge, team=team)

    return {
        "awarded_badges": awarded_badges,
        "locked_badges": locked_badges,
        }
