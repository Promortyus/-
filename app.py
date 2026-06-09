import streamlit as st
import math

def calculate_bearing_capacity(d, H2, H1, gamma2, phi2, c, gamma1, phi1, SCI, GSI, mi, D, gamma_c):
    rad = math.pi / 180
    
    # 角度转弧度等参数
    alpha2 = 90 - phi2 / 3
    alpha1 = 45 - phi1 / 3
    mb = mi * math.exp((GSI - 100) / (28 - 14 * D))
    s = math.exp((GSI - 100) / (9 - 3 * D))
    
    # F7: 岩体抗拉强度 (sigma_t)
    sigma_t = (SCI / 2) * (mb - math.sqrt(mb**2 + 4 * s)) * 1000
    
    # F8: 几何参数 C1
    C1 = H1 / math.tan(alpha1 * rad) + d / 2
    
    # F9: 几何参数 C2
    C2 = H1 / math.tan(alpha1 * rad) + H2 / math.tan(alpha2 * rad) + d / 2
    
    # F10: 几何参数 C0
    C0 = C1**2 + C2**2 + C1 * C2
    
    # F12: 土层抗拔力 (R_soil)
    term1 = -0.55 * c
    term2 = (gamma2 * math.pi * math.sin((2 * alpha2 + 2 * phi2) * rad) * math.cos(phi2 * rad))
    term3 = (C2**3 + 2 * C1**3 - 3 * C1**2 * C2) / (6 * math.cos(alpha2 * rad)**2)
    R_soil = term1 * term2 * term3
    
    # F13: 岩层抗拔力 (R_rock)
    R_rock = math.pi * H1 * (1 / math.sin(alpha1 * rad)) * (H1 / math.tan(alpha1 * rad) + d) * abs(sigma_t)
    
    # F14: 土岩锥体自重 (W_cone)
    part_soil = (gamma2 * math.pi * H2 / 3) * C0 - gamma2 * math.pi * (d / 2)**2 * H2
    part_rock = (gamma1 * math.pi * H1 / 3) * ((d / 2)**2 + C1**2 + (d / 2) * C1) - gamma1 * math.pi * (d / 2)**2 * H1
    W_cone = part_soil + part_rock
    
    # F15: 桩身自重 (W_pile)
    W_pile = gamma_c * math.pi * (d / 2)**2 * (H2 + H1 + 0.5)
    
    # F17: 修正因子 Alpha1
    Alpha1 = math.sqrt(1.472 - 0.805 / (1 + (H1 / d)**3.36))
    
    # F18: 修正因子 Alpha2
    Alpha2 = math.sqrt(0.253 + 0.885 / (1 + (H2 / d)**3.36))
    
    # F19: 修正因子 Alpha3
    Alpha3 = d / (H1 + d)
    
    # F20: 综合修正系数 (Beta)
    Beta = Alpha3 * Alpha2
    
    # F21: 最终极限承载力
    ultimate_capacity = (abs(R_soil) + W_cone) * Beta + W_pile + abs(R_rock) * Alpha1
    
    return {
        "R_soil": R_soil,
        "R_rock": R_rock,
        "W_cone": W_cone,
        "W_pile": W_pile,
        "Alpha1": Alpha1,
        "Beta": Beta,
        "ultimate_capacity": ultimate_capacity
    }

st.set_page_config(page_title="嵌岩抗拔桩承载力计算 App", layout="centered")

st.title("嵌岩抗拔桩承载力计算 App")
st.markdown("该在线工具基于Excel文档的逻辑开发，用于计算**最终极限承载力**。")

col1, col2 = st.columns(2)

with col1:
    st.subheader("基本参数")
    d = st.number_input("桩径 (d) [m]", value=1.0, step=0.1)
    H2 = st.number_input("土层厚度 (H2) [m]", value=3.0, step=0.1)
    H1 = st.number_input("嵌岩深度 (H1) [m]", value=3.0, step=0.1)
    
    st.subheader("土层参数")
    gamma2 = st.number_input("土的重度 (gamma2) [kN/m³]", value=17.0, step=1.0)
    phi2 = st.number_input("土的内摩擦角 (phi2) [°]", value=10.0, step=1.0)
    c = st.number_input("土的粘聚力 (c) [kPa]", value=25.0, step=1.0)

with col2:
    st.subheader("岩石参数")
    gamma1 = st.number_input("岩石重度 (gamma1) [kN/m³]", value=23.0, step=1.0)
    phi1 = st.number_input("岩石内摩擦角 (phi1) [°]", value=35.0, step=1.0)
    SCI = st.number_input("单轴抗压强度 (SCI) [MPa]", value=40.0, step=1.0)
    GSI = st.number_input("岩体地质强度指标 (GSI)", value=30.0, step=1.0)
    mi = st.number_input("岩石常数 (mi)", value=20.0, step=1.0)
    D = st.number_input("扰动因子 (D)", value=0.0, step=0.1)
    
    st.subheader("材料参数")
    gamma_c = st.number_input("桩身混凝土重度 (gamma_c) [kN/m³]", value=25.0, step=1.0)

st.markdown("---")

if st.button("计算最终极限承载力", use_container_width=True, type="primary"):
    res = calculate_bearing_capacity(d, H2, H1, gamma2, phi2, c, gamma1, phi1, SCI, GSI, mi, D, gamma_c)
    
    st.success(f"### 最终极限承载力: {res['ultimate_capacity']:.2f} kN")
    
    with st.expander("查看计算中间变量细节"):
        st.write(f"**土层抗拔力 (R_soil)**: {res['R_soil']:.2f} kN")
        st.write(f"**岩层抗拔力 (R_rock)**: {res['R_rock']:.2f} kN")
        st.write(f"**土岩锥体自重 (W_cone)**: {res['W_cone']:.2f} kN")
        st.write(f"**桩身自重 (W_pile)**: {res['W_pile']:.2f} kN")
        st.write(f"**修正因子 Alpha1**: {res['Alpha1']:.4f}")
        st.write(f"**综合修正系数 (Beta)**: {res['Beta']:.4f}")
