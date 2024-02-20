import cv2

# Carregar imagem
imagem = cv2.imread('teste.jpg')
imagem_gray = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)

# Inicializar o detector ORB
orb = cv2.ORB_create()

# Encontrar pontos chave e descritores
kp, desc = orb.detectAndCompute(imagem_gray, None)

# Desenhar pontos chave na imagem
imagem_com_pontos = cv2.drawKeypoints(imagem, kp, None, color=(0,255,0), flags=0)

# Exibir imagem com pontos chave
cv2.imshow('Pontos chave ORB', imagem_com_pontos)
cv2.waitKey(0)
cv2.destroyAllWindows()
