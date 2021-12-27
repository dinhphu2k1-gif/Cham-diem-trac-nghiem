import cv2
import numpy as np
import matplotlib.pyplot as plt
import pickle

def ScoreOfImage(path, ans, number_ans, model):
    img = cv2.imread(path, 0)

    blur = cv2.GaussianBlur(img,(5,5),0)
    thresh = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,11,2)

    horizal = thresh
    vertical = thresh

    scale_height = 20 #Scale này để càng cao thì số dòng dọc xác định sẽ càng nhiều
    scale_long = 15

    long = int(img.shape[1]/scale_long)
    height = int(img.shape[0]/scale_height)

    horizalStructure = cv2.getStructuringElement(cv2.MORPH_RECT, (long, 1))
    horizal = cv2.erode(horizal, horizalStructure, (-1, -1))
    horizal = cv2.dilate(horizal, horizalStructure, (-1, -1))

    verticalStructure = cv2.getStructuringElement(cv2.MORPH_RECT, (1, height))
    vertical = cv2.erode(vertical, verticalStructure, (-1, -1))
    vertical = cv2.dilate(vertical, verticalStructure, (-1, -1))

    mask = vertical + horizal

    contours, hierarchy = cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    
    max = -1
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        if cv2.contourArea(cnt) > max:
            x_max, y_max, w_max, h_max = x, y, w, h
            max = cv2.contourArea(cnt)

    # table = img[y_max:y_max+h_max, x_max:x_max+w_max]
    
    cropped_thresh_img = []
    cropped_origin_img = []
    countours_img = []

    if number_ans % 2 == 0:
        NUM_ROWS = int(number_ans / 2 + 1)
    else:
        NUM_ROWS = int(number_ans / 2 + 2)
    START_ROW = 1
    for i in range(START_ROW, NUM_ROWS):
        thresh1 = thresh[y_max + round(i*h_max/NUM_ROWS)+1:y_max + round((i+1)*h_max/NUM_ROWS)-1, x_max + round(w_max/4)+1:x_max +round(w_max/2)-1]
        contours_thresh1, hierarchy_thresh1 = cv2.findContours(thresh1,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        origin1 = img[y_max + round(i*h_max/NUM_ROWS) +1:y_max + round((i+1)*h_max/NUM_ROWS)-1, x_max + round(w_max/4)+1:x_max +round(w_max/2)-1]

        cropped_thresh_img.append(thresh1)
        cropped_origin_img.append(origin1)
        countours_img.append(contours_thresh1)
        
    for i in range(START_ROW, NUM_ROWS):
        thresh1 = thresh[y_max + round(i*h_max/NUM_ROWS)+1:y_max + round((i+1)*h_max/NUM_ROWS)-1, x_max + round(3*w_max/4)+1:x_max +round(w_max)-1]
        contours_thresh1, hierarchy_thresh1 = cv2.findContours(thresh1,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        origin1 = img[y_max + round(i*h_max/NUM_ROWS) +1:y_max + round((i+1)*h_max/NUM_ROWS)-1, x_max + round(3*w_max/4)+1:x_max +round(w_max)-1]

        cropped_thresh_img.append(thresh1)
        cropped_origin_img.append(origin1)
        countours_img.append(contours_thresh1)

    answer_img = {}
    for i, countour_img in enumerate(countours_img):
        for cnt in countour_img:
            if cv2.contourArea(cnt) > 30:
                x,y,w,h = cv2.boundingRect(cnt)
                if x > cropped_origin_img[i].shape[1]*0.1 and x < cropped_origin_img[i].shape[1]*0.9:
                    answer = cropped_origin_img[i][y-3:y+h+3, x-5:x+w+5]
                    answer = cv2.threshold(answer, 160, 255, cv2.THRESH_BINARY_INV)[1]
                    answer = cv2.resize(answer, (28, 28))
                    answer_img[i] = answer
    
    
    # run predcit        
    y_predict = {}

    for i in range(0, number_ans):
        y_predict[i] = 'X'

    for key in answer_img.keys():
        # print(key)
        res = model.predict(answer_img[key].reshape(-1,784))
        if res == 3:
            y_predict[key] = 'D'
        elif res == 2:
            y_predict[key] = 'C'
        elif res == 1:
            y_predict[key] = 'B'
        elif res == 0:
            y_predict[key] = 'A'
            
    print(y_predict) 
    print(ans)   
    cnt = 0
    for i in range(0, number_ans):
        # print(i)
        if ans[i] == y_predict[i]:
            cnt += 1

    return cnt/number_ans * 100


model = pickle.load(open('./knnpickle_file', 'rb'))

ans = ['D', 'D', 'C', 'X', 'C', 'B', 'X', 'X', 'X', 'C', 'X', 'D', 'X', 'X', 'X', 'C', 'C', 'A', 'B', 'D', 'A', 'D', 'B', 'D', 'C', 'A', 'A', 'D', 'A', 'C', 'B', 'A', 'X', 'A', 'B']
score = ScoreOfImage('./267549573_665571151386269_3233375091872825288_n.png', ans, 35, model )
print(score)