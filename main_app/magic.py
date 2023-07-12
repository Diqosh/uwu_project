from main_app.models import User


def fcm_send_push( ids, notifaction_text,  **kwargs):
    print('device_ids: ', *ids)
    print('notifactiob_text: ' , notifaction_text)
