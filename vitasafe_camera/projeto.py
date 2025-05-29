import cv2
import mediapipe as mp
import time
import requests

# Inicialização do MediaPipe
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.7)

# Parâmetros
ALERTA_TEMPO = 3
CANCELAMENTO_TEMPO = 3
emergencia_ativa = False
tempo_inicio_alerta = 0
tempo_inicio_cancelamento = 0

# Backend Flask
FLASK_API = "http://localhost:5000/api/emergencia"

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

# Enviar status para o backend
def atualizar_emergencia(ativa):
    try:
        requests.post(FLASK_API, json={"ativa": ativa}, timeout=1)
    except requests.RequestException as e:
        print("Erro ao comunicar com o backend:", e)

# Início da câmera
cap = cv2.VideoCapture(0)

while cap.isOpened():
    sucesso, frame = cap.read()
    if not sucesso:
        break

    frame = cv2.flip(frame, 1)
    imagem_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    resultado = hands.process(imagem_rgb)

    mao_visivel_e_aberta = False
    mao_visivel_e_fechada = False

    if resultado.multi_hand_landmarks and resultado.multi_handedness:
        for idx, hand_landmarks in enumerate(resultado.multi_hand_landmarks):
            hand_label = resultado.multi_handedness[idx].classification[0].label
            aberta = mao_aberta(hand_landmarks, hand_label)

            if aberta:
                mao_visivel_e_aberta = True
            else:
                mao_visivel_e_fechada = True

            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # Lógica de ativação de emergência
    if not emergencia_ativa:
        if mao_visivel_e_aberta:
            if tempo_inicio_alerta == 0:
                tempo_inicio_alerta = time.time()
            elif time.time() - tempo_inicio_alerta >= ALERTA_TEMPO:
                print("🔴 Emergência detectada por gesto!")
                emergencia_ativa = True
                atualizar_emergencia(True)
                tempo_inicio_alerta = 0
        else:
            tempo_inicio_alerta = 0
    else:
        # Cancelamento apenas se mão fechada visível por 3 segundos
        if mao_visivel_e_fechada:
            if tempo_inicio_cancelamento == 0:
                tempo_inicio_cancelamento = time.time()
            elif time.time() - tempo_inicio_cancelamento >= CANCELAMENTO_TEMPO:
                print("✅ Emergência cancelada por gesto!")
                emergencia_ativa = False
                atualizar_emergencia(False)
                tempo_inicio_cancelamento = 0
        else:
            tempo_inicio_cancelamento = 0

    # Mensagem visual
    if emergencia_ativa:
        cv2.putText(frame, '🔴 EMERGENCIA DETECTADA', (30, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 3)
    else:
        cv2.putText(frame, '🟢 Tudo normal', (30, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 100, 0), 2)

    cv2.imshow("VitaSafe - Gestos de Emergência", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
