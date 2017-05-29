

from kombu import Connection, Exchange, Queue

media_exchange = Exchange('media', 'direct', durable=True)
face_detector_queue = Queue('face_detector', exchange=media_exchange, routing_key='face_detector')



def process_media(body, message):
    

    print(body)
    message.ack()

with Connection('amqp://guest:guest@localhost//') as connection:
    with connection.Consumer([face_detector_queue],
        callbacks=[process_media]) as consumer:
        
        while True:
            connection.drain_events()
        

