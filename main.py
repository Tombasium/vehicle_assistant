import cv2
import numpy as np
from datetime import datetime

import gps_module


def get_gps_vel():
    return gps.velocity


def get_can_vel():
    return str(round(np.random.random(), 2))


def get_latitude():
    return str(round(np.random.random(), 8))


def get_longitude():
    return str(round(np.random.random(), 8))


def get_time():
    now = datetime.now()
    return now.strftime("%d/%m/%Y %H:%M:%S")


def get_mpg():
    return str(round(np.random.random(), 1))


def main():
    cap = cv2.VideoCapture(0)
    gps = gps_module.GpsModule()

    while (True):

        # Capture frames in the video
        ret, frame = cap.read()

        time = get_time()

        gps.update_data()

        gps_vel = "GPS vel : %s" % gps.velocity
        can_vel = "CAN vel : %s" % get_can_vel()

        lat = "Lat   : %s%s" % (gps.latitude, gps.lat_hemisphere)
        long = "Long : %s%s" % (gps.longitude, gps.long_hemisphere)

        mpg = "MPG : %s" % get_mpg()
        heading = "Heading : %s" % gps.heading

        # describe the type of font
        # to be used.
        font = cv2.FONT_HERSHEY_SIMPLEX

        # Use putText() method for
        # inserting text on video

        cv2.putText(frame,
                    time,
                    (5, 20),
                    font, 0.5,
                    (0, 255, 0),
                    1,
                    cv2.LINE_4)
        cv2.putText(frame,
                    gps_vel,
                    (5, 455),
                    font, 0.5,
                    (0, 255, 0),
                    1,
                    cv2.LINE_4)
        cv2.putText(frame,
                    can_vel,
                    (5, 475),
                    font, 0.5,
                    (0, 255, 0),
                    1,
                    cv2.LINE_4)
        cv2.putText(frame,
                    lat,
                    (150, 455),
                    font, 0.5,
                    (0, 255, 0),
                    1,
                    cv2.LINE_4)
        cv2.putText(frame,
                    long,
                    (150, 475),
                    font, 0.5,
                    (0, 255, 0),
                    1,
                    cv2.LINE_4)
        cv2.putText(frame,
                    mpg,
                    (440, 455),
                    font, 0.5,
                    (0, 255, 0),
                    1,
                    cv2.LINE_4)
        cv2.putText(frame,
                    heading,
                    (440, 475),
                    font, 0.5,
                    (0, 255, 0),
                    1,
                    cv2.LINE_4)

        # Display the resulting frame
        cv2.imshow('video', frame)

        # creating 'q' as the quit
        # button for the video
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # release the cap object
    cap.release()
    # close all windows
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()