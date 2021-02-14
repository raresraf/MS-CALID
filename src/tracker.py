import cv2
import numpy as np

PATH_TO_VIDEO = "C:\\Users\\andre\\Downloads\\DJI_0957.MP4"
WIDTH = 1280
HEIGHT = 720

class Bbox:
    def __init__(self, label=None, confidence=None, left_x=None, top_y=None, width=None, height=None):
        self.label = label
        self.confidence = confidence
        self.left_x = left_x
        self.top_y = top_y
        self.width = width
        self.height = height
    
    def __str__(self):
        return f"{self.label}: {self.confidence}%\t(left_x: {self.left_x}\ttop_y: {self.top_y}\twidth:\t{self.width}\theight:\t{self.height})"
    
    def __repr__(self):
        return f"{self.label}: {self.confidence}%\t(left_x: {self.left_x}\ttop_y: {self.top_y}\twidth:\t{self.width}\theight:\t{self.height})"

def getBboxesByFrame():
    bboxesByFrame = {}
    id = 1

    with open("results.txt", "r") as f:
        line = f.readline()
        while line:
            if line.strip() == "Objects:":
                bboxes = []

                f.readline() ## Skip empty line

                line = f.readline()
                while line:
                    if len(line.strip()) == 0:
                        break
                    
                    s = line.replace(' , ', '').split("%")

                    for i in range(len(s) - 1):
                        bbox = Bbox()

                        bbox.label, bbox.confidence = s[i].split(": ")

                        s[-1] = s[-1].strip()
                        s[-1] = s[-1][:len(s[-1]) - 1]
                        bbox.left_x, bbox.top_y, bbox.width, bbox.height = [int(x) for x in s[-1].split() if x.isdigit()]

                        bboxes.append(bbox)

                    line = f.readline()
                
                bboxesByFrame[id] = bboxes
                id += 1

            line = f.readline()

    return bboxesByFrame


bboxesByFrame = getBboxesByFrame()

cap = cv2.VideoCapture(PATH_TO_VIDEO)

width  = cap.get(cv2.CAP_PROP_FRAME_WIDTH)   # float `width`
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)  # float `height`

div_x = width / WIDTH
div_y = height / HEIGHT

colors = {}

# fourcc = cv2.VideoWriter_fourcc(*'XVID')
# out = cv2.VideoWriter('output.avi',fourcc, 20.0, (1280, 720))

trackers = cv2.MultiTracker_create()
# for bbox in bboxesByFrame[1]:
#     if bbox.label in ['house', 'hotel']:
#         tracker = cv2.TrackerCSRT_create()
#         trackers.add(tracker, frame, (int(bbox.left_x / div_x), int(bbox.top_y / div_y), int((bbox.left_x + bbox.width) / div_x), int((bbox.top_y + bbox.height) / div_y)))

sw = False
id = 1
while cap.isOpened():
    print(id)
    # if id >= 700:
    #     break
    ret, frame = cap.read()

    frame = cv2.resize(frame, (1280, 720), fx=0, fy=0, interpolation = cv2.INTER_CUBIC)

    if sw == False and id >= 480:
        for bbox in bboxesByFrame[id]:
            if bbox.label in ['church']:
                print("Church")
                p1 = (int(bbox.left_x / div_x), int(bbox.top_y / div_y))
                p2 = (int((bbox.left_x + bbox.width) / div_x), int((bbox.top_y + bbox.height) / div_y))


                bbox = cv2.selectROI(frame, False)
                tracker = cv2.TrackerCSRT_create()
                trackers.add(tracker, frame, bbox)
                sw = True


    (success, boxes) = trackers.update(frame)
    for box in boxes:
        if id >= 650:
            break
        (x, y, w, h) = [int(v) for v in box]
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(frame, "Church 1", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)

    # if id >= 450:
    #     out.write(frame)

    # for bbox in bboxesByFrame[id]:
    #     if bbox.label in ['house', 'hotel', 'church']:
    #         if bbox.label not in colors:
    #             colors[bbox.label] = list(np.random.random(size=3) * 256)
    #         color = colors[bbox.label]

    #         p1 = (int(bbox.left_x / div_x), int(bbox.top_y / div_y))
    #         p2 = (int((bbox.left_x + bbox.width) / div_x), int((bbox.top_y + bbox.height) / div_y))

    #         cv2.rectangle(frame, p1, p2, color, 1)
    #         cv2.putText(frame, bbox.label, p1, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)


    cv2.imshow('Video', frame)
    # cv2.imwrite("frame%d.jpg" % count, frame)
    id += 1
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break


cap.release()
out.release()

cv2.destroyAllWindows() # destroy all opened windows