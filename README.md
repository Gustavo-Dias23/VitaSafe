# VitaSafe - Sistema Comunitário de Resposta Rápida

O **VitaSafe** é um sistema de monitoramento por visão computacional que detecta gestos de emergência com as mãos, ideal para auxiliar pessoas que dependem de equipamentos elétricos vitais. Utilizando a câmera do dispositivo e a biblioteca MediaPipe, o sistema identifica uma mão aberta por 3 segundos para acionar um alerta de emergência, e uma mão fechada por 3 segundos para cancelar o alerta. Toda a lógica é integrada a um backend Flask, que fornece status em tempo real via API e interface web.

## 🔧 Funcionalidades

- Reconhecimento de gestos (mão aberta/fechada) via webcam
- Alerta visual na interface
- Integração com backend Flask
- Histórico de ocorrências
- API REST para status e controle
- Interface web com atualização em tempo real
- Estilo visual com destaque em caso de emergência

## 🚀 Como rodar o projeto

### 1. Clone o repositório

```bash
git clone https://github.com/Gustavo-Dias23/VitaSafe
cd vitasafe
```

### 2. Crie e ative o ambiente virtual

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

### 3. Instale as dependências

```bash
pip install flask opencv-python mediapipe requests
```

### 4. Inicie o backend Flask

```bash
cd vitasafe_backend
python app.py
```

### 5. Em outro terminal, execute o script de visão computacional

```bash
python gesture_detector.py
```

### 6. Acesse a interface web

Abra [http://localhost:5000](http://localhost:5000) no navegador para visualizar o status em tempo real.

## 🧠 Tecnologias utilizadas

- Python + OpenCV + MediaPipe
- Flask (API REST e HTML rendering)
- HTML + CSS + JavaScript (interface web)
- Integração com IoT e sistemas físicos (expansível)

## 📂 Estrutura do Projeto

```
vitasafe/
│
├── vitasafe_backend/
│   ├── app.py
│   ├── status_store.py
│   └── templates/
│       └── status.html
│
├── gesture_detector.py
├── requirements.txt
└── README.md
```


Feito para promover mais segurança para pessoas com necessidades críticas de energia.
