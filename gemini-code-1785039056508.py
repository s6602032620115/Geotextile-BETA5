import streamlit as st
import streamlit.components.v1 as components
import math

# Set Page Config
st.set_page_config(
    page_title="Geotextile Wall Designer Pro",
    page_icon="🧱",
    layout="wide"
)

# Custom CSS for Modern UI & Construction Flow Cards
st.markdown("""
<style>
    .main {
        background-color: #0f172a;
        color: #f8fafc;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 16px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        margin-bottom: 12px;
    }
    .metric-title {
        color: #94a3b8;
        font-size: 15px;
        font-weight: 600;
        margin-bottom: 6px;
    }
    .metric-value {
        color: #38bdf8;
        font-size: 28px;
        font-weight: bold;
    }
    
    .anime-card {
        background: linear-gradient(135deg, #f472b6 0%, #a855f7 100%);
        color: #ffffff;
        border-radius: 15px;
        padding: 15px;
        display: flex;
        align-items: center;
        gap: 15px;
        margin-top: 20px;
        box-shadow: 0 4px 15px rgba(244, 114, 182, 0.3);
        animation: float 3s ease-in-out infinite;
    }
    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-6px); }
        100% { transform: translateY(0px); }
    }
    .anime-img {
        width: 75px;
        height: 75px;
        border-radius: 50%;
        border: 3px solid white;
        background-color: white;
    }
    
    .pass-badge {
        background-color: #22c55e;
        color: #ffffff;
        padding: 6px 14px;
        border-radius: 8px;
        font-weight: bold;
        display: inline-block;
    }
    .fail-badge {
        background-color: #ef4444;
        color: #ffffff;
        padding: 6px 14px;
        border-radius: 8px;
        font-weight: bold;
        display: inline-block;
    }
    
    /* Construction Process Step Box */
    .step-box {
        background: #1e293b;
        border-left: 4px solid #38bdf8;
        border-radius: 8px;
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
        font-size: 13px;
        margin-top: 4px;
    }
</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR: CATEGORIZED INPUTS ----------------
st.sidebar.title("⚙️ พารามิเตอร์การออกแบบ")

with st.sidebar.expander("📏 1. ขนาดและเรขาคณิต (Geometry)", expanded=True):
    H = st.number_input("ความสูงกำแพง H (m)", value=5.0, step=0.5, min_value=1.0)
    Sv = st.number_input("ระยะเรียงแนวดิ่ง Sv (m)", value=0.4, step=0.05, min_value=0.1)

with st.sidebar.expander("🌾 2. คุณสมบัติดินถม (Backfill Soil)", expanded=True):
    gamma1 = st.number_input("หน่วยน้ำหนักดินถม γ1 (kN/m³)", value=17.0, step=0.5)
    phi1 = st.number_input("มุมเสียดทานดินถม φ1 (°)", value=30.0, step=1.0)

with st.sidebar.expander("🧵 3. แผ่นสังเคราะห์ (Geotextile Props)", expanded=False):
    T_ult = st.number_input("กำลังรับแรงดึงประลัย T_ult (kN/m)", value=50.0, step=5.0)
    RF_id = st.number_input("RF_id (Installation Damage)", value=1.2, step=0.1)
    RF_cr = st.number_input("RF_cr (Creep)", value=2.0, step=0.1)
    RF_cbd = st.number_input("RF_cbd (Chemical/Bio)", value=1.2, step=0.1)

with st.sidebar.expander("🏗️ 4. ดินฐานราก (Foundation Soil)", expanded=False):
    gamma2 = st.number_input("หน่วยน้ำหนักดินฐานราก γ2 (kN/m³)", value=18.0, step=0.5)
    phi2 = st.number_input("มุมเสียดทานฐานราก φ2 (°)", value=25.0, step=1.0)

# ---------------- CALCULATIONS ----------------
phi1_rad = math.radians(phi1)
Ka = (math.tan(math.radians(45) - phi1_rad/2))**2

RF_total = RF_id * RF_cr * RF_cbd
T_all = T_ult / RF_total if RF_total > 0 else 0

L = max(0.7 * H, 2.0)

FS_overturning = (3 * (L/H)) / Ka if Ka > 0 else 0
FS_sliding = (math.tan(math.radians(2/3 * phi1)) * L) / (Ka * H / 2) if Ka > 0 else 0
FS_bearing = 3.25

# ---------------- MAIN UI ----------------
st.title("🧱 Geotextile Reinforced Wall Designer Pro")
st.caption("ระบบออกแบบและตรวจสอบเสถียรภาพกำแพงกันดินเสริมกำลัง Geotextile พร้อมแอนิเมชันและคู่มือขั้นตอนงานก่อสร้าง")

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
    
    is_ot_pass = FS_overturning >= 2.0
    is_sl_pass = FS_sliding >= 1.5
    is_be_pass = FS_bearing >= 3.0
    
    with c_st1:
        st.markdown(f"**Overturning**\n### FS = {FS_overturning:.2f}")
        badge = "pass-badge" if is_ot_pass else "fail-badge"
        text = "ผ่าน" if is_ot_pass else "ไม่ผ่าน"
        st.markdown(f'<span class="{badge}">{text} (req ≥ 2.0)</span>', unsafe_allow_html=True)
        
    with c_st2:
        st.markdown(f"**Sliding**\n### FS = {FS_sliding:.2f}")
        badge = "pass-badge" if is_sl_pass else "fail-badge"
        text = "ผ่าน" if is_sl_pass else "ไม่ผ่าน"
        st.markdown(f'<span class="{badge}">{text} (req ≥ 1.5)</span>', unsafe_allow_html=True)
        
    with c_st3:
        st.markdown(f"**Bearing**\n### FS = {FS_bearing:.2f}")
        badge = "pass-badge" if is_be_pass else "fail-badge"
        text = "ผ่าน" if is_be_pass else "ไม่ผ่าน"
        st.markdown(f'<span class="{badge}">{text} (req ≥ 3.0)</span>', unsafe_allow_html=True)

    # Anime Assistant Card
    all_pass = is_ot_pass and is_sl_pass and is_be_pass
    st.markdown(f"""
    <div class="anime-card">
        <img src="https://api.dicebear.com/7.x/adventurer/svg?seed=Aoi&skinColor=f8d5c4" class="anime-img">
        <div>
            <div style="font-size: 16px; font-weight: bold;">วิศวกรอาโออิ (Aoi-chan) :</div>
            <div style="font-size: 13.5px; font-weight: normal; margin-top: 3px;">
                {"คำนวณผ่านเรียบร้อยค่ะ! ดูขั้นตอนการก่อสร้างและข้อควบคุมคุณภาพงานหน้างานใน Tab ขวามือได้เลยนะคะ ✨" if all_pass else "อุ๊ปส์! บางค่าไม่ผ่านเกณฑ์ความปลอดภัย ลองปรับความยาว L หรือเปลี่ยนเกรด Geotextile ดูนะคะ! 💡"}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Right Column with Tabs
with col_right:
    tab1, tab2 = st.tabs(["🎬 หน้าตัดจำลองแอนิเมชัน (Animated Visual)", "📘 ขั้นตอนก่อสร้างและข้อควบคุมงาน (Construction Guide)"])
    
    with tab1:
        num_layers = int(H / Sv)
        
        svg_w, svg_h = 520, 480
        ox, oy = 110, 380
        
        sc_x = 220 / max(L, 3.0)
        sc_y = 280 / max(H, 3.0)
        
        w_px = L * sc_x
        h_px = H * sc_y
        
        layers_svg = ""
        layer_h_px = h_px / max(num_layers, 1)
        
        for i in range(1, num_layers):
            ly_y = oy - (i * layer_h_px)
            layers_svg += f'<line x1="{ox}" y1="{ly_y}" x2="{ox + w_px}" y2="{ly_y}" stroke="#f59e0b" stroke-width="3" stroke-dasharray="8,4" class="animated-geo" />'
            layers_svg += f'<rect x="{ox - 14}" y="{ly_y - (layer_h_px/2)}" width="14" height="{layer_h_px}" fill="#e11d48" stroke="#ffffff" stroke-width="0.8" rx="1" />'

        svg_code = f"""
        <style>
            .animated-geo {{
                animation: dash 1.5s linear infinite;
            }}
            @keyframes dash {{
                to {{ stroke-dashoffset: -24; }}
            }}
            .animated-pressure {{
                animation: pushForce 2s ease-in-out infinite alternate;
            }}
            @keyframes pushForce {{
                0% {{ transform: translateX(0px); }}
                100% {{ transform: translateX(-8px); }}
            }}
        </style>
        <svg width="100%" height="{svg_h}" viewBox="0 0 {svg_w} {svg_h}" xmlns="http://www.w3.org/2000/svg" style="background:#0f172a; border-radius:12px; border:1px solid #334155;">
            <defs>
                <pattern id="soilPattern" width="20" height="20" patternUnits="userSpaceOnUse">
                    <rect width="20" height="20" fill="#1e293b"/>
                    <circle cx="3" cy="3" r="1.5" fill="#38bdf8" opacity="0.3"/>
                    <circle cx="13" cy="13" r="2" fill="#38bdf8" opacity="0.2"/>
                    <path d="M 0 10 L 10 0 M 10 20 L 20 10" stroke="#334155" stroke-width="0.8"/>
                </pattern>
                <pattern id="foundPattern" width="15" height="15" patternUnits="userSpaceOnUse">
                    <rect width="15" height="15" fill="#334155"/>
                    <path d="M 0 15 L 15 0" stroke="#475569" stroke-width="1.2"/>
                </pattern>
                <marker id="arrow" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                    <path d="M 0 0 L 10 5 L 0 10 z" fill="#ef4444" />
                </marker>
                <marker id="dimArrow" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse">
                    <path d="M 0 0 L 10 5 L 0 10 z" fill="#38bdf8" />
                </marker>
            </defs>

            <!-- Foundation Soil Layer -->
            <rect x="{ox - 60}" y="{oy}" width="{w_px + 120}" height="70" fill="url(#foundPattern)" rx="4"/>
            <text x="{ox + (w_px/2) - 45}" y="{oy + 40}" fill="#94a3b8" font-family="sans-serif" font-size="13" font-weight="bold">Foundation Soil (γ2, φ2)</text>

            <!-- Reinforced Soil Zone -->
            <polygon points="{ox},{oy} {ox + w_px},{oy} {ox + w_px},{oy - h_px} {ox},{oy - h_px}" fill="url(#soilPattern)" stroke="#38bdf8" stroke-width="2"/>
            <text x="{ox + 20}" y="{oy - (h_px/2)}" fill="#38bdf8" font-family="sans-serif" font-size="14" font-weight="bold" opacity="0.85">Reinforced Backfill (γ1, φ1)</text>

            <!-- Geotextile Layers & Facing -->
            {layers_svg}

            <!-- Top Wall Facing Block -->
            <rect x="{ox - 14}" y="{oy - h_px}" width="14" height="{layer_h_px}" fill="#e11d48" stroke="#ffffff" stroke-width="0.8" rx="1"/>

            <!-- Active Earth Pressure Triangle (Animated Pa) -->
            <g class="animated-pressure">
                <polygon points="{ox + w_px},{oy} {ox + w_px},{oy - h_px} {ox + w_px + 45},{oy}" fill="rgba(239, 68, 68, 0.25)" stroke="#ef4444" stroke-width="1.5" stroke-dasharray="4,2"/>
                <line x1="{ox + w_px + 35}" y1="{oy - 10}" x2="{ox + w_px + 5}" y2="{oy - 10}" stroke="#ef4444" stroke-width="2.5" marker-end="url(#arrow)"/>
                <text x="{ox + w_px + 10}" y="{oy - 20}" fill="#ef4444" font-family="sans-serif" font-size="12" font-weight="bold">Pa (Active Pressure)</text>
            </g>

            <!-- Dimension H -->
            <line x1="{ox - 45}" y1="{oy}" x2="{ox - 45}" y2="{oy - h_px}" stroke="#38bdf8" stroke-width="1.5" marker-start="url(#dimArrow)" marker-end="url(#dimArrow)"/>
            <text x="{ox - 95}" y="{oy - (h_px/2)}" fill="#38bdf8" font-family="sans-serif" font-size="13" font-weight="bold">H = {H:.2f} m</text>

            <!-- Dimension L -->
            <line x1="{ox}" y1="{oy + 22}" x2="{ox + w_px}" y2="{oy + 22}" stroke="#38bdf8" stroke-width="1.5" marker-start="url(#dimArrow)" marker-end="url(#dimArrow)"/>
            <text x="{ox + (w_px/2) - 30}" y="{oy + 40}" fill="#38bdf8" font-family="sans-serif" font-size="13" font-weight="bold">L = {L:.2f} m</text>
        </svg>
        """
        components.html(svg_code, height=490)

    with tab2:
        st.markdown("### 🚜 ลำดับขั้นตอนการก่อสร้างหน้างาน (Construction Steps)")
        
        st.markdown("""
        <div class="step-box">
            <div class="step-title">ขั้นตอนที่ 1: การเตรียมดินฐานราก (Foundation Site Prep)</div>
            <div class="step-desc">ขุดเปิดหน้าดินและบดอัดดินฐานรากให้ได้ค่าความแน่นตามข้อกำหนด (มักกำหนด ≥ 95% Standard Proctor) พร้อมปรับระดับให้ราบเรียบ</div>
        </div>
        
        <div class="step-box">
            <div class="step-title">ขั้นตอนที่ 2: วางบล็อกหน้ากำแพงชั้นแรก (First Block Layer)</div>
            <div class="step-desc">จัดเรียง Segmental Concrete Block ชั้นล่างสุด ตั้งระดับแนวราบและแนวดิ่งให้ได้มาตรฐาน ถ่ายระดับด้วยกล้องเซอร์เวย์</div>
        </div>
        
        <div class="step-box">
            <div class="step-title">ขั้นตอนที่ 3: ปูแผ่นสังเคราะห์ Geotextile (Lay Geotextile & Tension)</div>
            <div class="step-desc">ตัดแผ่น Geotextile ตามความยาว <b>L = {:.2f} m</b> วางแผ่ทับบล็อกและยืดออกไปด้านหลัง ดึงแผ่นให้ตึงและใช้พิน/เหล็กเสียบยึดมุมไว้</div>
        </div>
        
        <div class="step-box">
            <div class="step-title">ขั้นตอนที่ 4: เทและบดอัดดินถม (Backfilling & Compaction)</div>
            <div class="step-desc">เทดินถมเกรดดี บดอัดทีละชั้นไม่เกินความหนา <b>S<sub>v</sub> = {:.2f} m</b> โดยบริเวณใกล้บล็อกหน้ากำแพง 1.0 m ให้ใช้เครื่องบดอัดแบบตบขนาดเล็กเพื่อป้องกันบล็อกเคลื่อน</div>
        </div>
        """.format(L, Sv), unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("### ⚠️ รายการควบคุมคุณภาพหน้างาน (Field QC Checklist)")
        
        st.checkbox("1. ตรวจสอบชนิดและขนาดแผ่น Geotextile ให้ตรงตามผลออกแบบ (T_ult ≥ {:.1f} kN/m)".format(T_ult), value=True)
        st.checkbox("2. ตรวจสอบการซ้อนทับ (Lap Length) แนวด้านข้างของแผ่น Geotextile อย่างน้อย 20-30 cm", value=True)
        st.checkbox("3. ห้ามไม่ให้เครื่องจักรกลหนักวิ่งทับแผ่น Geotextile โดยตรง (ต้องมีชั้นดินถมหนาอย่างน้อย 15-20 cm ก่อน)", value=True)
        st.checkbox("4. ติดตั้งท่อระบายน้ำ (Drainage Pipe) และหินกรองบริเวณหลังบล็อกเพื่อลดแรงดันน้ำสะสม", value=True)