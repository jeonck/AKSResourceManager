import streamlit as st
import subprocess
import pandas as pd
import re  # 정규 표현식 모듈 추가

# pandas에서 최대 표시 행 수를 30으로 설정
pd.options.display.max_rows = 60

# Streamlit 앱의 페이지 설정
st.set_page_config(layout="wide")

# 사용 가능한 모든 kube context 가져오기
def get_kube_contexts():
    try:
        output = subprocess.run("kubectl config get-contexts -o name", shell=True, check=True, stdout=subprocess.PIPE, universal_newlines=True)
        contexts = output.stdout.strip().split('\n')
        return contexts
    except subprocess.CalledProcessError as e:
        st.error(f"Error getting kube contexts: {e}")
        return []

kube_contexts = get_kube_contexts()

# 사이드바에서 kube context 선택
selected_context = st.sidebar.selectbox(
    "Select kube context",
    kube_contexts
)

# 앱 제목에 선택된 kube context 표시
st.title(f'AKS Resource Manager - {selected_context}')

# 리소스 탭 생성
resource_types = ("Namespaces","Nodes", "Pods", "Services", "Deployments", "Secrets", 
                  "StorageClasses","PersistentVolumes", "PersistentVolumeClaims","HPA",
                  "Ingress", "ConfigMaps",  "ServiceAccounts", "LoadBalancers",
                  "Roles", "ClusterRoles", "RoleBindings", "ClusterRoleBindings",
                   "ResourceQuotas", "LimitRanges", 
                  )

tabs = st.tabs(resource_types)

# kubectl 명령어 실행 및 출력 파싱
def get_kubectl_output(command, resource_type):
    command_with_context = f"{command} --context {selected_context}"
    try:
        if resource_type == "LoadBalancers":
            kubectl_proc = subprocess.Popen(command_with_context, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
            grep_proc = subprocess.Popen(["grep", "LoadBalancer"], stdin=kubectl_proc.stdout, stdout=subprocess.PIPE, universal_newlines=True)
            kubectl_proc.stdout.close()
            output, errors = grep_proc.communicate()
            lines = output.strip().split('\n')
        else:
            output = subprocess.run(command_with_context, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
            lines = output.stdout.strip().split('\n')

        if len(lines) > 1:
            headers = lines[0].split()
            headers = [header if headers.count(header) == 1 else f"{header}_{idx+1}" for idx, header in enumerate(headers)]
            data = []
            for line in lines[1:]:
                row_data = re.split(r'\s+', line.strip(), maxsplit=len(headers)-1)
                while len(row_data) < len(headers):
                    row_data.append(None)
                data.append(row_data)
            return pd.DataFrame(data, columns=headers)
        return pd.DataFrame()
    except subprocess.CalledProcessError as e:
        st.error(f"Error executing command: {e}")
        return pd.DataFrame()

# 리소스 유형에 따른 kubectl 명령어 및 출력
resource_commands = {
    "Nodes": "kubectl get nodes -o wide",
    "Pods": "kubectl get pods -o wide --all-namespaces",
    "Services": "kubectl get svc -o wide --all-namespaces",
    "Deployments": "kubectl get deployments -o wide --all-namespaces",
    "Secrets": "kubectl get secrets -o wide --all-namespaces",
    "LoadBalancers": "kubectl get svc -o wide --all-namespaces",
    "Ingress": "kubectl get ingress -o wide --all-namespaces",
    "ConfigMaps": "kubectl get configmaps -o wide --all-namespaces",
    "Namespaces": "kubectl get namespaces",
    "ServiceAccounts": "kubectl get serviceaccounts -o wide --all-namespaces",
    "StorageClasses": "kubectl get storageclass",
    "HPA": "kubectl get hpa -o wide --all-namespaces",
    "ResourceQuotas": "kubectl get quota -o wide --all-namespaces",
    "LimitRanges": "kubectl get limitranges -o wide --all-namespaces",
    "PersistentVolumes": "kubectl get pv -o wide",
    "PersistentVolumeClaims": "kubectl get pvc -o wide --all-namespaces",
    "Roles": "kubectl get roles -o wide --all-namespaces",
    "ClusterRoles": "kubectl get clusterroles -o wide",
    "RoleBindings": "kubectl get rolebindings -o wide --all-namespaces",
    "ClusterRoleBindings": "kubectl get clusterrolebindings -o wide"
}


for tab, resource_type in zip(tabs, resource_types):
    with tab:
        command = resource_commands.get(resource_type)
        if command:
            df_output = get_kubectl_output(command, resource_type)

            if not df_output.empty:
                # 데이터프레임에 스타일 적용: 셀 테두리를 흰색으로 설정
                styled_df = df_output.style.map(lambda x: "color: white; background-color: black")\
                                           .set_table_styles([{
                                               'selector': 'td, th',
                                               'props': [('border', '1px solid white')]
                                           }], overwrite=False)

                # 스타일이 적용된 데이터프레임을 HTML로 변환
                html_df = styled_df.to_html(escape=False)

                # 스타일이 적용된 HTML 데이터프레임을 Streamlit 앱에 표시
                st.markdown(html_df, unsafe_allow_html=True)
            else:
                st.write("No data available.")

