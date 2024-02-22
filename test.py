import random
import cv2
import numpy as np
from ultralytics import YOLO
import arduino as sl

# opening the file in read mode
my_file = open("utils/coco.txt", "r")
# reading the file
data = my_file.read()
# replacing end splitting the text | when newline ('\n') is seen.
class_list = data.split("\n")
my_file.close()

port = 'COM4'
baud = 9600

# print(class_list)

regions = {
    "region1": 0,
    "region2": 0,
    "region3": 0,
    "region4": 0
}

f = open("output.txt", "w")

# Generate random colors for class list
detection_colors = []
for i in range(len(class_list)):
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    detection_colors.append((b, g, r))

# load a pretrained YOLOv8n model
model = YOLO("weights/yolov8n.pt", "v8")

# Vals to resize video frames | small frame optimise the run
frame_wid = 640
frame_hyt = 480
j = 0
k = [0,0,0,0]
# cap = cv2.VideoCapture(1)
cap = cv2.VideoCapture("inference/videos/7.mp4")

if not cap.isOpened():
    print("Cannot open camera")
    exit()

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    # if frame is read correctly ret is True

    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    #  resize the frame | small frame optimise the run
    # frame = cv2.resize(frame, (frame_wid, frame_hyt))

    # Predict on image
    detect_params = model.predict(source=[frame], conf=0.45, save=False)

    # Convert tensor array to numpy
    DP = detect_params[0].numpy()
    #print(DP)

    if len(DP) != 0:
        for i in range(len(detect_params[0])):
            #print(i)
            boxes = detect_params[0].boxes
            box = boxes[i]  # returns one box
            clsID = box.cls.numpy()[0]
            conf = box.conf.numpy()[0]
            bb = box.xyxy.numpy()[0]

            if clsID == 0:
                cv2.rectangle(
                    frame,
                    (int(bb[0]), int(bb[1])),
                    (int(bb[2]), int(bb[3])),
                    detection_colors[int(clsID)],
                    3,
                )

                y = (bb[3] + bb[1])//2
                x = (bb[2] + bb[0])//2

                if x < frame_wid/2:
                    if y < frame_hyt/2:
                        if (not regions["region1"]):
                            regions["region1"] = 1
                            k[0]+=1
                    else:
                        if (not regions["region3"]):
                            regions["region3"] = 1
                            k[2]+=1
                else:
                    if y < frame_hyt/2:
                        if (not regions["region2"]):
                            regions["region2"] = 1
                            k[1]+=1
                    else:
                        if (not regions["region4"]):
                            regions["region4"] = 1
                            k[3]+=1
                #print("\n\n" + str(region) + "\n" + str(x) + " " + str(y))
                # Display class name and confidence
                font = cv2.FONT_HERSHEY_COMPLEX
                cv2.putText(
                    frame,
                    class_list[int(clsID)] + " " + str(round(conf, 3)) + "%",
                    (int(bb[0]), int(bb[1]) - 10),
                    font,
                    1,
                    (255, 255, 255),
                    2,
                )
    #print(regions)
    # Display the resulting frame
    cv2.imshow("ObjectDetection", frame)
    j = j + 1
    regions = dict.fromkeys(regions, 0)
    if j >= 50:
        if k[0]>30:
            regions["region1"] = 1
        if k[1]>30:
            regions["region2"] = 1
        if k[2]>30:
            regions["region3"] = 1
        if k[3]>30:
            regions["region4"] = 1
        #print("\nResult = " + str(regions) + "\n\n")
        f.write(str(regions) + "\n")
        sl.send_list_to_arduino(list(regions.values()))
        k = [0, 0, 0, 0]
        j = 0

    regions = dict.fromkeys(regions, 0)


    # Terminate run when "Q" pressed
    if cv2.waitKey(1) == ord("q"):
        break
#print("\n\n frames = " + str(j))
sl.send_list_to_arduino(list(regions.values()))
sl.close_serial_port()
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
