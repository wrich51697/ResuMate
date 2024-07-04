from celery import Celery

celery = Celery(__name__, broker='your_broker_url')


@celery.task
def process_file(file_id, file_path):
    # Implement your AI processing logic here
    print(f"Processing file {file_id} at {file_path}")
    # Simulate processing time
    import time
    time.sleep(10)
    print(f"Completed processing file {file_id}")
