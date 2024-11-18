import datetime
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone


from .models import Action


def create_action(user, verb: str, target=None):
    """Create a new action that optionally includes a target.
    Additionally checks for the existence of similar actions to avoid duplicates

    Args:
        user: User to create the action
        verb: The action to be performed
        target (optional): _description_. Defaults to None.
    """
    # check for similar actions made in the past minute
    now = timezone.now()
    last_minute = now - datetime.timedelta(seconds=60)
    similar_actions = Action.objects.filter(
        user_id=user.id, verb=verb, created__gte=last_minute)

    if target:
        target_ct = ContentType.objects.get_for_model(target)
        similar_actions = similar_actions.filter(
            target_ct=target_ct, target_id=target.id)

    if not similar_actions:
        # if there's no similar action
        action = Action(user=user, verb=verb, target=target)
        action.save()
        return True
    return False
