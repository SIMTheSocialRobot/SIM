from kombu import Connection, Exchange, Queue

media_exchange = Exchange('media', 'direct', durable=True)
voice_queue = Queue('voice', exchange=media_exchange, routing_key='voice')
image_queue = Queue('image', exchange=media_exchange, key='image')

def process_media(body, message):
    print body
    message.ack()

with Connection('amqp://guest:guest@localhost//') as connection:
    with connection.Consumer([voice_queue, image_queue],
        callbacks=[process_media]) as consumer:
        
        while True:
            connection.drain_events()