# build : docker build -t aks_manager .
# run : docker run -p 8501:8501 -v ~/.kube:/root/.kube aks_manager
# run 기본 참조 : docker run -p 8501:8501 aks_manager

# 기본 이미지 설정
FROM python:3.8

# 작업 디렉터리 설정
WORKDIR /app

# 현재 디렉터리의 내용을 컨테이너의 /app으로 복사
COPY . /app

# requirements.txt에 명시된 필요한 패키지들을 설치
RUN pip install --no-cache-dir -r requirements.txt

# kubectl 설치
RUN apt-get update && apt-get install -y curl && \
    curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl" && \
    chmod +x ./kubectl && \
    mv ./kubectl /usr/local/bin/kubectl

# 컨테이너 외부로 노출할 포트 지정
EXPOSE 8501

# 컨테이너 시작 시 실행될 명령어
CMD ["streamlit", "run", "aks_manager.py", "--server.port=8501"]
