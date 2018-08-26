import cv2
import numpy as np


def update_pts(params, x, y):
    global x_init, y_init
    params["top_left_pt"] = (min(x_init, x), min(y_init, y))
    params["bottom_right_pt"] = (max(x_init, x), max(y_init, y))



def draw_rectangle(event, x, y, flags, params):
    global selected
    global x_init, y_init, drawing
 
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        x_init, y_init = x, y

    elif event == cv2.EVENT_MOUSEMOVE and drawing:
        update_pts(params, x, y)

    elif event == cv2.EVENT_LBUTTONUP:
        selected=True
        drawing = False
        update_pts(params, x, y)



if __name__ == '__main__':
    drawing = False
    event_params = {"top_left_pt": (-1, -1), "bottom_right_pt": (-1, -1)}
    selected=False
	video_path='Video path here'
    cap = cv2.VideoCapture(video_path)
    tracker=cv2.TrackerMIL_create()
    initialized=False
    bbox1=[]





   
    if not cap.isOpened():
        raise IOError("Cannot open webcam")

    cv2.namedWindow('Webcam')

    cv2.setMouseCallback('Webcam', draw_rectangle, event_params)


    bbox=()
    while True:

        while True:
            ok, frame = cap.read()
            print 'read initialized'
            img = cv2.resize(frame, None, fx=1, fy=1, interpolation=cv2.INTER_AREA)
            print 'image resized'
            (x0, y0), (x1, y1) = event_params["top_left_pt"], event_params["bottom_right_pt"]
            cv2.rectangle(img, (x0, y0), (x1, y1), (255, 255, 255), 2)
            print 'rectangle initialized'
            bbox1=[x0,y0,x1-x0,y1-y0]

            if selected:
                bbox = tuple(bbox1)
                tracked=tracker.init(frame,bbox)

                if not ok:
                    break
                ok,bbox=tracker.update(img)
                if ok:
                        p1=(int(bbox[0]),int(bbox[1]))
                        p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
                        cv2.rectangle(img,p1,p2,(255,0,0),2,1)
                else:
                        cv2.putText(frame, "Tracking failure detected", (100, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,
                                    (0, 0, 255), 2)

            cv2.imshow('Webcam', img)

            c = cv2.waitKey(5)
            if c == 27:
                break



        cap.release()
        cv2.destroyAllWindows()