import imutils
import pytesseract
from PIL import Image
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'#응용프로그램을
# 설치하세요 위치는 알아서 탐색기에서 확인하시고..
import cv2
import numpy as np




'''

해야할 일
1. 전체 책에서 라벨 위치만 따오기 (이건 생략해도 될듯하다.)
2. 라벨을 똑바로 세우기
3. 라벨에서 문자를 추출하기.
4. isbn의 위치를 찾으면 isbn의 x,y,h는 넘겨두고 w만 라벨 전체의 길이만큼 만든뒤.
5. 거기서 모든 문자열을 추출하면 끝이난다.

'''







resultStrings=[]
#large = cv2.imread('numbers100.png')
large = cv2.imread('isbn2.jpg')#사용자가 클로즈업을 해서 사진을 찍는다면 상관이 없겠지만 그냥 책만 턱 내려놓으면 이걸로는 답이 없다.




large= cv2.resize(large, (1000, 1000)) #이미지 리사이즈 .
rgb = cv2.pyrDown(large) #이미지의 크기를 반으로 줄인다.
small = cv2.cvtColor(rgb, cv2.COLOR_BGR2GRAY)#그레이스케일 이미지.

kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
grad = cv2.morphologyEx(small, cv2.MORPH_GRADIENT, kernel)

_, bw = cv2.threshold(grad, 0.0, 255.0, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 1))#이거  getStructing Element하고 .... morphologyEx쓰면
connected = cv2.morphologyEx(bw, cv2.MORPH_CLOSE, kernel)# 그림판의 지우개 같은 느낌으로 안을 싹비우고 경계만 남기는 그거였었나....?
#canny쓰는게 훨씬더 간단하지만 뭔일이 날지 모르니 일단 소스 자체는 남겨두기로 하겠다.


# using RETR_EXTERNAL instead of RETR_CCOMP
contours, hierarchy = cv2.findContours(connected.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)#경계선을 찾아내서 분리하자.
mask = np.zeros(bw.shape, dtype=np.uint8)#왜 있는지 모르겠지만 아무것도 없는 빈 배열이다.
rgb2 =rgb.copy()#deep copy rgb2는 네모찍힐놈 그냥 rgb는 네모안찍히고 연산할놈. 이거 없애도 될듯한데....




grayScaleImg = cv2.cvtColor(rgb, cv2.COLOR_BGR2GRAY)
thersoldImg = cv2.adaptiveThreshold(grayScaleImg, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
img_canny = cv2.Canny(grayScaleImg, 50, 150)


for idx in range(len(contours)):
    x, y, w, h = cv2.boundingRect(contours[idx])
    print("x: ",x," ,y: ",y," ,w: ",w," ,h: ",h)
    #print("idx : ",idx)
    #print("contours : ",contours)
    #mask[y:y+h, x:x+w] = 0
    cv2.drawContours(mask, contours, idx, (255, 255, 255), -1)
    #r = float(cv2.countNonZero(mask[y:y+h, x:x+w])) / (w * h)
    if   w > 1 and h > 1:
    #if r > 0.45 and w > 8 and h > 8:
        cv2.rectangle(rgb2, (x, y), (x+w-1, y+h-1), (0, 255, 0), 1)
        cv2.putText(img=rgb2,text=str(idx), org=( x ,y ), color =(255, 0, 0), fontScale=1,fontFace=cv2.FONT_HERSHEY_SIMPLEX )
    textArea=rgb[y:y+h, x:x+w]#웬진 모르겠지만 인쇄해보니 역순으로 돌아간다 왜지.
    textArea = cv2.cvtColor(textArea, cv2.COLOR_BGR2GRAY)#진짜  textarea를 정확히 말하는지는 일단 둘째치고,
    #text = pytesseract.image_to_string(rgb[y:y+h, x:x+w], config='--psm 6 digits')


    text = pytesseract.image_to_string(img_canny[y-1:y+h+1, x-1:x+w+1], lang='eng')
    #약간 범위를 증가. 근데 이게 행렬 범위를 넘어버리면 문제될텐데....  정확도를 높이기 위해 adaptiveThresold 로 연산
    #그래도 연산이 안된다. Canny로 시도한 뒤 성공했다. idx 0번에서 드디어 ISBN 넘버가 나오기 시작했다.

    text = text.split('\n')[0:-1]
    text = '\n'.join(text)
    # https://stackoverflow.com/questions/64877469/problem-with-printing-to-console-with-pytessaract-in-spyder
    print("/----------------------------------")
    print("text is ",text)

    print("type of text ",type(text))

    print("location is isbn(ISBN)", text.find("isbn")," ",text.find("ISBN"))

    if text.find("isbn") >=0  or text.find("ISBN") >=0:
        print("isbn 좌표 찾음 \nidx : {}  x : {}  y : {}".format(idx,x,y)) #가장 큰 범위에서 나오는것은 의미가 없다. 어짜피 다 찾아낼것 아닌가.
        cv2.rectangle(rgb2, (x, y), (x +1, y + 1), (0, 0, 255), 1)
    else:
        print("isbn 좌표 없음 \nidx :  {}  x : {}  y : {}".format(idx,x,y))


    resultStrings.append(text)


# show image with contours rect
cv2.imshow('rects', rgb2)
cv2.imshow('line Extract ',img_canny)



print(resultStrings)
cv2.waitKey()





'''
#img = cv2.imread('numbers100.png', cv2.IMREAD_COLOR)
img = cv2.imread('isbn.jpg', cv2.IMREAD_COLOR)
img2= cv2.resize(img, (620, 480)) #이미지 리사이즈 .
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # 그레이 스케일로 변환하기.
gray = cv2.bilateralFilter(gray, 11, 17, 17)  # 흐리게 해서 노이즈 감소.
edged = cv2.Canny(gray, 30, 200)  # Perform Edge detection
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3)) #3*3크기의 반원형 붓으로
grad = cv2.morphologyEx(img2,cv2.MORPH_GRADIENT,kernel)#내부를 싹 지워서 외곽선 선따기  비슷한 개념으로 생각하자. .......
_,bw =cv2.threshold(grad,0.0,255,cv2.THRESH_BINARY|cv2.THRESH_OTSU)


# find contours in the edged image, keep only the largest
# ones, and initialize our screen contour
cnts = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:10]
screenCnt = None

# loop over our contours
for c in cnts:
    # approximate the contour
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.018 * peri, True)

    # if our approximated contour has four points, then
    # we can assume that we have found our screen
    if len(approx) == 4: #꼭지점이 4개인 이유는 매우 간단하다. 번호판이 사각형이기 때문이다.
        screenCnt = approx
        break

if screenCnt is None:
    detected = 0
    print
    "No contour detected"
else:
    detected = 1

if detected == 1:
    cv2.drawContours(img, [screenCnt], -1, (0, 255, 0), 3)

# Masking the part other than the number plate
mask = np.zeros(gray.shape, np.uint8)
new_image = cv2.drawContours(mask, [screenCnt], 0, 255, -1, )
new_image = cv2.bitwise_and(img, img, mask=mask)

# Now crop
(x, y) = np.where(mask == 255)
(topx, topy) = (np.min(x), np.min(y))
(bottomx, bottomy) = (np.max(x), np.max(y))
Cropped = gray[topx:bottomx + 1, topy:bottomy + 1]

# Read the number plate
text = pytesseract.image_to_string(gray, config='--psm 11')
print("Detected Number is:", text)

#cv2.imshow('image', img)
cv2.imshow('Cropped', gray)

cv2.waitKey(0)
cv2.destroyAllWindows()
'''