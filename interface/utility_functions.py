import datetime
import json

from django.http import JsonResponse

from interface.constants import DAY_QUOTA_LIMIT, MINUTES_QUOTA_LIMIT, MINUTES_QUOTA, MINUTES_ERROR_MSG, \
    DAY_QUOTA_ERROR_MSG


def input_validation(func):
    def inner(request):
        filters = request.GET.get('filters') or request.POST.get('filters')
        filters = json.loads(request.body).get('filters') if not filters and request.body else {}
        # removing key having empty value
        filters = {k: v for k, v in filters.items() if v}
        return func(filters)

    return inner


def session_validation(func):
    def inner(request):

        # checking for minutes quota
        if 'minutes_quota' not in request.session or has_minutes_quota_expired(request.session):
            request.session['minutes_quota'] = {'count': 1, 'expiry_at': datetime.datetime.now().timestamp()}
        else:
            request.session['minutes_quota']['count'] = request.session['minutes_quota'].get('count') + 1

        if request.session['minutes_quota']['count'] > MINUTES_QUOTA_LIMIT:
            return JsonResponse({"error": True, "error_msg": MINUTES_ERROR_MSG})

        # checking for day quota
        if 'day_quota' not in request.session or get_date_from_timestamp(request.session) < datetime.date.today():
            request.session['day_quota'] = {'count': 1, 'expiry_at': datetime.datetime.now().timestamp()}
        else:
            request.session['day_quota']['count'] = request.session['day_quota'].get('count') + 1

        if request.session['day_quota']['count'] > DAY_QUOTA_LIMIT:
            return JsonResponse({"error": True, "error_msg": DAY_QUOTA_ERROR_MSG})

        return func(request)

    return inner


def get_date_from_timestamp(session):
    timestamp = session['day_quota'].get('expiry_at')
    return datetime.date.fromtimestamp(timestamp)


def has_minutes_quota_expired(session):
    timestamp = datetime.datetime.fromtimestamp(session['minutes_quota']['expiry_at'])
    comparator = datetime.datetime.now() - datetime.timedelta(seconds=MINUTES_QUOTA)
    if timestamp < comparator:
        return True

    return False
