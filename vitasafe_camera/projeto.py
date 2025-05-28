# camera_emergencia.py

import cv2
import mediapipe as mp
import time
import requests

# MediaPipe setup
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.7)

# Parâmetros
ALERTA_TEMPO = 3  # segundos
TEMPO_INICIO = 0
EMERGENCIA_ATIVA = False

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

    frame = cv2.flip(frame, 1)
    imagem_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    resultado = hands.process(imagem_rgb)

    pelo_menos_uma_mao_aberta = False
    alguma_mao_fechada = False

    if resultado.multi_hand_landmarks and resultado.multi_handedness:
        for idx, hand_landmarks in enumerate(resultado.multi_hand_landmarks):
            hand_label = resultado.multi_handedness[idx].classification[0].label
            aberta = mao_aberta(hand_landmarks, hand_label)
            if aberta:
                pelo_menos_uma_mao_aberta = True
            else:
                alguma_mao_fechada = True

            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    tempo_atual = time.time()

    # Lógica de ativação
    if pelo_menos_uma_mao_aberta and not EMERGENCIA_ATIVA:
        if TEMPO_INICIO == 0:
            TEMPO_INICIO = tempo_atual
        else:
            tempo_mantido = tempo_atual - TEMPO_INICIO
            cv2.putText(frame, f'Tempo com mao aberta: {int(tempo_mantido)}s', (30, 100),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)

            if tempo_mantido >= ALERTA_TEMPO:
                print("🔴 Emergência detectada por gesto!")
                EMERGENCIA_ATIVA = True
                try:
                    requests.post("http://localhost:5000/api/emergencia", json={"ativa": True})
                except:
                    print("⚠️ Não foi possível comunicar com o backend.")
                TEMPO_INICIO = 0
    else:
        if not EMERGENCIA_ATIVA:
            TEMPO_INICIO = 0

    # Cancelamento
    if EMERGENCIA_ATIVA and alguma_mao_fechada:
        print("✅ Emergência cancelada por gesto.")
        EMERGENCIA_ATIVA = False
        try:
            requests.post("http://localhost:5000/api/emergencia", json={"ativa": False})
        except:
            print("⚠️ Não foi possível comunicar com o backend.")

    # Mostrar alerta
    if EMERGENCIA_ATIVA:
        cv2.putText(frame, '🔴 EMERGENCIA DETECTADA', (30, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 3)

    cv2.imshow("VitaSafe - Gestos de Emergência", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
