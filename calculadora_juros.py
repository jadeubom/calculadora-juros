import streamlit as st

st.set_page_config(page_title="Calculadora de Juros Compostos", page_icon="💰", layout="centered")

st.title("💰 Calculadora de Juros Compostos")
st.write("Simule o crescimento do seu património e descubra o poder dos juros compostos!")

# Entradas do usuário
investimento_inicial = st.number_input("Investimento Inicial (R$)", value=1000.0, step=100.0)
taxa_juros_anual = st.number_input("Taxa de Juros Anual (%)", value=10.0, step=0.5)
aporte_mensal = st.number_input("Aporte Mensal (R$)", value=200.0, step=50.0)
anos = st.slider("Período (Anos)", min_value=1, max_value=40, value=10)

# Cálculo de juros compostos
taxa_mensal = (1 + taxa_juros_anual / 100) ** (1/12) - 1
meses = anos * 12
patrimonio = investimento_inicial
total_investido = investimento_inicial

dados_grafico = []

for mes in range(1, meses + 1):
    patrimonio = (patrimonio + aporte_mensal) * (1 + taxa_mensal)
    total_investido += aporte_mensal
    dados_grafico.append(patrimonio)

total_juros = patrimonio - total_investido

# Exibição dos Resultados
st.subheader("📊 Resultado da Simulação")

col1, col2 = st.columns(2)
with col1:
    st.metric("Patrimônio Final", f"R$ {patrimonio:,.2f}")
    st.metric("Total Investido", f"R$ {total_investido:,.2f}")
with col2:
    st.metric("Total em Juros Ganho", f"R$ {total_juros:,.2f}")

# Gráfico de evolução
st.line_chart(dados_grafico)

# Seção de Afiliados
st.markdown("---")
st.subheader("📚 Recomendações para Investidores")
st.write("Aprenda a investir melhor com os livros recomendados:")
st.markdown("- [ O Homem Mais Rico da Babilónia ](https://link.amazon/B00HPXuD9) - Essencial para iniciantes.")
st.markdown("- [ Os Segredos da Mente Milionária ](https://link.amazon/B04u4t7pb) - Mude a sua mentalidade financeira.")