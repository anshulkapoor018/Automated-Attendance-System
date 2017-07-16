import cv2

def facechop(image):
    facedata = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    img = cv2.imread(image)

    minisize = (img.shape[1],img.shape[0])
    miniframe = cv2.resize(img, minisize)

    faces = facedata.detectMultiScale(miniframe)

    for f in faces:
        x, y, w, h = [ v for v in f ]
        cv2.rectangle(img, (x,y), (x+w,y+h), (255,255,255))
        sub_face = img[y:y+h, x:x+w]
        face_file_name = "face_" + str(y) + ".jpg"
        #resized_image = cv2.resize(sub_face, (125, 150))
        cv2.imwrite(face_file_name, sub_face)
        #cv2.imshow(image, img)
    return

if __name__:
    facechop("group4.jpg")
    facechop("1.jpg")
    facechop("2.jpg")
    facechop("3.jpg")
    facechop("4.jpg")
    facechop("5.jpg")
    facechop("6.jpg")
    facechop("7.jpg")
    facechop("8.jpg")
    facechop("9.jpg")
    facechop("10.jpg")
    facechop("11.jpg")
    facechop("12.jpg")
    facechop("13.jpg")
    facechop("14.jpg")
    facechop("15.jpg")
    facechop("16.jpg")
    facechop("17.jpg")
    facechop("18.jpg")
    facechop("19.jpg")
    facechop("group2.jpg")
    facechop("group3.jpg")
    facechop("hello.jpg")
    facechop("group4.jpg")