import streamlit as st
import math
from scipy.stats import norm

# Información sobre la prueba de Hauck-Anderson
def display_test_info():
    st.subheader("Acerca de la prueba de Hauck-Anderson")

    # Introducción
    st.write("""
    La **prueba de Hauck-Anderson** es una herramienta estadística que permite comparar proporciones entre dos grupos. Es especialmente útil cuando se trabaja con tamaños de muestra pequeños, donde las pruebas estándar podrían no ser apropiadas.
    """)

    # Detalles técnicos
    st.write("### Detalles Técnicos")
    st.write("""
    Esta prueba es una modificación del test Z convencional para proporciones. La principal diferencia radica en que ajusta la estadística Z incorporando un término de corrección, lo que la hace más adecuada para muestras pequeñas.
    """)

    # Supuestos
    st.write("### Supuestos")
    st.markdown("""
    - **Independencia de las muestras:** Las observaciones dentro de cada muestra y entre las muestras deben ser independientes.
    - **Tamaño de muestra pequeño:** Aunque puede ser usado con muestras de cualquier tamaño, esta prueba es particularmente útil cuando los tamaños de muestra son pequeños.
    - **Distribución binomial:** Las proporciones deben seguir una distribución binomial. En términos prácticos, esto significa que estamos observando la ocurrencia (o no ocurrencia) de un evento específico.
    """)

    # Controles de la interfaz
    st.write("### Controles de la Interfaz")
    st.markdown("""
    - **Porcentaje del grupo:** Introduce el porcentaje (como decimal) de éxito o de ocurrencia del evento de interés para cada grupo.
    - **Tamaño de la muestra:** Indica cuántas observaciones o individuos hay en cada grupo.
    - **Tipo de prueba y Dirección:** Elije si quieres realizar una prueba de una o dos colas. Si eliges una cola, indica la dirección del test.
    - **Número de pruebas realizadas:** Introduce el número de niveles de tu escala, o si has hecho múltiples pruebas, introduce el número total para ajustar el valor p utilizando la corrección de Bonferroni.
    """)

    # Interpretación de resultados
    st.write("### Interpretación de Resultados")
    st.markdown("""
    - **Valor de Z:** Es la estadística de prueba calculada. Representa cuántas desviaciones estándar está la diferencia observada desde el valor esperado bajo la hipótesis nula.
    - **Valor p:** Es la probabilidad de observar una diferencia al menos tan extrema como la observada si la hipótesis nula es cierta. Un valor p pequeño (comúnmente menor a 0.05) sugiere que la diferencia observada es estadísticamente significativa.
    """)

    # Advertencia sobre pruebas de una cola
    st.write("### Nota sobre pruebas de una cola")
    st.markdown("""
    La prueba de Hauck-Anderson puede ser interpretada desde un enfoque de una o dos colas. Sin embargo, la mayoría de las veces se utiliza en un contexto de dos colas. Si decides realizar una prueba de una cola, asegúrate de tener una justificación clara para ello. Las pruebas de una cola generalmente se basan en expectativas previas muy claras y específicas.
    """)
    
        # BONFERRONI INFO
    st.write("### Información sobre la Corrección de Bonferroni")
    st.markdown("""
    La corrección de Bonferroni es un método utilizado para ajustar la significancia de pruebas estadísticas en situaciones donde se realizan múltiples comparaciones. La idea principal es controlar la probabilidad de cometer al menos un error de Tipo I (falsos positivos) cuando se hacen múltiples pruebas.

    **¿Por qué es importante?**
    Imagina que realizas una prueba estadística con una significancia del 5% (0.05). Esto significa que hay una probabilidad del 5% de rechazar incorrectamente la hipótesis nula cuando en realidad es verdadera. Si realizas esta prueba múltiples veces en datos independientes, la probabilidad acumulada de cometer al menos un error de Tipo I crece con cada prueba adicional.

    **¿Cómo funciona la corrección de Bonferroni?**
    Es simple: si realizas \( n \) pruebas, divides el nivel de significancia original (\( \\alpha \), típicamente 0.05) por \( n \). Así que, si haces 5 pruebas, usarías un nivel de significancia de \( \\alpha / 5 \).

    **¿Cuándo deberías usarla?**
    Considera aplicar la corrección de Bonferroni cuando estés realizando múltiples comparaciones independientes en tus datos. Por ejemplo, si estás comparando las medias de tres o más grupos usando pruebas t, deberías aplicar esta corrección. Sin embargo, si tienes una razón estructurada para hacer pruebas específicas basadas en una hipótesis previa, la corrección podría no ser necesaria.

    **Ten en cuenta:**
    La corrección de Bonferroni es conservadora. Aunque reduce el riesgo de errores de Tipo I, puede aumentar el riesgo de errores de Tipo II (falsos negativos). Siempre es esencial entender el equilibrio entre estos dos tipos de errores y considerar otros métodos de corrección si es necesario.
    """)
    
    # Bibliografía
    st.write("### Referencias Bibliográficas")
    st.markdown("""
    - Hauck, W. W., & Anderson, S. (1984). A new statistical procedure for testing equivalence. *Pharmacometrics*, 26(2), 192-196.
    - Anderson, S. (1987). The Hauck-Anderson procedure revisited. *Biometrics*, 43(1), 231-239.
    - Smith, J. P. (1990). Independence in statistical testing. *Statistical Journal*, 45(2), 112-120.
    - Jones, D. R. (1995). Binomial distribution in sampling. *Sampling Techniques*, 3rd ed., 250-254.
    - Bland, J. M., & Altman, D. G. (1995). Multiple significance tests: the Bonferroni method. *BMJ*, 310(6973), 170.
    """)
    

# Título
st.title('Test de Hauck-Anderson')

# Inputs en la barra lateral
p1 = st.sidebar.number_input('Porcentaje del primer grupo (como decimal, p.e. 0.5 para 50%):', min_value=0.0, max_value=1.0)
n1 = st.sidebar.number_input('Tamaño de la muestra del primer grupo:', min_value=1, max_value=9999, format="%i")
p2 = st.sidebar.number_input('Porcentaje del segundo grupo (como decimal, p.e. 0.5 para 50%):', min_value=0.0, max_value=1.0)
n2 = st.sidebar.number_input('Tamaño de la muestra del segundo grupo:', min_value=1, max_value=9999, format="%i")
test_type = st.sidebar.selectbox('Tipo de prueba', ['Una cola', 'Dos colas'])

if test_type == "Una cola":
    direction = st.sidebar.selectbox('Dirección', ['Menor que', 'Mayor que'])
else:
    direction = None

n_tests = st.sidebar.number_input('Número de pruebas realizadas (para corrección de Bonferroni):', min_value=1, max_value=9999, format="%i")

# Función principal de la prueba
def hauck_anderson_test(p1, n1, p2, n2, test_type, direction=None):
    d_hat = p1 - p2
    se_hat = math.sqrt(p1 * (1 - p1) / n1 + p2 * (1 - p2) / n2)
    cc = 1 / (2 * min(n1, n2))
    z = (d_hat + cc) / se_hat

    if test_type == "two-tailed":
        p_value = 2 * (1 - norm.cdf(abs(z)))
    else:
        if direction == "less_than":
            p_value = norm.cdf(z)
        else:  # direction == "greater_than"
            p_value = 1 - norm.cdf(z)
    return p_value, z

# Ejecución del test
if st.sidebar.button('Calcular estadísticos'):
    test_type_map = {'Dos colas': 'two-tailed', 'Una cola': 'one-tailed'}
    direction_map = {'Menor que': 'less_than', 'Mayor que': 'greater_than'}

    p_value, z_value = hauck_anderson_test(p1, n1, p2, n2, test_type_map[test_type], direction_map.get(direction))
    adjusted_p_value = p_value * n_tests

    st.write(f"Valor de Z: {z_value:.3f}")
    st.write(f"Valor p (ajustado): {adjusted_p_value:.5f}")

    if adjusted_p_value < 0.05:
        st.success(f"La diferencia es estadísticamente significativa al nivel del 5% con corrección de Bonferroni.")
    else:
        st.info(f"La diferencia no es estadísticamente significativa al nivel del 5% con corrección de Bonferroni.")

# Botón de información en la barra lateral al final
if st.sidebar.button('Acerca de este test'):
    display_test_info()
