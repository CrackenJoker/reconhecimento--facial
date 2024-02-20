import cv2
import numpy as np

# Inicializar detector ORB
orb = cv2.ORB_create()

# Carregar a imagem de referência para comparação
imagem_referencia = cv2.imread('teste.jpg')
imagem_referencia_gray = cv2.cvtColor(imagem_referencia, cv2.COLOR_BGR2GRAY)
kp_referencia, desc_referencia = orb.detectAndCompute(imagem_referencia_gray, None)

# Inicializar os classificadores para detecção facial e ocular
faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eyeCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

# Inicializar a captura de vídeo da câmera
video_capture = cv2.VideoCapture(0)

while True:
    # Capturar o próximo quadro da câmera
    ret, frame = video_capture.read()
    if not ret:
        break

    # Converter o quadro para escala de cinza
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detectar rostos na imagem em escala de cinza
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30)
    )

    # Para cada rosto detectado
    for (x, y, w, h) in faces:
        # Desenhar um retângulo em volta do rosto
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        # Detectar olhos dentro da região do rosto
        eyes = eyeCascade.detectMultiScale(gray[y:y+h, x:x+w], scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(frame, (x+ex, y+ey), (x+ex+ew, y+ey+eh), (255, 0, 0), 2)

        # Detectar pontos chave na região do rosto usando ORB
        kp_rosto, desc_rosto = orb.detectAndCompute(gray[y:y+h, x:x+w], None)

        # Comparar os descritores dos pontos chave do rosto com os da imagem de referência
        if desc_rosto is not None and desc_referencia is not None:
            bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
            matches = bf.match(desc_referencia, desc_rosto)
            # Defina um limite de correspondência para determinar se é a mesma pessoa
            limite_correspondencia = 10
            if len(matches) > limite_correspondencia:
                cv2.putText(frame, "Mesma pessoa", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    # Exibir o quadro resultante
    cv2.imshow('Video', frame)

    # Verificar se o usuário pressionou a tecla 'q' para sair
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar recursos e fechar janelas
video_capture.release()
cv2.destroyAllWindows()
