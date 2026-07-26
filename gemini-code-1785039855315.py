with tab1:
        num_layers = int(H / Sv)
        
        # ปรับขนาด Canvas และจุดอ้างอิงให้กว้าง อ่านง่ายขึ้น
        svg_w, svg_h = 600, 520
        ox, oy = 130, 390
        
        sc_x = 220 / max(L, 3.0)
        sc_y = 280 / max(H, 3.0)
        
        w_px = L * sc_x
        h_px = H * sc_y
        
        layers_svg = ""
        layer_h_px = h_px / max(num_layers, 1)
        
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
            <rect x="{ox - 80}" y="{oy}" width="{w_px + 160}" height="95" fill="url(#foundPattern)" rx="4"/>
            <line x1="{ox - 80}" y1="{oy}" x2="{ox + w_px + 80}" y2="{oy}" stroke="#475569" stroke-width="2"/>
            
            <!-- Foundation Text (ขยับลงมาล่างสุด แยกชั้นเจนชัดเจน) -->
            <text x="{ox + (w_px/2)}" y="{oy + 65}" fill="#94a3b8" font-family="sans-serif" font-size="13" font-weight="bold" text-anchor="middle">
                Foundation Soil (γ2 = {gamma2:.1f}, φ2 = {phi2:.0f}°)
            </text>

            <!-- Reinforced Soil Zone -->
            <polygon points="{ox},{oy} {ox + w_px},{oy} {ox + w_px},{oy - h_px} {ox},{oy - h_px}" fill="url(#soilPattern)" stroke="#0284c7" stroke-width="2" filter="url(#shadow)"/>
            <text x="{ox + (w_px/2)}" y="{oy - (h_px/2)}" fill="#38bdf8" font-family="sans-serif" font-size="14" font-weight="bold" text-anchor="middle" opacity="0.95">
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
                
                <!-- Pressure Label (ขยับออกขวาไม่ให้บังเส้น) -->
                <text x="{ox + w_px + 50}" y="{oy - (h_px/3) + 4}" fill="#f87171" font-family="sans-serif" font-size="12" font-weight="bold">
                    Pa (Active Earth Pressure)
                </text>
            </g>

            <!-- Dimension H (ด้านซ้าย) -->
            <line x1="{ox - 50}" y1="{oy}" x2="{ox - 50}" y2="{oy - h_px}" stroke="#38bdf8" stroke-width="1.5" marker-start="url(#dimArrow)" marker-end="url(#dimArrow)"/>
            <rect x="{ox - 118}" y="{oy - (h_px/2) - 12}" width="62" height="24" fill="#0f172a" rx="4" stroke="#38bdf8" stroke-width="0.8"/>
            <text x="{ox - 87}" y="{oy - (h_px/2) + 4}" fill="#38bdf8" font-family="sans-serif" font-size="12" font-weight="bold" text-anchor="middle">
                H = {H:.2f} m
            </text>

            <!-- Dimension L (ตรงกลาง ระหว่างฐานรากกับดินถม) -->
            <line x1="{ox}" y1="{oy + 24}" x2="{ox + w_px}" y2="{oy + 24}" stroke="#38bdf8" stroke-width="1.5" marker-start="url(#dimArrow)" marker-end="url(#dimArrow)"/>
            <rect x="{ox + (w_px/2) - 35}" y="{oy + 12}" width="70" height="24" fill="#0f172a" rx="4" stroke="#38bdf8" stroke-width="0.8"/>
            <text x="{ox + (w_px/2)}" y="{oy + 28}" fill="#38bdf8" font-family="sans-serif" font-size="12" font-weight="bold" text-anchor="middle">
                L = {L:.2f} m
            </text>
        </svg>
        """
        components.html(svg_code, height=530)