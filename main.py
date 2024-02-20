import cv2
import numpy as np

#Carregamentos da imagens das imagem para comparação
orb = cv2.ORB_create()
imagem_bd = cv2.imread('teste.jpg')
imagem_bd_cor = cv2.cvtColor(imagem_bd, cv2.COLOR_BGR2GRAY)
kp, descricao = orb.detectAndCompute(imagem_bd_cor,None)

#Recebendo Imagem da camara
video_capture = cv2.VideoCapture(0)#Capturando a imagem que vem da camara

try:
    faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    eyeCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
    print(faceCascade)
except FileExistsError:
    print("Erro: Arquivo do classificador de rosto não encontrado.")
    exit()

while True:
    ret, frame = video_capture.read()
    if not ret:
         break
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)#Dando do objecto ou rosto identificado
    faces = faceCascade.detectMultiScale(
          gray,
          scaleFactor=1.1,
          minNeighbors=5,
          minSize=(30,30)
    )
    for (x,y,w,h) in faces:
          #Desenhar um retangulo em volta do rosto
          cv2.rectangle(frame,(x,y),(x+w, y+h),(0,255,0),2)
          olhos = eyeCascade.detectMultiScale(gray[y:y+h, x:x+w],
               scaleFactor=1.1,
               minNeighbors=5,
               minSize=(30,30))
          for (ox,oy,ow,oh) in olhos:
               cv2.rectangle(frame, (x+ox, y+oy), (x+ox+ow, y+oy+oh),(255,0,0),2)
          #pegando pontos chaves na região do rosto usando orb
          kp_rosto, descricao_rosto = orb.detectAndCompute(gray[y:y+h,x:x+w],None)

          #Comparando as descrições dos pontos chaves dos objectos
          if descricao_rosto is not None and descricao is not None:
               bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
               matches = bf.match(descricao,descricao_rosto)

               #Limite de correspondencia
               limite = 10
               if len(matches)> limite:
                    cv2.putText(frame,"É a mesma pessoa",(x,y-10),cv2.FONT_HERSHEY_COMPLEX, 0.9,(0,255,0),2)
    cv2.imshow('Detetação',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
         break

video_capture.release()
cv2.destroyAllWindows()    
