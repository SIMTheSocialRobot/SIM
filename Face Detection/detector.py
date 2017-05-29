import cv2
import sys
from kombu import Connection, Exchange, Queue

media_exchange = Exchange('media', 'direct', durable=True)
face_detector_queue = Queue('face_detector', exchange=media_exchange, routing_key='face_detector')

cascPath = sys.argv[1]
faceCascade = cv2.CascadeClassifier(cascPath)

video_capture = cv2.VideoCapture(0)
video_capture.set(3,640)
video_capture.set(4,480)

with Connection('amqp://guest:guest@localhost//') as conn:

    i = 0;
    while True:
        # Capture frame-by-frame
        ret, frame = video_capture.read()
        if i < 5:
            i = i+1
            continue
        i = 0

        frame = cv2.flip(frame,1)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(90, 90),
            flags=cv2.cv.CV_HAAR_SCALE_IMAGE
        )

        # Draw a rectangle around the faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            xc = ((x+w/2) - 320 )
            yc = ((y+h/2) - 240)
            # print (str(xc) + " " + str(yc) + " " + str(w))
            producer = conn.Producer(serializer='json')
            producer.publish({'xc': xc, 'yc': yc},
            exchange=media_exchange, routing_key='face_detector',
            declare=[face_detector_queue])

        # Display the resulting frame
        cv2.imshow('Video', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()