import cv2
import numpy as np

PATH_TO_VIDEO = ""

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

x = width / 1280
y = height / 720

colors = {}

# tracker = cv2.TrackerCSRT_create()

id = 1
while cap.isOpened():
    ret, frame = cap.read()

    frame = cv2.resize(frame, (1280, 720), fx=0, fy=0, interpolation = cv2.INTER_CUBIC)

    

    for bbox in bboxesByFrame[id]:
        if bbox.label in ['house', 'hotel']:
            if bbox.label not in colors:
                colors[bbox.label] = list(np.random.random(size=3) * 256)
            color = colors[bbox.label]

            p1 = (int(bbox.left_x / x), int(bbox.top_y / y))
            p2 = (int((bbox.left_x + bbox.width) / x), int((bbox.top_y + bbox.height) / y))

            cv2.rectangle(frame, p1, p2, color, 1)
            cv2.putText(frame, bbox.label, p1, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)

    
    cv2.imshow('Video', frame)
    # cv2.imwrite("frame%d.jpg" % count, frame)
    id += 1
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break
    
    


cap.release()
cv2.destroyAllWindows() # destroy all opened windows