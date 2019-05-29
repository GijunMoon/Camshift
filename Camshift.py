from __future__ import print_function #import
import sys
import cv2
from random import randint

trackerTypes = ['BOOSTING', 'MIL', 'KCF','TLD', 'MEDIANFLOW', 'GOTURN', 'MOSSE', 'CSRT'] #트레커 타입 열거

def createTrackerByName(trackerType):
  # 트레커를 이름에 따라 생성합니다.
  if trackerType == trackerTypes[0]:
    tracker = cv2.TrackerBoosting_create()
  elif trackerType == trackerTypes[1]: 
    tracker = cv2.TrackerMIL_create()
  elif trackerType == trackerTypes[2]:
    tracker = cv2.TrackerKCF_create()
  elif trackerType == trackerTypes[3]:
    tracker = cv2.TrackerTLD_create()
  elif trackerType == trackerTypes[4]:
    tracker = cv2.TrackerMedianFlow_create()
  elif trackerType == trackerTypes[5]:
    tracker = cv2.TrackerGOTURN_create()
  elif trackerType == trackerTypes[6]:
    tracker = cv2.TrackerMOSSE_create()
  elif trackerType == trackerTypes[7]:
    tracker = cv2.TrackerCSRT_create()
  else:
    tracker = None
    print('틀린 트레커 이름입니다')
    print('현재 작동하는 트레커:')
    for t in trackerTypes:
      print(t)
    
  return tracker

if __name__ == '__main__':

  print("기본적인 트레커는 CSRT에 기반합니다. \n"
        "현재 작동하는 트레커:\n")
  for t in trackerTypes:
      print(t)      

  trackerType = "KCF"      #현재 트레커 타입


  videoPath = "videos/vd.MP4" #영상 경로
  

  cap = cv2.VideoCapture(videoPath) #영상 추출
 

  success, frame = cap.read()

  if not success:
    print('영상 읽기에 실패하였습니다.') #영상 추출에 실패했을 경우
    sys.exit(1)


  bboxes = []
  colors = [] 


  while True:
   
    bbox = cv2.selectROI('MultiTracker', frame) #ROI
    bboxes.append(bbox)
    colors.append((randint(64, 255), randint(64, 255), randint(64, 255)))
    print("q를 눌러 트레킹을 시작합니다.")
    print("아무 키를 눌러 다음 영역을 지정합니다.")
    j = cv2.waitKey(0) & 0xFF #q가 눌리면
    if (j == 113):  
      break
  
  print('선택된 영역 {}'.format(bboxes))

 
  multiTracker = cv2.MultiTracker_create() #트레커 생성


  for bbox in bboxes:
    multiTracker.add(createTrackerByName(trackerType), frame, bbox)


  while cap.isOpened():
    success, frame = cap.read()
    if not success:
      break
    

    success, boxes = multiTracker.update(frame)


    for i, newbox in enumerate(boxes): #바운딩 박스
      p1 = (int(newbox[0]), int(newbox[1]))
      p2 = (int(newbox[0] + newbox[2]), int(newbox[1] + newbox[3]))
      cv2.rectangle(frame, p1, p2, colors[i], 2, 1)


    cv2.imshow('MultiTracker', frame)
    

    if cv2.waitKey(1) & 0xFF == 27:   #esc로 종료
        break