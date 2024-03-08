# AKSResourceManager

도커허브로 공개하기

AKS Resource Manager를 aks-resourcemanager:v1.0.0 이름으로 Docker Hub에 공개하는 절차는 다음과 같습니다. 이 과정을 진행하기 전에 Dockerfile이 준비되어 있고, 로컬 환경에서 Docker가 설치되어 있어야 합니다.

Docker 이미지 빌드:

먼저, AKS Resource Manager의 소스 코드가 있는 디렉터리에서 Docker 이미지를 빌드해야 합니다. Dockerfile이 위치한 디렉터리에서 아래 명령어를 실행합니다:

```docker build -t aks-resourcemanager:v1.0.0 . ```

이 명령어는 현재 디렉터리(.)의 Dockerfile을 사용하여 aks-resourcemanager라는 이름과 v1.0.0이라는 태그를 가진 이미지를 빌드합니다.
Docker Hub에 로그인:

Docker Hub에 이미지를 푸시하기 전에 Docker Hub 계정으로 로그인해야 합니다. 다음 명령어를 사용하여 로그인합니다:

```docker login -v docker.io```

사용자 이름과 비밀번호를 입력하여 로그인합니다.
이미지에 Docker Hub 사용자 이름 태그 추가:

Docker Hub에 이미지를 푸시하기 위해서는 이미지 이름 앞에 Docker Hub 사용자 이름을 포함해야 합니다. 예를 들어, 사용자 이름이 yourusername이라면, 다음 명령어를 사용하여 이미지에 새 태그를 추가합니다:

```docker tag aks-resourcemanager:v1.0.0 yourusername/aks-resourcemanager:v1.0.0```

이 작업은 이미지에 추가 태그를 붙이는 것으로, 원본 이미지는 그대로 유지됩니다.
이미지를 Docker Hub에 푸시:

적절한 태그를 가진 이미지를 Docker Hub에 푸시하기 위해 다음 명령어를 사용합니다:

```docker push yourusername/aks-resourcemanager:v1.0.0```

이 명령어는 yourusername/aks-resourcemanager 리포지토리에 v1.0.0 태그를 가진 이미지를 푸시합니다. 이 과정에서 Docker Hub에 해당 리포지토리가 없다면 자동으로 생성됩니다.
Docker Hub에서 확인:

푸시가 완료되면, Docker Hub 계정의 리포지토리 목록에서 aks-resourcemanager 리포지토리를 확인할 수 있습니다. 리포지토리를 클릭하면 다양한 태그를 가진 이미지들을 볼 수 있으며, v1.0.0 태그가 표시되어야 합니다.
이 과정을 통해 Docker Hub에 aks-resourcemanager:v1.0.0 이미지를 성공적으로 공개할 수 있습니다. 이제 다른 사용자나 CI/CD 파이프라인에서 이 이미지를 
```docker pull yourusername/aks-resourcemanager:v1.0.0 ```
명령어를 사용하여 다운로드할 수 있습니다.

실행 
```docker run -p 8501:8501 -v ~/.kube:/root/.kube aks_manager```