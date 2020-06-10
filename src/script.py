from datetime import datetime

import cv2 as cv
import pandas as pd

first_frame = None
status_list = [None, None]
time_list = []
df = pd.DataFrame(columns=["START", "END"])

cap = cv.VideoCapture(0)

while True:
    check, frames = cap.read()
    status = 0
    gray_img = cv.cvtColor(frames, cv.COLOR_BGR2GRAY)
    gray_img = cv.GaussianBlur(gray_img, (21, 21), 0)

    if first_frame is None:
        first_frame = gray_img
        continue

    delta_frame = cv.absdiff(first_frame, gray_img)
    threshold_img = cv.threshold(delta_frame, 30, 255, cv.THRESH_BINARY)[1]
    dilate_img = cv.dilate(threshold_img, None, iterations=5)

    (cnts, _) = cv.findContours(threshold_img.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    for contour in cnts:
        if cv.contourArea(contour) < 5000:
            continue
        status = 1
        (x, y, w, h) = cv.boundingRect(contour)
        cv.rectangle(frames, (x, y), (x + w, y + h), (0, 255, 0), 1)

    status_list.append(status)
    if status_list[-1] == 1 and status_list[-2] == 0:
        time_list.append(datetime.now())
    if status_list[-1] == 0 and status_list[-2] == 1:
        time_list.append(datetime.now())

    cv.imshow("thresh image", threshold_img)
    cv.imshow("delta frame", delta_frame)
    cv.imshow("dilated image", dilate_img)
    cv.imshow("resulted frame", frames)

    key = cv.waitKey(1)

    if key == ord('q'):
        if status == 1:
            time_list.append(datetime.now())
        break

print(status_list)
print(time_list)

for i in range(0, len(time_list), 2):
    df = df.append({"START": time_list[i], "END": time_list[i + 1]}, ignore_index=True)

df.to_csv("Time.csv")

cap.release()
cv.destroyAllWindows()
