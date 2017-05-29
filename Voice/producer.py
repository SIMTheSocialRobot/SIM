from kombu import Connection
import datetime

with Connection('amqp://guest:guest@localhost:5672//') as conn:
    simple_queue = conn.SimpleQueue('face_detector')
    message = 'hello'
    simple_queue.put(message)
    print('Sent: %s' % message)
    simple_queue.close()