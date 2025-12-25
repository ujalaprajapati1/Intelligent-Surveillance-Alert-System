import cv2
import threading
import winsound

hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

camera = cv2.VideoCapture(0)

ALERT_ENABLED = True
alarm_playing = False
prev_gray = None


def set_alert_state():
    global ALERT_ENABLED
    ALERT_ENABLED = not ALERT_ENABLED
    return ALERT_ENABLED


def play_alarm():
    global alarm_playing
    if ALERT_ENABLED and not alarm_playing:
        alarm_playing = True
        winsound.Beep(1200, 400)
        alarm_playing = False


def generate_frames():
    global prev_gray

    while True:
        success, frame = camera.read()
        if not success:
            continue

        frame = cv2.resize(frame, (640, 480))
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (21, 21), 0)

        if prev_gray is None:
            prev_gray = blur
            continue

        delta = cv2.absdiff(prev_gray, blur)
        thresh = cv2.threshold(delta, 25, 255, cv2.THRESH_BINARY)[1]
        motion_pixels = cv2.countNonZero(thresh)
        prev_gray = blur

        bodies, _ = hog.detectMultiScale(frame, winStride=(8, 8))
        human_detected = len(bodies) > 0 or motion_pixels > 5000

        if human_detected and ALERT_ENABLED:
            threading.Thread(target=play_alarm, daemon=True).start()

        for (x, y, w, h) in bodies:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
            cv2.putText(
                frame,
                "HUMAN DETECTED",
                (x, y-10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 0, 255),
                2
            )

        if motion_pixels > 5000:
            cv2.putText(
                frame,
                "MOTION DETECTED",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (255, 255, 0),
                2
            )

        ret, buffer = cv2.imencode(".jpg", frame)
        frame = buffer.tobytes()

        yield (b"--frame\r\n"
               b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")
