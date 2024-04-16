from celery import shared_task

from refer.models import Code
import time

@shared_task
def delete_code(id):
    time.sleep(5)
    Code.objects.filter(id=id).delete()
    print(f'success deleted {id}')
