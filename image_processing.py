import cv2
import numpy as np
import time
import pickle


def update_pts(params, x, y):
    global x_init, y_init
    params["top_left_pt"] = (min(x_init, x), min(y_init, y))
    params["bottom_right_pt"] = (max(x_init, x), max(y_init, y))
    #img[y_init:y, x_init:x] = 255 - img[y_init:y, x_init:x]


def draw_rectangle(event, x, y, flags, params):
    global selected
    global x_init, y_init, drawing
    # First click initialize the init rectangle point
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        x_init, y_init = x, y
        # Meanwhile mouse button is pressed, update diagonal rectangle point
    elif event == cv2.EVENT_MOUSEMOVE and drawing:
        update_pts(params, x, y)
        # Once mouse botton is release
    elif event == cv2.EVENT_LBUTTONUP:
        selected=True
        drawing = False
        update_pts(params, x, y)



if __name__ == '__main__':
    drawing = False
    event_params = {"top_left_pt": (-1, -1), "bottom_right_pt": (-1, -1)}
    selected=False

    cap = cv2.VideoCapture(0)
    tracker=cv2.TrackerMOSSE_create()
    #csrt,kcf,mil,mosse
    initialized=False
    bbox1=[]





    # Check if the webcam is opened correctly
    if not cap.isOpened():
        raise IOError("Cannot open webcam")

    cv2.namedWindow('Webcam')
    # Bind draw_rectangle function to every mouse event
    cv2.setMouseCallback('Webcam', draw_rectangle, event_params)
    #(x0, y0), (x1, y1) = event_params["top_left_pt"], event_params["bottom_right_pt"]
    
   
    width=cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height=cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    orta_x=int(width/2)
    orta_y=int(height/2)
    

    bbox=()
    axy=[orta_x,orta_y]
    file_output='xdxd.avi'
    fourcc=cv2.VideoWriter_fourcc(*'FMP4')
    out=cv2.VideoWriter(file_output,fourcc,20.0,(int(width),int(height)))
    fp=open("pay1.pkl","wb")
    pickle.dump(axy,fp,protocol=2)
    fp.close()


    while True:
        ok, frame = cap.read()
        frame=cv2.flip(frame,-1)
        #print 'okuma basladi'
        img = cv2.resize(frame, None, fx=1, fy=1, interpolation=cv2.INTER_AREA)
        
        #print 'image resized'
        (x0, y0), (x1, y1) = event_params["top_left_pt"], event_params["bottom_right_pt"]
        cv2.rectangle(img, (x0, y0), (x1, y1), (255, 255, 255), 2)
        #print 'rectangle init'
        bbox1=[x0,y0,x1-x0,y1-y0]

        if selected:
            bbox = tuple(bbox1)
            tracked=tracker.init(img,bbox)
            #print 'bbox olusturuldu'



        #print 'okumaya devam'
        if not ok:
            break
        ret,bbox=tracker.update(img)
        if ret:
            p1=(int(bbox[0]),int(bbox[1]))
            p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
            cv2.rectangle(img,p1,p2,(255,0,0),2,1)
            a_x=int(2*bbox[0]+bbox[2])/2
            a_y=int(2*bbox[1]+bbox[3])/2
            axy=[a_x,a_y]
            cv2.arrowedLine(img, (320, 480), (int(a_x),int(a_y)), (255, 255, 255), 2)
            
        else:
            cv2.putText(img, "Tracking failure detected", (100, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,
                                    (0, 0, 255), 2)
            axy=[orta_x,orta_y]
        
        #a_x=int(2*bbox[0]+bbox[2])/2
        #a_y=int(2*bbox[1]+bbox[3])/2
        #axy=[a_x,a_y]
        print (axy)
        fp=open("pay1.pkl","wb")
        pickle.dump(axy,fp,protocol=2)
        fp.close()
        #cv2.arrowedLine(img, (320, 480), (int(a_x),int(a_y)), (255, 255, 255), 2)
        out.write(img)
        
                       
        cv2.imshow('Webcam', img)
        
        c = cv2.waitKey(5)
        if c == 27:
            axy=[orta_x,orta_y]
            fp=open("pay1.pkl","wb")
            pickle.dump(axy,fp,protocol=2)
            fp.close()
            print(axy)
            time.sleep(0.5)
            break
        #print(orta_x)
        #print(orta_y)

    
    cap.release()
    out.release()
    cv2.destroyAllWindows()
