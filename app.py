import streamlit as st
import pandas as pd
import re
from PIL import Image

# 1. Configuração da Página
st.set_page_config(page_title="Consulta Pé-de-Meia - Constantino", page_icon="🎓")

# --- ESTILO CSS PARA MENSAGENS E RODAPÉ ---
st.markdown("""
    <style>
    .caixa-sucesso {
        padding: 30px; background-color: #d4edda; color: #155724;
        border-radius: 15px; border: 2px solid #c3e6cb;
        text-align: center; font-size: 22px; font-weight: bold;
    }
    .caixa-erro {
        padding: 30px; background-color: #f8d7da; color: #721c24;
        border-radius: 15px; border: 2px solid #f5c6cb;
        text-align: center; font-size: 22px; font-weight: bold;
    }
    .destaque-tel { font-size: 26px; color: #b22222; display: block; margin-top: 10px; }
    
    /* Estilo para o Rodapé */
    .rodape {
        text-align: center;
        color: #666;
        font-style: italic;
        margin-top: 50px;
        padding: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Exibição da Logo
try:
    img_logo = Image.open("logo.png")
    st.image(img_logo, width=250)
except:
    try:
        img_logo = Image.open("logo.jpg")
        st.image(img_logo, width=250)
    except:
        st.warning("⚠️ Logo não encontrada.")

st.title("🎓 Portal de Consulta - Pé-de-Meia")
st.subheader("Escola Padre Constantino de Monte")

# 3. Carregamento dos Dados (Google Sheets)
@st.cache_data(ttl=600)
def carregar_dados():
    try:
        ID_PLANILHA = "136yN8S4R3RTeAaErRE-trzS6fmmz0o3s"
        url = f"https://docs.google.com/spreadsheets/d/{ID_PLANILHA}/export?format=xlsx"
        return pd.read_excel(url)
    except Exception as e:
        st.error(f"Erro ao conectar com a planilha: {e}")
        return None

df = carregar_dados()

if df is not None:
    col_nome, col_cpf, col_nasc, col_situacao, col_desc = "nome", "CPF", "data de nascimento", "Situação", "Descrição"

    with st.form("form_consulta"):
        st.write("Digite os dados do estudante:")
        cpf_digitado = st.text_input("CPF (somente números):")
        nasc_digitada = st.text_input("Data de Nascimento (ex: 30/04/2010):")
        btn = st.form_submit_button("CONSULTAR AGORA")

    if btn:
        if cpf_digitado and nasc_digitada:
            cpf_limpo = re.sub(r'\D', '', cpf_digitado).zfill(11)
            nasc_limpa = nasc_digitada.strip()

            cpfs_planilha = df[col_cpf].astype(str).str.replace(r'\D', '', regex=True).str.zfill(11)
            datas_planilha = pd.to_datetime(df[col_nasc], errors='coerce').dt.strftime('%d/%m/%Y')

            resultado = df[(cpfs_planilha == cpf_limpo) & (datas_planilha == nasc_limpa)]

            if not resultado.empty:
                aluno = resultado.iloc[0]
                status = str(aluno[col_situacao]).upper()
                
                st.markdown(f"### Estudante: **{aluno[col_nome]}**")
                st.write("---")

                if "NÃO" not in status:
                    st.markdown(f"""<div class="caixa-sucesso">✅ TUDO CERTO PARA RECEBER O BENEFÍCIO!<br><br>
                                    Procure a Caixa Econômica Federal para mais detalhes.</div>""", unsafe_allow_html=True)
                else:
                    st.markdown(f"""<div class="caixa-erro">⚠️ ESTUDANTE NÃO ELEGÍVEL<br><br>
                                    MOTIVO: {aluno[col_desc]}<br><br>
                                    Procurar a Secretaria ou Direção da Escola no WhatsApp:<br>
                                    <span class="destaque-tel">(67) 3454-1045</span></div>""", unsafe_allow_html=True)
            else:
                st.error("❌ Estudante não localizado. Verifique se digitou corretamente.")

# --- RODAPÉ FINAL (Sempre visível) ---
st.markdown("---")
st.markdown('<div class="rodape">Feito com carinho pela Equipe Padre Constantino ❤️</div>', unsafe_allow_html=True)
