import cv2
import mediapipe as mp
import time

# Inicialização do MediaPipe
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.7)

# Parâmetros
ALERTA_TEMPO = 3  # segundos
EMERGENCIA_ATIVA = False
TEMPO_INICIO = 0

# Função para verificar se a mão está aberta
def mao_aberta(hand_landmarks, hand_label):
    dedos = []

    if hand_label == "Right":
        dedos.append(hand_landmarks.landmark[4].x < hand_landmarks.landmark[3].x)
    else:
        dedos.append(hand_landmarks.landmark[4].x > hand_landmarks.landmark[3].x)

    for i in [8, 12, 16, 20]:
        dedos.append(hand_landmarks.landmark[i].y < hand_landmarks.landmark[i - 2].y)

    return all(dedos)

# Início da câmera
cap = cv2.VideoCapture(0)

while cap.isOpened():
    sucesso, frame = cap.read()
    if not sucesso:
        break

    # Preprocessamento
    frame = cv2.flip(frame, 1)
    imagem_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    resultado = hands.process(imagem_rgb)

    pelo_menos_uma_mao_aberta = False

    if resultado.multi_hand_landmarks and resultado.multi_handedness:
        for idx, hand_landmarks in enumerate(resultado.multi_hand_landmarks):
            hand_label = resultado.multi_handedness[idx].classification[0].label  # "Right" ou "Left"

            if mao_aberta(hand_landmarks, hand_label):
                pelo_menos_uma_mao_aberta = True

            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # Lógica de detecção de emergência
    if pelo_menos_uma_mao_aberta:
        if TEMPO_INICIO == 0:
            TEMPO_INICIO = time.time()
        elif time.time() - TEMPO_INICIO >= ALERTA_TEMPO and not EMERGENCIA_ATIVA:
            print("🔴 Emergência detectada por gesto!")
            EMERGENCIA_ATIVA = True
    else:
        TEMPO_INICIO = 0  # Reinicia o tempo

    # Mostrar aviso
    if EMERGENCIA_ATIVA:
        cv2.putText(frame, '🔴 EMERGENCIA DETECTADA', (30, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 3)

    cv2.imshow("VitaSafe - Gestos de Emergência", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):  # Tecla ESC
        break

cap.release()
cv2.destroyAllWindows()
