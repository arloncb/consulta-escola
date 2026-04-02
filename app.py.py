import streamlit as st
import pandas as pd
import re
from PIL import Image

# 1. Configuração da Página
st.set_page_config(page_title="Consulta Pé-de-Meia - Constantino", page_icon="🎓")

# --- ESTILO CSS PARA MENSAGENS GRANDES E COLORIDAS ---
st.markdown("""
    <style>
    .caixa-sucesso {
        padding: 30px;
        background-color: #d4edda;
        color: #155724;
        border-radius: 15px;
        border: 2px solid #c3e6cb;
        text-align: center;
        font-size: 22px;
        font-weight: bold;
    }
    .caixa-erro {
        padding: 30px;
        background-color: #f8d7da;
        color: #721c24;
        border-radius: 15px;
        border: 2px solid #f5c6cb;
        text-align: center;
        font-size: 22px;
        font-weight: bold;
    }
    .destaque-tel {
        font-size: 26px;
        color: #b22222;
        display: block;
        margin-top: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Exibição da Logo da Escola
try:
    # Tenta abrir a logo (supondo que seja .png ou .jpg)
    try:
        img_logo = Image.open("logo.png")
    except:
        img_logo = Image.open("logo.jpg")
        
    st.image(img_logo, width=250)
except:
    st.warning("⚠️ Logo não encontrada. Verifique se o nome do arquivo é 'logo.png' ou 'logo.jpg' na sua pasta.")

st.title("🎓 Portal de Consulta - Pé-de-Meia")
st.subheader("Escola Padre Constantino de Monte")

# 3. Carregamento dos Dados
@st.cache_data
def carregar_dados():
    try:
        return pd.read_excel("dados.xlsx")
    except Exception as e:
        st.error(f"Erro ao ler 'dados.xlsx': {e}")
        return None

df = carregar_dados()

if df is not None:
    # Mapeamento das colunas conforme você informou
    col_nome = "nome"
    col_cpf = "CPF"
    col_nasc = "data de nascimento"
    col_situacao = "Situação"
    col_desc = "Descrição"

    # Formulário de Consulta
    with st.form("form_consulta"):
        st.write("Digite os dados do estudante:")
        cpf_digitado = st.text_input("CPF (somente números):")
        nasc_digitada = st.text_input("Data de Nascimento (ex: 30/04/2010):")
        btn = st.form_submit_button("CONSULTAR AGORA")

    if btn:
        if cpf_digitado and nasc_digitada:
            # Limpeza para comparação
            cpf_limpo = re.sub(r'\D', '', cpf_digitado).zfill(11)
            nasc_limpa = nasc_digitada.strip()

            # Prepara a planilha para comparação
            cpfs_planilha = df[col_cpf].astype(str).str.replace(r'\D', '', regex=True).str.zfill(11)
            datas_planilha = pd.to_datetime(df[col_nasc], errors='coerce').dt.strftime('%d/%m/%Y')

            # Busca
            resultado = df[(cpfs_planilha == cpf_limpo) & (datas_planilha == nasc_limpa)]

            if not resultado.empty:
                aluno = resultado.iloc[0]
                status = str(aluno[col_situacao]).upper()
                
                st.markdown(f"### Estudante: **{aluno[col_nome]}**")
                st.write("---")

                # LÓGICA DE MENSAGENS PERSONALIZADAS
                # Verifica se é Elegível (se não tiver a palavra 'NÃO' no status)
                if "NÃO" not in status:
                    st.markdown(f"""
                        <div class="caixa-sucesso">
                            ✅ TUDO CERTO PARA RECEBER O BENEFÍCIO!<br><br>
                            Procure a Caixa Econômica Federal para mais detalhes.
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    # Mensagem para NÃO Elegível (Destaque Maior)
                    st.markdown(f"""
                        <div class="caixa-erro">
                            ⚠️ ESTUDANTE NÃO ELEGÍVEL<br><br>
                            MOTIVO: {aluno[col_desc]}<br><br>
                            Procurar a Secretaria ou Direção da Escola para mais detalhes no WhatsApp:<br>
                            <span class="destaque-tel">(67) 3454-1045</span>
                        </div>
                    """, unsafe_allow_html=True)
            else:
                st.error("❌ Estudante não localizado. Verifique os dados digitados.")
        else:
            st.warning("Preencha todos os campos para consultar.")