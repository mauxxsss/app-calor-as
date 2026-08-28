import streamlit as st
import pandas as pd

# Configuración de la página de Streamlit
st.set_page_config(
    page_title="Control de Calorías Diario",
    page_icon="🥗",
    layout="wide"
)

# Estilo CSS personalizado
st.markdown("""
    <style>
    .main {
        background-color: #f8fafc;
    }
    .stMetric {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        border: 1px solid #e2e8f0;
    }
    </style>
""", unsafe_allow_html=True)

# Título principal de la aplicación en español
st.title("🥗 Control de Calorías Diario")
st.markdown("Establece tu objetivo diario de calorías, registra tus comidas y mantén el control total.")

# Inicializar el estado de sesión
if 'meals' not in st.session_state:
    st.session_state.meals = []

if 'target_calories' not in st.session_state:
    st.session_state.target_calories = 0

# --- SECCIÓN LATERAL: CONFIGURACIÓN Y ENTRADA DE DATOS ---
with st.sidebar:
    st.header("⚙️ Configuración")
    
    # Objetivo Calórico que empieza en 0 para que el usuario lo escriba
    st.session_state.target_calories = st.number_input(
        "Calorías Diarias Objetivo (kcal)",
        min_value=0,
        max_value=10000,
        value=st.session_state.target_calories,
        step=50
    )
    
    st.markdown("---")
    st.subheader("🍽️ Registrar Alimento")
    
    with st.form("meal_form", clear_on_submit=True):
        meal_name = st.text_input("Nombre de la comida", placeholder="Ej. Desayuno, Arroz con pollo...")
        meal_calories = st.number_input("Calorías (kcal)", min_value=0, max_value=3000, value=0, step=10)
        submitted = st.form_submit_button("Añadir al Registro")
        
        if submitted:
            if meal_name.strip() == "":
                meal_name = "Comida"
            st.session_state.meals.append({"Comida": meal_name, "Calorías": meal_calories})
            st.success(f"¡Registrado: {meal_name}!")

# --- SECCIÓN PRINCIPAL: DASHBOARD ---
consumed_calories = sum(item["Calorías"] for item in st.session_state.meals)
remaining_calories = st.session_state.target_calories - consumed_calories

# Evitar división por cero en la barra de progreso si el objetivo es 0
if st.session_state.target_calories > 0:
    progress_percentage = min(float(consumed_calories / st.session_state.target_calories), 1.0)
else:
    progress_percentage = 0.0

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="🎯 Objetivo Diario", value=f"{st.session_state.target_calories} kcal")

with col2:
    st.metric(label="🔥 Calorías Consumidas", value=f"{consumed_calories} kcal")

with col3:
    if st.session_state.target_calories > 0:
        st.metric(
            label="⚡ Calorías Restantes", 
            value=f"{remaining_calories} kcal",
            delta=f"{-consumed_calories} kcal de consumo"
        )
    else:
        st.metric(label="⚡ Calorías Restantes", value="Define un objetivo")

st.markdown("### 📊 Progreso del Día")
st.progress(progress_percentage)

if st.session_state.target_calories > 0 and consumed_calories > st.session_state.target_calories:
    st.warning("⚠️ ¡Has superado tu meta calórica diaria recomendada!")

st.markdown("---")

# Tabla de alimentos consumidos con borrado individual limpio
st.subheader("📋 Registro de Comidas de Hoy")

if len(st.session_state.meals) == 0:
    st.info("No hay registros de comida añadidos todavía. ¡Configura tus calorías e introduce tus comidas en el panel lateral!")
else:
    df_meals = pd.DataFrame(st.session_state.meals)
    st.dataframe(df_meals, use_container_width=True)
    
    st.markdown("#### 🗑️ Eliminar una comida específica")
    
    meal_options = [f"{i+1}. {item['Comida']} ({item['Calorías']} kcal)" for i, item in enumerate(st.session_state.meals)]
    selected_to_delete = st.selectbox("Selecciona cuál quieres borrar:", meal_options, label_visibility="collapsed")
    
    col_del1, col_del2 = st.columns([1, 4])
    with col_del1:
        if st.button("Eliminar seleccionada"):
            index_to_remove = meal_options.index(selected_to_delete)
            st.session_state.meals.pop(index_to_remove)
            st.rerun()
            
    with col_del2:
        if st.button("🧹 Borrar todo el registro"):
            st.session_state.meals = []
            st.rerun()
