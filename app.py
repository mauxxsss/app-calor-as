import streamlit as st
import pandas as pd

# Configuración de la página de Streamlit
st.set_page_config(
    page_title="Interactive Calorie Tracker",
    page_icon="🥗",
    layout="wide"
)

# Estilo CSS personalizado para darle un toque moderno y estético
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

# Título principal de la aplicación
st.title("🥗 Dynamic Calorie & Nutrition Tracker")
st.markdown("Personaliza tu rango diario de calorías, registra tus comidas en tiempo real y mantén el control total de tus objetivos nutricionales.")

# Inicializar el estado de sesión (Session State) para persistir datos mientras interactúas
if 'meals' not in st.session_state:
    st.session_state.meals = []

if 'target_calories' not in st.session_state:
    st.session_state.target_calories = 2000

# --- SECCIÓN LATERAL: CONFIGURACIÓN Y ENTRADA DE DATOS ---
with st.sidebar:
    st.header("⚙️ Configuración")
    
    # Objetivo Calórico
    st.session_state.target_calories = st.number_input(
        "Calorías Diarias Objetivo (kcal)",
        min_value=500,
        max_value=6000,
        value=st.session_state.target_calories,
        step=50
    )
    
    st.markdown("---")
    st.subheader("🍽️ Registrar Alimento")
    
    with st.form("meal_form", clear_on_submit=True):
        meal_name = st.text_input("Descripción / Comida", placeholder="Ej. Desayuno, Ensalada...")
        meal_calories = st.number_input("Calorías (kcal)", min_value=0, max_value=3000, value=0, step=10)
        submitted = st.form_submit_button("Añadir al Registro")
        
        if submitted:
            if meal_name.strip() == "":
                meal_name = "Comida sin nombre"
            st.session_state.meals.append({"Comida": meal_name, "Calorías": meal_calories})
            st.success(f"¡Registrado: {meal_name}!")

# --- SECCIÓN PRINCIPAL: DASHBOARD ---
# Cálculo de estadísticas actuales
consumed_calories = sum(item["Calorías"] for item in st.session_state.meals)
remaining_calories = st.session_state.target_calories - consumed_calories
progress_percentage = min(float(consumed_calories / st.session_state.target_calories), 1.0) if st.session_state.target_calories > 0 else 0.0

# Fila de métricas principales
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="🎯 Objetivo Diario", value=f"{st.session_state.target_calories} kcal")

with col2:
    st.metric(label="🔥 Calorías Consumidas", value=f"{consumed_calories} kcal")

with col3:
    delta_color = "normal" if remaining_calories >= 0 else "inverse"
    st.metric(
        label="⚡ Calorías Restantes", 
        value=f"{remaining_calories} kcal",
        delta=f"{-consumed_calories} kcal de consumo"
    )

# Barra de progreso visual
st.markdown("### 📊 Progreso del Día")
st.progress(progress_percentage)

if consumed_calories > st.session_state.target_calories:
    st.warning("⚠️ ¡Has superado tu meta calórica diaria recomendada!")

st.markdown("---")

# Tabla de alimentos consumidos y botón para eliminar elementos
st.subheader("📋 Registro de Comidas de Hoy")

if len(st.session_state.meals) == 0:
    st.info("No hay registros de comida añadidos todavía. ¡Usa el panel lateral para empezar a registrar!")
else:
    # Convertir a DataFrame para mostrarlo ordenado
    df_meals = pd.DataFrame(st.session_state.meals)
    
    # Mostrar tabla interactiva con opción de borrar filas
    col_table, col_actions = st.columns([3, 1])
    
    with col_table:
        st.dataframe(df_meals, use_container_width=True)
        
    with col_actions:
        st.markdown("#### Acciones")
        index_to_delete = st.number_input("Índice a eliminar", min_value=0, max_value=max(0, len(st.session_state.meals)-1), step=1, label_visibility="collapsed")
        if st.button("🗑️ Eliminar Fila"):
            if len(st.session_state.meals) > 0:
                removed = st.session_state.meals.pop(index_to_delete)
                st.rerun()

    if st.button("🧹 Limpiar Todo el Registro"):
        st.session_state.meals = []
        st.rerun()
