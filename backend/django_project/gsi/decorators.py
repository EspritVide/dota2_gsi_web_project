# import json
# import pprint
# from django_project.settings import BASE_DIR

from django.http import HttpResponse

from .scripts import get_cleared_gsi_data, check_continue_condition


def check_gsi_data(func):
    """
    Validate and clear GSI data,
    manage game in DB and Redis
    """
    def wrapper(*args, **kwargs):
        request = args[0]

        # with open(f'{BASE_DIR}/game_states.txt', mode='a') as f:
        #     try:
        #         gsi_data = json.loads(request.body)
        #         f.write(pprint.pformat(gsi_data) + '\n\n')
        #     except Exception:
        #         pass

        cleared_gsi_data = get_cleared_gsi_data(request.body)

        if not cleared_gsi_data:
            return HttpResponse('Bad GSI data')

        if not check_continue_condition(cleared_gsi_data):
            return HttpResponse('Passed GSI data')

        return func(*args,
                    gsi_data=cleared_gsi_data,
                    **kwargs)
    return wrapper
