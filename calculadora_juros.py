import streamlit as st
import pandas as pd

st.set_page_config(page_title="Calculadora de Juros Compostos", page_icon="💰", layout="centered")

st.title("💰 Calculadora de Juros Compostos")
st.write("Simule o crescimento do seu património e descubra o poder dos juros compostos!")

col1, col2 = st.columns(2)

with col1:
    valor_inicial = st.number_input("Investimento Inicial (R$)", min_value=0.0, value=1000.0, step=100.0)
    aporte_mensal = st.number_input("Aporte Mensal (R$)", min_value=0.0, value=200.0, step=50.0)

with col2:
    taxa_anual = st.number_input("Taxa de Juros Anual (%)", min_value=0.0, value=10.0, step=0.5)
    anos = st.slider("Período (Anos)", min_value=1, max_value=40, value=10)

# Cálculos
meses = anos * 12
taxa_mensal = (1 + taxa_anual / 100) ** (1 / 12) - 1

dados = []
saldo = valor_inicial
total_investido = valor_inicial

for m in range(1, meses + 1):
    juros_mes = saldo * taxa_mensal
    saldo += juros_mes + aporte_mensal
    total_investido += aporte_mensal
    
    if m % 12 == 0:
        dados.append({
            "Ano": m // 12,
            "Total Investido": round(total_investido, 2),
            "Total Juros": round(saldo - total_investido, 2),
            "Património Total": round(saldo, 2)
        })

df = pd.DataFrame(dados)

st.subheader("📊 Resultado da Simulação")
st.metric("Património Final", f"R$ {saldo:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

col_res1, col_res2 = st.columns(2)
col_res1.metric("Total Investido", f"R$ {total_investido:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
col_res2.metric("Total em Juros Ganho", f"R$ {saldo - total_investido:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

st.line_chart(df.set_index("Ano")[["Total Investido", "Património Total"]])

st.markdown("---")
st.subheader("📚 Recomendações para Investidores")
st.write("Aprenda a investir melhor com os livros recomendados:")
st.markdown("- [ O Homem Mais Rico da Babilónia ](https://amazon.com.br) - Essencial para iniciantes.")
st.markdown("- [ Os Segredos da Mente Milionária ](https://amazon.com.br) - Mude a sua mentalidade financeira.")