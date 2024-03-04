# pip install -U hydralit_components : https://github.com/TangleSpace/hydralit_components
import streamlit as st
import hydralit_components as hc
import subprocess
import pandas as pd
import re

# Streamlit 앱의 페이지 설정
st.set_page_config(page_title="AKS Resource Manager", layout="wide")

# 앱 제목
st.title('AKS Resource Manager')

# 사용 가능한 모든 kube context 가져오기
def get_kube_contexts():
    try:
        process = subprocess.run("kubectl config get-contexts -o name", shell=True, check=True, stdout=subprocess.PIPE, universal_newlines=True)
        contexts = process.stdout.strip().split('\n')
        return contexts
    except subprocess.CalledProcessError as e:
        st.error(f"Error getting kube contexts: {str(e)}")
        return []

kube_contexts = get_kube_contexts()
selected_context = st.sidebar.selectbox("Select kube context", kube_contexts)

# 리소스 유형 옵션 정의
option_data = [
    {'icon': "bi bi-server", 'label': "Nodes"},
    {'icon': "bi bi-diagram-3", 'label': "Pods"},
    {'icon': "bi bi-hdd-network", 'label': "Services"},
    {'icon': "bi bi-stack", 'label': "Deployments"},
    {'icon': "bi bi-shield-lock", 'label': "Secrets"},
    {'icon': "bi bi-hdd-rack", 'label': "LoadBalancers"},
    {'icon': "bi bi-door-open", 'label': "Ingress"},
    {'icon': "bi bi-file-earmark-text", 'label': "ConfigMaps"},
    {'icon': "bi bi-diagram-2", 'label': "Namespaces"},
    {'icon': "bi bi-person-badge", 'label': "ServiceAccounts"},
    {'icon': "bi bi-boxes", 'label': "StorageClasses"},
    {'icon': "bi bi-hdd-stack", 'label': "PersistentVolumes"},
    {'icon': "bi bi-hdd-stack-fill", 'label': "PersistentVolumeClaims"},
]

# 스타일 오버라이드 설정
over_theme = {'txc_inactive': 'white', 'menu_background': 'purple', 'txc_active': 'yellow', 'option_active': 'blue'}

# 옵션 바 표시 및 선택된 옵션 처리
selected_option = hc.option_bar(option_definition=option_data, title='Select Kubernetes Resource', key='ResourceOption', override_theme=over_theme, horizontal_orientation=True)

# kubectl 명령어 실행 및 출력 파싱
def get_kubectl_output(command):
    try:
        output = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        lines = output.stdout.strip().split('\n')
        if len(lines) > 1:
            headers = lines[0].split()
            headers = [header if headers.count(header) == 1 else f"{header}_{idx+1}" for idx, header in enumerate(headers)]
            data = [re.split(r'\s+', line.strip(), maxsplit=len(headers)-1) for line in lines[1:] if line]
            return pd.DataFrame(data, columns=headers)
        return pd.DataFrame()
    except subprocess.CalledProcessError as e:
        st.error(f"Error executing command: {e}")
        return pd.DataFrame()

# 선택된 리소스 유형에 대한 정보 표시

if selected_option:
    resource_label = selected_option  # 수정된 부분
    st.write(f"Selected Kubernetes resource: {resource_label}")

    # Load Balancers 리소스 유형을 위한 특별한 처리
    if resource_label == 'LoadBalancers':
        command = f"kubectl get svc -o wide --all-namespaces --context={selected_context} | grep LoadBalancer"
    else:
        command = f"kubectl get {resource_label.lower()} -o wide --all-namespaces --context={selected_context}"

    df_output = get_kubectl_output(command)
    if not df_output.empty:
        st.dataframe(df_output)
    else:
        st.write("No data available.")
