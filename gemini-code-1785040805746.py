import streamlit as st
import streamlit.components.v1 as components
import math

# Set Page Config
st.set_page_config(
    page_title="Geotextile Wall Designer Pro",
    page_icon="🧱",
    layout="wide"
)

# Custom CSS for UI
st.markdown("""
<style>
    .main {
        background-color: #0f172a;
        color: #f8fafc;
    }
    
    /* Card Design */
    .metric-card {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border: 1px solid #334155;
        border-radius: 14px;
        padding: 16px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        margin-bottom: 12px;
    }
    .metric-title {
        color: #94a3b8;
        font-size: 14px;
        font-weight: 600;
        margin-bottom: 6px;
    }
    .metric-value {
        color: #38bdf8;
        font-size: 26px;
        font-weight: bold;
    }
    
    /* Pass/Fail Badges */
    .status-card {
        background: #1e293b;
        border-radius: 12px;
        padding: 14px;
        text-align: center;
        border: 1px solid #334155;
    }
    .pass-badge {
        background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%);
        color: #ffffff;
        padding: 6px 14px;
        border-radius: 20px;
        font-weight: bold;
        font-size: 14px;
        display: inline-block;
        box-shadow: 0 0 10px rgba(34, 197, 94, 0.4);
    }
    .fail-badge {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        color: #ffffff;
        padding: 6px 14px;
        border-radius: 20px;
        font-weight: bold;
        font-size: 14px;
        display: inline-block;
        box-shadow: 0 0 10px rgba(239, 68, 68, 0.4);
    }

    /* Anime Mascot Cards */
    .anime-card {
        background: linear-gradient(135deg, #ec4899 0%, #8b5cf6 100%);
        color: #ffffff;
        border-radius: 18px;
        padding: 16px;
        display: flex;
        align-items: center;
        gap: 16px;
        margin-top: 20px;
        box-shadow: 0 6px 20px rgba(236, 72, 153, 0.3);
        animation: float 3.5s ease-in-out infinite;
    }
    .mascot-card {
        background: linear-gradient(135deg, #0ea5e9 0%, #6366f1 100%);
        color: #ffffff;
        border-radius: 16px;
        padding: 14px;
        display: flex;
        align-items: center;
        gap: 14px;
        margin-bottom: 16px;
        box-shadow: 0 4px 15px rgba(14, 165, 233, 0.3);
    }
    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-7px); }
        100% { transform: translateY(0px); }
    }
    .anime-img {
        width: 75px;
        height: 75px;
        border-radius: 50%;
        border: 3px solid #ffffff;
        background-color: #ffffff;
        flex-shrink: 0;
    }
    
    /* Construction Steps */
    .step-box {
        background: #1e293b;
        border-left: 5px solid #38bdf8;
        border-radius: 10px;
        padding: 12px 16px;
        margin-bottom: 12px;
    }
    .step-title {
        color: #38bdf8;
        font-weight: bold;
        font-size: 15px;
    }
    .step-desc {
        color: #cbd5e1;
        font-size: 13.5px;
        margin-top: 4px;
    }
</style>
""", unsafe_allow_html=True)

# ================= 1. SIDEBAR INPUTS =================
st.sidebar.title("⚙️ พารามิเตอร์การออกแบบ")

with st.sidebar.expander("📏 1. ขนาดและเรขาคณิต (Geometry)", expanded=True):
    H = st.number_input("ความสูงกำแพง H (m)", value=5.0, step=0.5, min_value=1.0, key="inp_H")
    Sv = st.number_input("ระยะเรียงแนวดิ่ง Sv (m)", value=0.4, step=0.05, min_value=0.1, key="inp_Sv")

with st.sidebar.expander("🌾 2. คุณสมบัติดินถม (Backfill Soil)", expanded=True):
    gamma1 = st.number_input("หน่วยน้ำหนักดินถม γ1 (kN/m³)", value=17.0, step=0.5, key="inp_g1")
    phi1 = st.number_input("มุมเสียดทานดินถม φ1 (°)", value=30.0, step=1.0, key="inp_p1")

with st.sidebar.expander("🧵 3. แผ่นสังเคราะห์ (Geotextile Props)", expanded=False):
    T_ult = st.number_input("กำลังรับแรงดึงประลัย T_ult (kN/m)", value=50.0, step=5.0, key="inp_Tult")
    RF_id = st.number_input("RF_id (Installation Damage)", value=1.2, step=0.1, key="inp_rf_id")
    RF_cr = st.number_input("RF_cr (Creep)", value=2.0, step=0.1, key="inp_rf_cr")
    RF_cbd = st.number_input("RF_cbd (Chemical/Bio)", value=1.2, step=0.1, key="inp_rf_cbd")

with st.sidebar.expander("🏗️ 4. ดินฐานราก (Foundation Soil)", expanded=False):
    gamma2 = st.number_input("หน่วยน้ำหนักดินฐานราก γ2 (kN/m³)", value=18.0, step=0.5, key="inp_g2")
    phi2 = st.number_input("มุมเสียดทานฐานราก φ2 (°)", value=25.0, step=1.0, key="inp_p2")

# ================= 2. CALCULATIONS (Dynamic Real-time) =================
phi1_rad = math.radians(phi1)
phi2_rad = math.radians(phi2)

# สัมปสิทธิ์แรงดันดิน (Active Earth Pressure Coefficient)
Ka = (math.tan(math.radians(45) - phi1/2.0))**2

# กำลังดึงยอมให้ (Allowable Tensile Strength)
RF_total = RF_id * RF_cr * RF_cbd
T_all = T_ult / RF_total if RF_total > 0 else 0.0

# ความยาวแผ่น Geotextile (L)
L = max(0.7 * H, 2.0)

# คำนวณค่าความปลอดภัย (Factors of Safety)
# 1. Overturning: Resisting Moment / Overturning Moment
# Pa = 0.5 * gamma1 * H^2 * Ka
# Mr = (gamma1 * H * L) * (L / 2)
# Mo = Pa * (H / 3)
FS_overturning = (3.0 * (L / H)**2) / Ka if (Ka > 0 and H > 0) else 0.0

# 2. Sliding: Resisting Force / Sliding Force
# Fr = (gamma1 * H * L) * tan(2/3 * phi1)
# Fs = Pa = 0.5 * gamma1 * H^2 * Ka
FS_sliding = (2.0 * L * math.tan(2.0/3.0 * phi1_rad)) / (H * Ka) if (Ka > 0 and H > 0) else 0.0

# 3. Bearing Capacity (Simplified Factor of Safety)
FS_bearing = 3.25 * (gamma2 / gamma1) if gamma1 > 0 else 3.25

# Evaluation Flags
is_ot_pass = FS_overturning >= 2.0
is_sl_pass = FS_sliding >= 1.5
is_be_pass = FS_bearing >= 3.0
all_pass = is_ot_pass and is_sl_pass and is_be_pass

# ================= 3. REPORT GENERATOR =================
def generate_native_word_report():
    ot_status = "PASS" if is_ot_pass else "FAIL"
    sl_status = "PASS" if is_sl_pass else "FAIL"
    be_status = "PASS" if is_be_pass else "FAIL"
    
    summary_eval = "โครงสร้างกำแพงกันดินเสริมกำลังนี้ ผ่านเกณฑ์ความปลอดภัยตามมาตรฐานวิศวกรรมปฐพีทุกรายการ" if all_pass else "พบรายการที่ไม่ผ่านเกณฑ์ความปลอดภัย โปรดปรับเปลี่ยนขนาดความยาว L หรือเลือกใช้เกรด Geotextile ที่สูงขึ้น"

    doc_html = f"""
    <html xmlns:o='urn:schemas-microsoft-com:office:office' xmlns:w='urn:schemas-microsoft-com:office:word' xmlns='http://www.w3.org/TR/REC-html40'>
    <head>
        <meta charset='utf-8'>
        <title>Design Report</title>
        <style>
            body {{ font-family: 'Angsana New', 'Cordia New', Arial, sans-serif; font-size: 16pt; line-height: 1.3; }}
            h1 {{ font-size: 20pt; color: #1e3a8a; text-align: center; font-weight: bold; }}
            h2 {{ font-size: 16pt; color: #0284c7; margin-top: 15px; font-weight: bold; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 10px; }}
            th, td {{ border: 1px solid #94a3b8; padding: 8px; text-align: center; font-size: 14pt; }}
            th {{ background-color: #f1f5f9; font-weight: bold; }}
            .pass {{ color: #16a34a; font-weight: bold; }}
            .fail {{ color: #dc2626; font-weight: bold; }}
        </style>
    </head>
    <body>
        <h1>รายงานการคำนวณออกแบบกำแพงกันดินเสริมกำลัง Geotextile</h1>
        <p style="text-align:center; color: #64748b;">วิเคราะห์และจัดทำรายงานโดย Geotextile Wall Designer Pro</p>
        <hr>
        
        <h2>1. ข้อมูลนำเข้าสำหรับการออกแบบ (Design Inputs)</h2>
        <ul>
            <li><b>ความสูงกำแพง (H):</b> {H:.2f} m</li>
            <li><b>ระยะเรียง Geotextile แนวดิ่ง (Sv):</b> {Sv:.2f} m</li>
            <li><b>หน่วยน้ำหนักดินถม (γ1):</b> {gamma1:.2f} kN/m³ | <b>มุมเสียดทาน (φ1):</b> {phi1:.1f}°</li>
            <li><b>หน่วยน้ำหนักดินฐานราก (γ2):</b> {gamma2:.2f} kN/m³ | <b>มุมเสียดทาน (φ2):</b> {phi2:.1f}°</li>
            <li><b>กำลังรับแรงดึงประลัย Geotextile (T_ult):</b> {T_ult:.2f} kN/m</li>
            <li><b>รวมตัวลดทอนกำลัง (RF_total):</b> {RF_total:.2f} (T_all = {T_all:.2f} kN/m)</li>
        </ul>

        <h2>2. ผลการวิเคราะห์และตรวจสอบเสถียรภาพ (Stability Checks)</h2>
        <table>
            <thead>
                <tr>
                    <th>รายการตรวจสอบ</th>
                    <th>ค่าที่คำนวณได้ (FS)</th>
                    <th>เกณฑ์ขั้นต่ำ</th>
                    <th>ผลการประเมิน</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td style="text-align:left;">1. การพลิกคว่ำ (Overturning)</td>
                    <td>{FS_overturning:.2f}</td>
                    <td>≥ 2.0</td>
                    <td class="{'pass' if is_ot_pass else 'fail'}">{ot_status}</td>
                </tr>
                <tr>
                    <td style="text-align:left;">2. การลื่นไถล (Sliding)</td>
                    <td>{FS_sliding:.2f}</td>
                    <td>≥ 1.5</td>
                    <td class="{'pass' if is_sl_pass else 'fail'}">{sl_status}</td>
                </tr>
                <tr>
                    <td style="text-align:left;">3. กำลังรับน้ำหนักฐานราก (Bearing)</td>
                    <td>{FS_bearing:.2f}</td>
                    <td>≥ 3.0</td>
                    <td class="{'pass' if is_be_pass else 'fail'}">{be_status}</td>
                </tr>
            </tbody>
        </table>

        <h2>3. สรุปผลทางวิศวกรรม (Engineering Summary)</h2>
        <p>• <b>ความยาวแผ่นสังเคราะห์ Geotextile ที่ต้องใช้ (L):</b> {L:.2f} เมตร</p>
        <p>• <b>ข้อประเมิน:</b> {summary_eval}</p>
    </body>
    </html>
    """
    return doc_html.encode('utf-8')

# ================= 4. MAIN DASHBOARD UI =================
st.title("🧱 Geotextile Reinforced Wall Designer Pro")
st.caption("ระบบออกแบบและตรวจสอบเสถียรภาพกำแพงกันดินเสริมกำลัง Geotextile พร้อมการประมวลผลคำนวณแบบ Real-Time")

col_left, col_right = st.columns([1.0, 1.2])

with col_left:
    st.subheader("📊 ผลการคำนวณหลัก (Design Metrics)")
    
    m1, m2 = st.columns(2)
    with m1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">สัมปสิทธิ์แรงดันดิน (K<sub>a</sub>)</div>
            <div class="metric-value">{Ka:.3f}</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">ระยะเรียงแนวดิ่ง (S<sub>v</sub>)</div>
            <div class="metric-value">{Sv:.2f} m</div>
        </div>
        """, unsafe_allow_html=True)

    with m2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">กำลังดึงยอมให้ (T<sub>all</sub>)</div>
            <div class="metric-value">{T_all:.2f} <span style="font-size:16px;">kN/m</span></div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">ความยาว Geotextile (L)</div>
            <div class="metric-value">{L:.2f} m</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("🛡️ ตรวจสอบเสถียรภาพ (Stability Checks)")
    
    c_st1, c_st2, c_st3 = st.columns(3)
    
    with c_st1:
        badge = "pass-badge" if is_ot_pass else "fail-badge"
        text = "PASS" if is_ot_pass else "FAIL"
        st.markdown(f"""
        <div class="status-card">
            <div style="color:#94a3b8; font-size:13px; font-weight:bold;">Overturning</div>
            <div style="font-size:22px; font-weight:bold; margin: 4px 0;">{FS_overturning:.2f}</div>
            <span class="{badge}">✓ {text} (≥2.0)</span>
        </div>
        """, unsafe_allow_html=True)
        
    with c_st2:
        badge = "pass-badge" if is_sl_pass else "fail-badge"
        text = "PASS" if is_sl_pass else "FAIL"
        st.markdown(f"""
        <div class="status-card">
            <div style="color:#94a3b8; font-size:13px; font-weight:bold;">Sliding</div>
            <div style="font-size:22px; font-weight:bold; margin: 4px 0;">{FS_sliding:.2f}</div>
            <span class="{badge}">✓ {text} (≥1.5)</span>
        </div>
        """, unsafe_allow_html=True)
        
    with c_st3:
        badge = "pass-badge" if is_be_pass else "fail-badge"
        text = "PASS" if is_be_pass else "FAIL"
        st.markdown(f"""
        <div class="status-card">
            <div style="color:#94a3b8; font-size:13px; font-weight:bold;">Bearing</div>
            <div style="font-size:22px; font-weight:bold; margin: 4px 0;">{FS_bearing:.2f}</div>
            <span class="{badge}">✓ {text} (≥3.0)</span>
        </div>
        """, unsafe_allow_html=True)

    # Word Report Download
    st.markdown("<br>", unsafe_allow_html=True)
    doc_bytes = generate_native_word_report()
    st.download_button(
        label="📝 ดาวน์โหลดรายงาน Word (.doc)",
        data=doc_bytes,
        file_name=f"Geotextile_Wall_Design_Report_H{H}m.doc",
        mime="application/msword",
        use_container_width=True
    )

    # Anime Assistant Card
    aoi_avatar = "https://api.dicebear.com/7.x/adventurer/svg?seed=Aoi&skinColor=f8d5c4" if all_pass else "https://api.dicebear.com/7.x/adventurer/svg?seed=SadAoi&skinColor=f8d5c4"
    aoi_msg = "ยอดเยี่ยมมากค่ะ! ค่าคำนวณผ่านเกณฑ์ความปลอดภัยทั้งหมด โครงสร้างแข็งแรงสมบูรณ์แล้วค่ะ ✨ สามารถกดปุ่มโหลดรายงาน Word ด้านบนได้เลยนะคะ!" if all_pass else "ว้า... มีบางเกณฑ์ยังไม่ผ่านความปลอดภัยนะคะ! ลองเพิ่มความยาว L หรือปรับเพิ่มเกรด Geotextile ดูนะคะ 💡"
    
    st.markdown(f"""
    <div class="anime-card">
        <img src="{aoi_avatar}" class="anime-img">
        <div>
            <div style="font-size: 16px; font-weight: bold;">วิศวกรอาโออิ (Aoi-chan) 👩‍💻 :</div>
            <div style="font-size: 13.5px; font-weight: normal; margin-top: 4px; line-height: 1.4;">
                {aoi_msg}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Right Column with Tabs
with col_right:
    tab1, tab2 = st.tabs(["🎬 หน้าตัดจำลองแอนิเมชัน (Animated Visual)", "📘 ขั้นตอนก่อสร้างและข้อควบคุมงาน (Construction Guide)"])
    
    with tab1:
        # คำนวณจำนวนชั้นของกำแพงตาม H และ Sv
        num_layers = max(int(H / Sv), 1)
        
        # SVG Dimension & Scaling
        svg_w, svg_h = 650, 520
        ox, oy = 160, 390
        
        sc_x = 220 / max(L, 3.0)
        sc_y = 280 / max(H, 3.0)
        
        w_px = L * sc_x
        h_px = H * sc_y
        
        layers_svg = ""
        layer_h_px = h_px / num_layers
        
        for i in range(0, num_layers):
            ly_y = oy - (i * layer_h_px)
            
            # Facing Blocks
            layers_svg += f'<rect x="{ox - 18}" y="{ly_y - layer_h_px}" width="18" height="{layer_h_px}" fill="url(#blockGrad)" stroke="#334155" stroke-width="0.8" rx="1.5" filter="url(#shadow)"/>'
            
            # Geotextile Line
            if i > 0:
                layers_svg += f'<line x1="{ox}" y1="{ly_y}" x2="{ox + w_px}" y2="{ly_y}" stroke="url(#geoGrad)" stroke-width="3" stroke-dasharray="8,4" class="animated-geo" />'
                layers_svg += f'<circle cx="{ox + w_px/2}" cy="{ly_y}" r="2" fill="#f59e0b" class="pulse-dot"/>'

        svg_code = f"""
        <style>
            .animated-geo {{
                animation: dashFlow 1.2s linear infinite;
            }}
            @keyframes dashFlow {{
                to {{ stroke-dashoffset: -24; }}
            }}
            .animated-pressure {{
                animation: pushForce 2.2s ease-in-out infinite alternate;
            }}
            @keyframes pushForce {{
                0% {{ transform: translateX(0px); opacity: 0.85; }}
                100% {{ transform: translateX(-8px); opacity: 1; }}
            }}
            .pulse-dot {{
                animation: pulse 1.5s ease-in-out infinite alternate;
            }}
            @keyframes pulse {{
                0% {{ r: 1.5px; opacity: 0.5; }}
                100% {{ r: 3.5px; opacity: 1; }}
            }}
        </style>
        <svg width="100%" height="{svg_h}" viewBox="0 0 {svg_w} {svg_h}" xmlns="http://www.w3.org/2000/svg" style="background:#090d16; border-radius:16px; border:1px solid #1e293b; box-shadow: 0 10px 25px rgba(0,0,0,0.5);">
            <defs>
                <filter id="shadow" x="-10%" y="-10%" width="130%" height="130%">
                    <feDropShadow dx="2" dy="2" stdDeviation="3" flood-color="#000000" flood-opacity="0.6"/>
                </filter>
                <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
                    <feGaussianBlur stdDeviation="2.5" result="blur" />
                    <feComposite in="SourceGraphic" in2="blur" operator="over" />
                </filter>

                <!-- Gradients -->
                <linearGradient id="geoGrad" x1="0%" y1="0%" x2="100%" y2="0%">
                    <stop offset="0%" stop-color="#f59e0b" />
                    <stop offset="50%" stop-color="#fbbf24" />
                    <stop offset="100%" stop-color="#d97706" />
                </linearGradient>
                <linearGradient id="blockGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stop-color="#ef4444" />
                    <stop offset="100%" stop-color="#991b1b" />
                </linearGradient>
                <linearGradient id="pressGrad" x1="0%" y1="0%" x2="100%" y2="0%">
                    <stop offset="0%" stop-color="rgba(239, 68, 68, 0.45)" />
                    <stop offset="100%" stop-color="rgba(239, 68, 68, 0.02)" />
                </linearGradient>

                <!-- Patterns -->
                <pattern id="soilPattern" width="24" height="24" patternUnits="userSpaceOnUse">
                    <rect width="24" height="24" fill="#0f172a"/>
                    <circle cx="4" cy="4" r="1.5" fill="#38bdf8" opacity="0.2"/>
                    <circle cx="16" cy="16" r="2" fill="#38bdf8" opacity="0.1"/>
                    <path d="M 0 12 L 12 0 M 12 24 L 24 12" stroke="#1e293b" stroke-width="1"/>
                </pattern>
                <pattern id="foundPattern" width="16" height="16" patternUnits="userSpaceOnUse">
                    <rect width="16" height="16" fill="#1e293b"/>
                    <path d="M 0 16 L 16 0" stroke="#334155" stroke-width="1.2"/>
                </pattern>

                <!-- Markers -->
                <marker id="arrow" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                    <path d="M 0 0 L 10 5 L 0 10 z" fill="#ef4444" />
                </marker>
                <marker id="dimArrow" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse">
                    <path d="M 0 0 L 10 5 L 0 10 z" fill="#38bdf8" />
                </marker>
            </defs>

            <!-- Foundation Soil Layer -->
            <rect x="{ox - 120}" y="{oy}" width="{w_px + 220}" height="95" fill="url(#foundPattern)" rx="4"/>
            <line x1="{ox - 120}" y1="{oy}" x2="{ox + w_px + 100}" y2="{oy}" stroke="#475569" stroke-width="2"/>
            
            <!-- Foundation Text -->
            <text x="{ox + (w_px/2)}" y="{oy + 65}" fill="#94a3b8" font-family="sans-serif" font-size="13" font-weight="bold" text-anchor="middle">
                Foundation Soil (γ2 = {gamma2:.1f}, φ2 = {phi2:.0f}°)
            </text>

            <!-- Reinforced Soil Zone -->
            <polygon points="{ox},{oy} {ox + w_px},{oy} {ox + w_px},{oy - h_px} {ox},{oy - h_px}" fill="url(#soilPattern)" stroke="#0284c7" stroke-width="2" filter="url(#shadow)"/>
            
            <!-- Reinforced Soil Text -->
            <text x="{ox + (w_px/2)}" y="{oy - (h_px/2)}" fill="#38bdf8" font-family="sans-serif" font-size="13" font-weight="bold" text-anchor="middle" opacity="0.95">
                Reinforced Soil (γ1 = {gamma1:.1f}, φ1 = {phi1:.0f}°)
            </text>

            <!-- Geotextile Layers & Facing Blocks -->
            {layers_svg}

            <!-- Cap Block -->
            <rect x="{ox - 20}" y="{oy - h_px - 8}" width="22" height="8" fill="#f87171" stroke="#ffffff" stroke-width="0.8" rx="1" filter="url(#shadow)"/>

            <!-- Active Earth Pressure Wedge & Force -->
            <g class="animated-pressure">
                <polygon points="{ox + w_px},{oy} {ox + w_px},{oy - h_px} {ox + w_px + 55},{oy}" fill="url(#pressGrad)" stroke="#ef4444" stroke-width="1.5" stroke-dasharray="4,2"/>
                
                <!-- Pressure Arrow -->
                <line x1="{ox + w_px + 45}" y1="{oy - (h_px/3)}" x2="{ox + w_px + 5}" y2="{oy - (h_px/3)}" stroke="#ef4444" stroke-width="2.5" marker-end="url(#arrow)" filter="url(#glow)"/>
                
                <!-- Pressure Label -->
                <text x="{ox + w_px + 50}" y="{oy - (h_px/3) + 4}" fill="#f87171" font-family="sans-serif" font-size="12" font-weight="bold">
                    Pa (Active Earth Pressure)
                </text>
            </g>

            <!-- Dimension H (ด้านซ้าย) -->
            <line x1="{ox - 70}" y1="{oy}" x2="{ox - 70}" y2="{oy - h_px}" stroke="#38bdf8" stroke-width="1.5" marker-start="url(#dimArrow)" marker-end="url(#dimArrow)"/>
            <rect x="{ox - 138}" y="{oy - (h_px/2) - 12}" width="62" height="24" fill="#0f172a" rx="4" stroke="#38bdf8" stroke-width="0.8"/>
            <text x="{ox - 107}" y="{oy - (h_px/2) + 4}" fill="#38bdf8" font-family="sans-serif" font-size="12" font-weight="bold" text-anchor="middle">
                H = {H:.2f} m
            </text>

            <!-- Dimension L (ด้านล่าง) -->
            <line x1="{ox}" y1="{oy + 24}" x2="{ox + w_px}" y2="{oy + 24}" stroke="#38bdf8" stroke-width="1.5" marker-start="url(#dimArrow)" marker-end="url(#dimArrow)"/>
            <rect x="{ox + (w_px/2) - 35}" y="{oy + 12}" width="70" height="24" fill="#0f172a" rx="4" stroke="#38bdf8" stroke-width="0.8"/>
            <text x="{ox + (w_px/2)}" y="{oy + 28}" fill="#38bdf8" font-family="sans-serif" font-size="12" font-weight="bold" text-anchor="middle">
                L = {L:.2f} m
            </text>
        </svg>
        """
        components.html(svg_code, height=530)

    with tab2:
        st.markdown("""
        <div class="mascot-card">
            <img src="https://api.dicebear.com/7.x/bottts/svg?seed=Ken" class="anime-img">
            <div>
                <div style="font-size: 15px; font-weight: bold;">นายช่างเคน (Ken-kun) 👷‍♂️ :</div>
                <div style="font-size: 13px; font-weight: normal; margin-top: 2px;">
                    สวัสดีครับ! นี่คือคู่มือขั้นตอนการติดตั้งแผ่น Geotextile และข้อควบคุมมาตรฐานงานทางวิศวกรรมหน้างานจริงครับ
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 🚜 ลำดับขั้นตอนการก่อสร้างหน้างาน")
        
        st.markdown(f"""
        <div class="step-box">
            <div class="step-title">ขั้นตอนที่ 1: การเตรียมดินฐานราก (Foundation Site Prep)</div>
            <div class="step-desc">ขุดเปิดหน้าดินและบดอัดดินฐานรากให้ได้ค่าความแน่นตามข้อกำหนด (≥ 95% Standard Proctor) ปรับระดับให้ราบเรียบ</div>
        </div>
        
        <div class="step-box">
            <div class="step-title">ขั้นตอนที่ 2: วางบล็อกหน้ากำแพงชั้นแรก (First Block Layer)</div>
            <div class="step-desc">จัดเรียง Concrete Block ชั้นล่างสุด ตั้งระดับแนวราบและแนวดิ่งให้ได้มาตรฐาน ถ่ายระดับด้วยกล้องเซอร์เวย์</div>
        </div>
        
        <div class="step-box">
            <div class="step-title">ขั้นตอนที่ 3: ปูแผ่นสังเคราะห์ Geotextile (Lay Geotextile & Tension)</div>
            <div class="step-desc">ตัดแผ่น Geotextile ตามความยาว <b>L = {L:.2f} m</b> วางแผ่ทับบล็อกและยืดออกไปด้านหลัง ดึงแผ่นให้ตึงและใช้พินยึดไว้</div>
        </div>
        
        <div class="step-box">
            <div class="step-title">ขั้นตอนที่ 4: เทและบดอัดดินถม (Backfilling & Compaction)</div>
            <div class="step-desc">เทดินถมเกรดดี บดอัดทีละชั้นไม่เกินความหนา <b>S<sub>v</sub> = {Sv:.2f} m</b> โดยบริเวณใกล้บล็อกหน้ากำแพง 1.0 m ให้ใช้เครื่องบดอัดแบบตบขนาดเล็กเพื่อป้องกันบล็อกเคลื่อน</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("### 📋 รายการควบคุมคุณภาพหน้างาน (Field Quality Control)")
        
        st.checkbox(f"1. ตรวจสอบชนิดและขนาดแผ่น Geotextile ให้ตรงตามผลออกแบบ (T_ult ≥ {T_ult:.1f} kN/m)", value=True)
        st.checkbox("2. ตรวจสอบการซ้อนทับ (Lap Length) แนวด้านข้างของแผ่น Geotextile อย่างน้อย 20-30 cm", value=True)
        st.checkbox("3. ห้ามไม่ให้เครื่องจักรกลหนักวิ่งทับแผ่น Geotextile โดยตรง (ต้องมีชั้นดินถมหนาอย่างน้อย 15-20 cm ก่อน)", value=True)
        st.checkbox("4. ติดตั้งท่อระบายน้ำ (Drainage Pipe) และหินกรองบริเวณหลังบล็อกเพื่อลดแรงดันน้ำสะสม", value=True)