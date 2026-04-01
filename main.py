import streamlit as st

st.set_page_config(page_title="Credit Card Transactions Dataset Analysis", layout="wide")

st.markdown("""
    <style>
    /* Configura a posição do conteúdo no fundo da sidebar */
    .sidebar-footer {
        position: absolute;
        bottom: -700px; /* Ajuste conforme necessário */
        width: 100%;
        text-align: center;
        font-size: 0.85rem;
        color: gray;
    }
    </style>
""", unsafe_allow_html=True)

st.sidebar.markdown('<div class = "sidebar-footer">Feito por Guilherme Pasqualette </div>', unsafe_allow_html=True)

pages = [
    st.Page('client.py', title='Client Analysis', icon=':material/person:'),
    st.Page('merch.py', title='Merchant Analysis', icon=':material/storefront:'),
    st.Page('fraud.py', title='Fraud x Non-fraud Analysis', icon=':material/policy_alert:')
]

pg = st.navigation(pages)
pg.run()

