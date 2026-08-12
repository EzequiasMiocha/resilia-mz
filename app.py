import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import base64
import io

st.set_page_config(page_title="RESILIA MZ — Simulação off-grid", layout="wide")

# ══════════════════════ ESTILO ══════════════════════
st.markdown("""
<style>
header, footer, #MainMenu {visibility:hidden;}
.stApp, [data-testid="stAppViewContainer"]{
  background:linear-gradient(160deg,#05130C 0%,#0A2013 45%,#0B2418 100%) !important;}
.stMarkdown, .stMarkdown p, [data-testid="stMarkdownContainer"] {color:#FFFFFF !important;}
[data-testid="stCaptionContainer"]{color:#F0FFF8 !important;}
h1,h2,h3,h4,h5,h6{color:#FFFFFF !important; font-weight:700;}
li{color:#FFFFFF !important;}
td,th{color:#FFFFFF !important;}

.hdr{position:sticky; top:0; z-index:999; display:flex; align-items:center; gap:16px;
  flex-wrap:wrap; padding:12px 20px; margin-bottom:2rem; border-radius:0 0 16px 16px;
  background:linear-gradient(90deg, rgba(5,19,12,.99), rgba(10,32,19,.99) 55%, rgba(12,42,24,.99));
  border:1px solid #1E4D33; border-top:none; box-shadow:0 6px 24px rgba(0,0,0,.55);}
.hdr::after{content:""; position:absolute; left:0; right:0; bottom:-1px; height:3px;
  background:linear-gradient(90deg,#FDE047,#4ADE80,#16A34A);}
.hdr-img{height:50px; width:auto; border-radius:8px;}
.hdr-img.light{background:#FFFFFF; padding:4px 8px;}
.hdr-logo{height:50px; width:50px; display:flex; align-items:center; justify-content:center;
  background:linear-gradient(135deg,#4ADE80,#22C55E); color:#05130C;
  font-weight:800; font-size:22px; border-radius:8px;}
.hdr-title{color:#FFFFFF; font-size:21px; font-weight:700; letter-spacing:.08em;}
.hdr-title span{color:#6EE7A0;}
.hdr-sub{color:#FFFFFF; font-size:12px;}
.hdr-badges{margin-left:auto; display:flex; gap:8px; flex-wrap:wrap;}
.badge{color:#FFFFFF; background:rgba(74,222,128,.14); border:1px solid #2F6B47;
  padding:5px 12px; border-radius:999px; font-size:11.5px; font-weight:500;}
.badge.gold{color:#04150B; background:linear-gradient(90deg,#6EE7A0,#22C55E); border:none; font-weight:700;}

.stTabs [data-baseweb="tab-list"]{gap:4px; background:#0A1D12; border:1px solid #1E4D33;
  padding:5px; border-radius:10px;}
.stTabs [data-baseweb="tab"]{border-radius:8px; padding:8px 18px; font-weight:600; color:#FFFFFF;}
.stTabs [aria-selected="true"]{background:#164429; color:#6EE7A0 !important;}

.explain{background:#0B2416; border:1px solid #2E7D4F; border-left:3px solid #4ADE80;
  border-radius:10px; padding:12px 16px; font-size:13.5px; color:#FFFFFF; margin:10px 0 20px 0;}
.explain b{color:#6EE7A0;}
.okbox{background:#0C2E1B; border:1px solid #2E7D4F; border-left:3px solid #6EE7A0;
  border-radius:10px; padding:12px 16px; font-size:13.5px; color:#FFFFFF; margin:8px 0 14px 0;}
.warnbox{background:#241113; border:1px solid #933333; border-left:3px solid #F87171;
  border-radius:10px; padding:12px 16px; font-size:13.5px; color:#FFFFFF; margin:8px 0 14px 0;}
.foot{margin-top:28px; padding:14px; border-radius:12px; border:1px solid #1E4D33;
  background:#0A1D12; color:#FFFFFF; font-size:12.5px; text-align:center;}

/* ── SIDEBAR ── */
[data-testid="stSidebar"]{
  background:linear-gradient(180deg,#0A1D12 0%,#0C2418 100%) !important;
  border-right:1px solid #1E4D33;}
[data-testid="stSidebar"] .stMarkdown,
[data-testid="stSidebar"] .stMarkdown p,
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"]{color:#FFFFFF !important;}
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3{color:#FFFFFF !important;}
[data-testid="stSidebar"] [data-testid="stCaptionContainer"]{color:#6EE7A0 !important;}
[data-testid="stSidebar"] hr{border-color:#1E4D33 !important;}

/* ── RÁDIOS — texto sempre visível (todas as variantes) ── */
div[data-testid="stRadio"], div[data-testid="stRadio"] label,
div[data-testid="stRadio"] p, div[data-testid="stRadio"] span,
div[data-testid="stRadio"] div{color:#FFFFFF !important; font-size:13px;}
div[data-testid="stRadio"]{color-scheme:dark;}
div[data-testid="stRadio"] [data-testid="stMarkdownContainer"] p{color:#FFFFFF !important;}

/* ── SLIDERS e CHECKBOX ── */
div[data-testid="stSlider"] label, div[data-testid="stSlider"] p,
div[data-testid="stSlider"] span{color:#FFFFFF !important; font-weight:600;}
div[data-testid="stSlider"] [data-testid="stTickBar"]{color:#6EE7A0 !important;}
div[data-testid="stSlider"] [role="slider"]{background:#4ADE80 !important; border-color:#4ADE80 !important;}
div[data-testid="stSlider"] [data-baseweb="slider"] > div > div{background:#1E4D33 !important;}
div[data-testid="stCheckbox"] label, div[data-testid="stCheckbox"] p,
div[data-testid="stCheckbox"] span{color:#FFFFFF !important;}
</style>""", unsafe_allow_html=True)

def card(titulo, valor, sub, cor):
    st.markdown(f'''<div style="background:#0C2115;border:1px solid #24583B;border-radius:12px;
      padding:14px 16px;border-top:3px solid {cor};">
      <div style="color:#6EE7A0;font-size:11px;font-weight:700;letter-spacing:.08em;text-transform:uppercase">{titulo}</div>
      <div style="color:#FFFFFF;font-size:26px;font-weight:700">{valor}</div>
      <div style="color:#FFFFFF;font-size:11px">{sub}</div></div>''', unsafe_allow_html=True)

def explicar(titulo, texto):
    st.markdown(f'<div class="explain"><b>{titulo}:</b> {texto}</div>', unsafe_allow_html=True)

def img_b64(caminho):
    try:
        with open(caminho, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except Exception:
        return None

# ══════════════════════ DADOS (Mabote) ══════════════════════
@st.cache_data
def carregar():
    try: df = pd.read_excel("dataset_offgrid_mabote_5dias_final.xlsx")
    except Exception: df = pd.read_csv("dataset_offgrid_mabote_5dias_final.csv")
    df["Data"] = pd.to_datetime(df["Data"]); df["dia"] = df["Data"].dt.date
    return df
df = carregar()
dias = sorted(df["dia"].unique())
clima_dia = df.groupby("dia")["Tipo_Clima"].first()
clima = df["Tipo_Clima"].values
E_RUIM = df.loc[clima=="Ruim","Demanda_Comunidade_kW"].values.sum()
VENTO_SERIE = df["Velocidade_Vento_m_s"].values

C = {"sol":"#FDE047","bat":"#4ADE80","falt":"#F87171","dem":"#FFFFFF","soc":"#C084FC","max":"#38BDF8"}

S_SHAPE=[1,1,1,1,1,1,1.3,1.6,1.6,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.4,1.3,1.3,1.2,1.2,1.1,1,1]
E_SHAPE=[.3,.3,.3,.3,.3,.3,.6,1,1.6,2,2.2,2.2,2.2,2,1.8,1.5,1.2,1.4,1.6,1.4,1,.7,.5,.4]
PERFIS = ["Mabote — medido (real)","Mabote +30% (crescimento / moagem)",
          "Centro de saúde (24 h)","Escola + uso produtivo"]

def vetor_demanda(perfil):
    if perfil == PERFIS[0]: return df["Demanda_Comunidade_kW"].values
    if perfil == PERFIS[1]: return df["Demanda_Comunidade_kW"].values*1.3
    shape,kwh = (S_SHAPE,60) if "saúde" in perfil else (E_SHAPE,80)
    return np.tile(np.array(shape)/sum(shape)*kwh, len(df)//24)

CENARIOS = {
    "Medido em Mabote (sem alteração)": (1.0, 1.0, 1.0),
    "Ciclone / tempestade (radiação -50%, vento x2.5)": (0.5, 2.5, 1.0),
    "Calmaria prolongada (vento x0.3)": (1.0, 0.3, 1.0),
    "Pico de calor (demanda +20%)": (1.0, 1.0, 1.2),
}
F_SOL, F_VEN, F_DEM = 1.0, 1.0, 1.0
USAR_MED, V_MAN = True, 2.0

# ══════════════════════ MODELO FÍSICO ══════════════════════
def simular(pv, bat_kwh, dem):
    G  = df["Radiacao_Solar_W_m2"].values*F_SOL
    Ta = df["Temperatura_C"].values
    v  = (VENTO_SERIE*F_VEN) if USAR_MED else np.full(len(dem), V_MAN)*F_VEN
    fc = 9.5/(5.7+3.8*np.clip(v,0,15))
    Tc = Ta + 25.0*(G/800.0)*fc
    der = np.clip(1-0.004*(Tc-25), 0.7, 1.0)
    sol = pv*(G/1000.0)*0.97*der
    cap, soc = bat_kwh, bat_kwh*0.9
    ds_h,db_h,un_h,soc_h,des_h = [],[],[],[],[]
    for t in range(len(dem)):
        d, g = dem[t], sol[t]
        if g >= d:
            ds,db,un = d, 0, 0
            surplus = g-d
            stored = min(surplus*0.92, cap-soc)
            soc += stored
            des = surplus - stored/0.92
        else:
            ds = g; need = d-g
            db = min(need, soc*0.95); soc -= db/0.95; un = need-db
            des = 0.0
        ds_h.append(ds); db_h.append(db); un_h.append(un); soc_h.append(soc); des_h.append(des)
    r = {k:np.array(vv) for k,vv in dict(ds=ds_h,db=db_h,un=un_h,soc=soc_h,des=des_h).items()}
    r.update(sol=sol, risco=100*r["un"].sum()/dem.sum())
    return r

def metricas(r, dem, bat):
    rb = 100*r["un"][clima=="Bom"].sum()/dem[clima=="Bom"].sum()
    rr = 100*r["un"][clima=="Ruim"].sum()/dem[clima=="Ruim"].sum()
    pior = max(100*r["un"][df["dia"]==d].sum()/dem[df["dia"]==d].sum() for d in dias)
    aut = 0.8*bat/dem.mean() if dem.mean() > 0 else 0.0
    soc_f = 100*r["soc"][-1]/bat if bat > 0 else 0.0
    gen = r["sol"].sum()
    util = 100*(1 - r["des"].sum()/max(gen,1e-9))
    return dict(risco=r["risco"], rb=rb, rr=rr, pior=pior, aut=aut, soc_f=soc_f,
                util=util, S=max(0, round(100-2*rr-rb)))

# ══════════════════════ CABEÇALHO ══════════════════════
logo_b64, emerge_b64 = img_b64("logo.png"), img_b64("emerge.png")
logo_html   = f'<img src="data:image/png;base64,{logo_b64}" class="hdr-img light">' if logo_b64 else '<div class="hdr-logo">R</div>'
emerge_html = f'<img src="data:image/png;base64,{emerge_b64}" class="hdr-img">' if emerge_b64 else '<span class="badge">EMERGE</span>'

st.markdown(f"""
<div class="hdr">
  {logo_html}
  <div><div class="hdr-title">RESILIA <span>MZ</span></div>
  <div class="hdr-sub">Simulação off-grid solar + bateria · optimização para resiliência · dados de Mabote, Inhambane</div></div>
  <div class="hdr-badges">
    <span class="badge gold">HACKATHON — Southern Africa | Mozambique</span>
    <span class="badge">13 Ago 2026 · UEM — Faculdade de Ciências</span>
    <span class="badge">Grupo 36</span>
  </div>
  {emerge_html}
</div>""", unsafe_allow_html=True)

# ══════════════════════ PAINEL ══════════════════════
with st.sidebar:
    st.markdown("### Painel de controlo")
    st.caption("Entradas exigidas pelo desafio")
    pv  = st.slider("Solar (kWp)", 0, 60, 8)
    usar_vento_med = st.checkbox("Usar vento medido hora a hora (Mabote)", value=True)
    if usar_vento_med:
        USAR_MED, V_MAN = True, 2.0
        st.caption("Vento actual: série medida (0,8–4,2 m/s). Entra como factor térmico dos painéis — não gera energia.")
    else:
        USAR_MED = False
        V_MAN = st.slider("Vento ambiente (m/s)", 0.0, 10.0, 2.0, 0.5)
        st.caption("Vento manual: testa calmaria (0–1 m/s) ou vento forte (6–10 m/s) e vê o efeito no blackout.")
    bat = st.slider("Capacidade da bateria (kWh)", 0, 400, 60, 10)
    perfil = st.radio("Perfil de demanda", PERFIS)
    st.divider()
    st.markdown("#### Cenário climático (stress test)")
    cenario = st.radio("Evento extremo", list(CENARIOS))
    F_SOL, F_VEN, F_DEM = CENARIOS[cenario]
    st.divider()
    st.caption("Decisão de projecto: o vento medido em Mabote é demasiado fraco para gerar (<10% de capacidade); entra no modelo apenas como arrefecimento dos painéis.")

dem = vetor_demanda(perfil)*F_DEM
r = simular(pv, bat, dem)
m_at = metricas(r, dem, bat)

c1,c2,c3,c4 = st.columns(4)
with c1: card("Risco de blackout", f"{m_at['risco']:.0f}%", "média dos 5 dias", C["falt"])
with c2: card("Risco em dias bons", f"{m_at['rb']:.0f}%", "dias 1–3 (medidos)", C["sol"])
with c3: card("Risco em dias ruins", f"{m_at['rr']:.0f}%", "dias 4–5 (medidos)", C["max"])
with c4: card("Índice de resiliência", f"{m_at['S']}/100", "ponderação 2:1 dias ruins", C["bat"])

# ══════════════════════ GRÁFICOS ══════════════════════
def base(fig, titulo):
    fig.update_layout(template="plotly_dark", plot_bgcolor="#08170E",
        paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#FFFFFF", size=13),
        title=dict(text=titulo, font=dict(size=16, color="#FFFFFF")),
        legend=dict(orientation="h", y=1.18, traceorder="reversed", font=dict(size=13, color="#FFFFFF")),
        margin=dict(t=110), hovermode="x unified",
        xaxis=dict(gridcolor="#1F5233", tickfont=dict(size=12, color="#FFFFFF")),
        yaxis=dict(gridcolor="#1F5233", tickfont=dict(size=12, color="#FFFFFF")))
    return fig

def grafico_balanco(x, dem_x, r_x, titulo, vrect=False, marc=True):
    fig = go.Figure()
    fig.add_trace(go.Bar(x=x, y=r_x["ds"], name="Solar", marker_color=C["sol"],
                marker_line=dict(color="#05130C", width=1)))
    fig.add_trace(go.Bar(x=x, y=r_x["db"], name="Bateria", marker_color=C["bat"],
                marker_line=dict(color="#05130C", width=1)))
    fig.add_trace(go.Bar(x=x, y=r_x["un"], name="Não servida (blackout)", marker_color=C["falt"],
                marker_line=dict(color="#05130C", width=1)))
    fig.add_trace(go.Scatter(x=x, y=dem_x, name="Demanda da comunidade",
                mode="lines+markers" if marc else "lines",
                line=dict(color=C["dem"], width=3),
                marker=dict(size=6, symbol="circle-open", color=C["dem"])))
    fig.update_layout(barmode="stack", yaxis_title="Energia (kWh)")
    if vrect:
        fig.add_vrect(x0=71.5, x1=119.5, fillcolor=C["falt"], opacity=0.12, line_width=0,
                      annotation_text="Dias ruins (medidos)", annotation_position="top left",
                      annotation_font_color="#FFFFFF", annotation_font_size=12)
        fig.update_xaxes(tickvals=[0,24,48,72,96], ticktext=["Dia 1 (bom)","Dia 2 (bom)","Dia 3 (bom)","Dia 4 (ruim)","Dia 5 (ruim)"])
    return base(fig, titulo)

def grafico_falta(x, un_x, titulo, vrect=False):
    fig = go.Figure(go.Bar(x=x, y=un_x, name="Energia não servida", marker_color=C["falt"],
                 marker_line=dict(color="#7F1D1D", width=1)))
    fig.update_layout(yaxis_title="kWh não fornecidos")
    if np.max(un_x) <= 0:
        fig.add_annotation(x=0.5, y=1.0, xref="paper", yref="paper", showarrow=False,
            text="Sem défices — demanda 100% atendida", font=dict(color=C["bat"], size=14))
    if vrect:
        fig.add_vrect(x0=71.5, x1=119.5, fillcolor=C["falt"], opacity=0.12, line_width=0)
        fig.update_xaxes(tickvals=[0,24,48,72,96], ticktext=["Dia 1","Dia 2","Dia 3","Dia 4","Dia 5"])
    return base(fig, titulo)

def grafico_soc(x, r_x, cap, titulo, vrect=False):
    fig = go.Figure(go.Scatter(x=x, y=r_x["soc"], mode="lines", fill="tozeroy",
                name="Energia armazenada", line=dict(color=C["soc"], width=2.5),
                fillcolor="rgba(192,132,252,.35)"))
    if cap > 0:
        fig.add_hline(y=0.2*cap, line_dash="dash", line_color="#FFFFFF", opacity=0.8,
            annotation_text="reserva mínima (20%)", annotation_position="bottom right",
            annotation_font_color="#FFFFFF", annotation_font_size=11)
    fig.update_layout(yaxis_title="kWh armazenados")
    if vrect:
        fig.add_vrect(x0=71.5, x1=119.5, fillcolor=C["falt"], opacity=0.12, line_width=0)
        fig.update_xaxes(tickvals=[0,24,48,72,96], ticktext=["Dia 1","Dia 2","Dia 3","Dia 4","Dia 5"])
    return base(fig, titulo)

GUIA = ('<div class="explain"><b>Guia de cores (válida em todos os gráficos):</b> '
        'amarelo = solar · verde = bateria · vermelho = energia não servida (blackout) · '
        'linha branca = demanda da comunidade · violeta = energia armazenada. '
        'O vento (m/s) não gera energia: arrefece os painéis e modula a barra amarela.</div>')

# ══════════════════════ ABAS ══════════════════════
t0,t1,t2,t3,t4 = st.tabs(["Contexto e objectivo","Balanço 24 h","Resiliência (5 dias)",
                          "Optimização resiliente","Base técnica"])

with t0:
    st.markdown("#### Desafio")
    st.markdown('''<div style="background:#0C2115;border:1px solid #24583B;border-radius:12px;
      padding:16px 20px;font-size:14px;color:#FFFFFF">
      <b>Task:</b> construir um modelo de simulação que mostre como um sistema off-grid equilibra
      oferta e demanda ao longo de 24 horas.<br>
      <b>Deliverable:</b> ferramenta simples com entradas (solar, vento, capacidade da bateria, perfil de demanda)
      e saídas (balanço energético, risco de blackout).<br>
      <b>Twist:</b> optimizar para <b>resiliência</b>, não apenas eficiência.</div>''', unsafe_allow_html=True)
    st.markdown("#### Objectivo do trabalho")
    st.markdown("""O RESILIA MZ dimensiona um sistema off-grid **solar + bateria** para Mabote (Inhambane), **dados horários reais**. Decisão de projecto baseada nos dados: o vento medido (0,8–4,2 m/s) entra como **input ambiental em m/s**, actuando na temperatura dos painéis
    (vento arrefece → mais produção; calmaria + calor → até ~15% menos produção → mais blackout). O dimensionamento
    segue **optimização hierárquica**: resiliência obrigatória, eficiência técnica como desempate.""")
    
    st.markdown("#### Correspondência entre Desafio e a ferramenta")
    st.table(pd.DataFrame({
        "Exigência":["Entradas (solar, vento, bateria, perfil)","Balanço oferta × demanda em 24 h",
            "Risco de blackout","Twist: optimizar para resiliência","Modelo em folha de cálculo"],
        "Implementação no RESILIA MZ":["Painel lateral: solar (kWp), vento ambiente (m/s), bateria (kWh),",
            "Aba «Balanço 24 h», resolução horária 00–23 h",
            "Indicadores no topo + gráfico dedicado de energia não servida",
            "Aba «Optimização resiliente»: resiliência obrigatória, eficiência como desempate",
            "Exportação XLSX (abre no Excel)"]}))

    st.markdown("#### Sustentabilidade e replicação")
    st.markdown("""**Sustentabilidade:** ferramenta gratuita para comunidades e ONGs; parcerias institucionais
    (UEM, FUNAE, projecto EMERGE) para manutenção, dados e expansão; código aberto.
    **Replicação:** o modelo só necessita de cinco colunas (data, hora, radiação, temperatura/vento, demanda),
    recolhíveis com uma estação meteorológica básica e um medidor de carga.""")

with t1:
    st.markdown('<div class="okbox">Esta aba responde à tarefa central do desafio: o equilíbrio oferta–demanda em 24 horas.</div>', unsafe_allow_html=True)
    st.markdown(GUIA, unsafe_allow_html=True)
    i = st.radio("Dia de simulação", range(5), horizontal=True,
                 format_func=lambda i: f"Dia {i+1} ({clima_dia[dias[i]].lower()})")
    m = (df["dia"]==dias[i]).values
    r_d = {k: v[m] for k, v in r.items() if isinstance(v, np.ndarray)}
    st.plotly_chart(grafico_balanco(df.loc[m,"Hora"], dem[m], r_d, f"Balanço oferta × demanda — Dia {i+1}"), use_container_width=True)
    explicar("Leitura do gráfico", "as barras empilhadas mostram a fonte que abastece cada hora (solar ou bateria); a linha "
        "branca é o que a comunidade pediu. Onde as barras não alcançam a linha, a diferença aparece a vermelho (blackout).")
    st.plotly_chart(grafico_falta(df.loc[m,"Hora"], r_d["un"], f"Energia não servida (blackout) — Dia {i+1}"), use_container_width=True)
    explicar("Leitura do blackout", "cada barra vermelha é energia pedida e não entregue naquela hora; sem barras vermelhas, não há blackout.")
    st.plotly_chart(grafico_soc(df.loc[m,"Hora"], r_d, bat, "Estado de carga da bateria — 24 h"), use_container_width=True)
    explicar("Leitura da bateria", "a curva violeta sobe com o excedente diurno e desce à noite; "
        "abaixo da linha tracejada (reserva mínima), o sistema entra em zona de risco.")
    explicar("Efeito do vento", "desliga «vento medido» e compara 0,5 m/s (calmaria quente) com 8 m/s: a barra amarela "
        "muda vários % e as horas vermelhas podem aparecer ou desaparecer — o vento move o blackout sem gerar um único kWh.")

with t2:
    st.markdown(GUIA, unsafe_allow_html=True)
    st.plotly_chart(grafico_balanco(list(range(120)), dem, r, "Balanço oferta × demanda — 120 h (Mabote)", vrect=True, marc=False), use_container_width=True)
    explicar("Porquê cinco dias", "o balanço de 24 h cumpre o enunciado; a resiliência só se revela em dias consecutivos. "
        "Na faixa destacada (dias ruins medidos), um sistema resiliente mantém as barras à altura da linha branca.")
    ca1,ca2,ca3 = st.columns(3)
    with ca1: card("Autonomia da bateria", f"{m_at['aut']:.0f} h", "sem geração, descarga útil de 80%", C["bat"])
    with ca2: card("Cobertura no pior dia", f"{100-m_at['pior']:.0f}%", "pior dia medido (clima ruim)", C["max"])
    with ca3: card("Reserva final (SOC)", f"{m_at['soc_f']:.0f}%", "após os 5 dias simulados", C["soc"])
    st.plotly_chart(grafico_falta(list(range(120)), r["un"], "Energia não servida — 5 dias", vrect=True), use_container_width=True)
    st.plotly_chart(grafico_soc(list(range(120)), r, bat, "Estado de carga — 5 dias", vrect=True), use_container_width=True)
    st.table(pd.DataFrame({"Dia":[f"Dia {i+1}" for i in range(5)], "Clima":[clima_dia[d] for d in dias],
        "Demanda (kWh)":[round(dem[df['dia']==d].sum()) for d in dias],
        "Risco de blackout (%)":[round(100*r['un'][df['dia']==d].sum()/dem[df['dia']==d].sum()) for d in dias]}))

with t3:
    st.markdown('<div class="okbox">Como o twist é aplicado: optimização <b>hierárquica</b>. 1.º — resiliência: só concorrem configurações que cumprem os critérios abaixo. 2.º — eficiência técnica: entre as resilientes, vence a de menor dimensão instalada. Sem valores monetários: apenas física e confiabilidade.</div>', unsafe_allow_html=True)
    st.markdown("#### 1. Critérios de resiliência (definidos pelo planificador)")
    cc1, cc2 = st.columns(2)
    with cc1: rmax = st.slider("Risco máximo aceitável em dias ruins (%)", 0, 50, 10)
    with cc2: autmin = st.slider("Autonomia mínima da bateria (h)", 0, 48, 12)

    st.markdown("#### 2. Espaço de soluções avaliado e selecção")
    rows=[]
    for p in [8,12,16,22,30,40,50]:
        for b in [0,40,80,140,220,320,420]:
            rr = simular(p,b,dem)
            rows.append(dict(p=p,b=b,dim=p+b/10,**metricas(rr,dem,b)))
    d = pd.DataFrame(rows)
    ok_m = (d["rr"]<=rmax) & (d["aut"]>=autmin)

    ef = d[d["rb"]<=10].sort_values("dim").iloc[0]
    res_ok = d[ok_m]
    re_ = res_ok.sort_values("dim").iloc[0] if len(res_ok) else d.sort_values("rr").iloc[0]
    mr = d.sort_values(["rr","dim"]).iloc[0]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=d[~ok_m]["dim"], y=d[~ok_m]["rr"], mode="markers",
        name="Não cumpre resiliência", marker=dict(color="#94A3B8", size=9, opacity=0.8)))
    fig.add_trace(go.Scatter(x=d[ok_m]["dim"], y=d[ok_m]["rr"], mode="markers",
        name="Cumpre resiliência", marker=dict(color=C["bat"], size=9)))
    for sol,cor,nome in [(ef,"#CBD5E1","Só eficiência"),(re_,C["sol"],"Resiliente (proposta)"),(mr,C["max"],"Máx. resiliência")]:
        fig.add_trace(go.Scatter(x=[sol["dim"]], y=[sol["rr"]], mode="markers+text", name=nome,
            marker=dict(color=cor, size=18, symbol="star", line=dict(color="#FFFFFF", width=1)),
            text=[nome], textposition="top center", textfont=dict(color=cor, size=12)))
    fig.update_layout(xaxis_title="Índice de dimensão do sistema (kWp + kWh/10)",
        yaxis_title="Risco em dias ruins (%)",
        legend=dict(orientation="h", y=1.22, font=dict(size=12, color="#FFFFFF")), margin=dict(t=110))
    st.plotly_chart(base(fig, "Espaço de soluções: dimensão versus risco nos dias ruins"), use_container_width=True)
    explicar("Leitura do gráfico",
        "cada ponto é um dimensionamento solar+bateria simulado; os verdes cumprem os critérios, os cinzentos falham nos "
        "dias ruins. A estrela clara é a opção só eficiência (pequena, arriscada); a amarela é a proposta resiliente "
        "(a mais pequena entre as que cumprem); a ciano é a máxima resiliência.")

    if not len(res_ok):
        st.markdown('<div class="warnbox">Nenhuma configuração cumpre simultaneamente os dois critérios nesta grelha; a apresentar a de menor risco nos dias ruins.</div>', unsafe_allow_html=True)

    st.markdown("#### 3. Comparação das soluções de referência")
    k1,k2,k3 = st.columns(3)
    with k1: card("Só eficiência", f"dim. {ef['dim']:.0f}",
        f"solar {ef['p']:.0f} · bat. {ef['b']:.0f} — risco ruim {ef['rr']:.0f}%", "#CBD5E1")
    with k2: card("Resiliente — proposta", f"dim. {re_['dim']:.0f}",
        f"solar {re_['p']:.0f} · bat. {re_['b']:.0f} — risco ruim {re_['rr']:.0f}%", C["sol"])
    with k3: card("Máxima resiliência", f"dim. {mr['dim']:.0f}",
        f"solar {mr['p']:.0f} · bat. {mr['b']:.0f} — risco ruim {mr['rr']:.0f}%", C["max"])

    tab_cmp = pd.DataFrame({
        "Métrica":["Solar (kWp)","Bateria (kWh)","Índice de dimensão",
            "Eficiência de utilização (%)","Risco dias bons (%)","Risco dias ruins (%)",
            "Risco no pior dia (%)","Autonomia (h)","Índice de resiliência"],
        "Só eficiência":[ef['p'],ef['b'],round(ef['dim']),round(ef['util']),round(ef['rb']),round(ef['rr']),round(ef['pior']),round(ef['aut']),ef['S']],
        "Resiliente (proposta)":[re_['p'],re_['b'],round(re_['dim']),round(re_['util']),round(re_['rb']),round(re_['rr']),round(re_['pior']),round(re_['aut']),re_['S']],
        "Máx. resiliência":[mr['p'],mr['b'],round(mr['dim']),round(mr['util']),round(mr['rb']),round(mr['rr']),round(mr['pior']),round(mr['aut']),mr['S']]})
    st.table(tab_cmp)

    delta = re_["dim"]-ef["dim"]
    ens_ef, ens_re = ef["rr"]/100*E_RUIM, re_["rr"]/100*E_RUIM
    st.markdown(f"""<div class="explain"><b>Veredicto quantitativo:</b> a solução puramente eficiente exige menos
        capacidade instalada (índice {ef['dim']:.0f}), mas deixa cerca de {ens_ef:.0f} kWh por entregar nos dias ruins.
        A solução resiliente (proposta), com índice {re_['dim']:.0f} (+{delta:.0f}), limita a perda a {ens_re:.0f} kWh.
        Resiliência primeiro; eficiência a seguir.</div>""", unsafe_allow_html=True)

with t4:
    st.markdown("#### 1. Metodolgia utilizada por nos")
    st.table(pd.DataFrame({
        "Etapa":["1. Dados de campo","2. Calibração térmica","3. Simulação horária","4. Métricas",
                 "5. Optimização hierárquica","6. Visualização e exportação"],
        "O que fizemos":[
            "120 horas medidas em Mabote (radiação, temperatura, vento, demanda, clima)",
            "Painel de 8 kWp inferido dos dados; perdas eléctricas 3%; γ = -0,4%/°C; vento arrefece a célula",
            "Balanço hora a hora: solar + bateria, com perdas de carga (8%) e descarga (5%)",
            "Risco de blackout, autonomia, eficiência de utilização e índice de resiliência S",
            "1.º resiliência (restrições obrigatórias); 2.º eficiência (menor dimensão instalada)",
            "Cada equação gera directamente um elemento visual; relatório XLSX com as 120 horas"],
        "Onde aparece":[
            "Todas as abas (base de dados Mabote)",
            "Secção 2 desta aba (equações 1 e 2)",
            "Abas «Balanço 24 h» e «Resiliência (5 dias)»",
            "Cartões no topo e tabelas por dia",
            "Aba «Optimização resiliente»",
            "Gráficos de todas as abas + botão «Exportar XLSX»"]}))

    st.markdown("#### 2. As equações do modelo (formas práticas calibradas)")
    st.markdown("""O sistema é **off-grid solar + bateria**: o vento não gera energia; entra em m/s como factor
    térmico dos painéis. As formas completas ficam nas referências APA no fim desta aba.""")

    st.markdown("##### Equação 1 — Energia solar da hora (com temperatura)")
    st.latex(r"E_{sol}=P_{sol}\cdot\frac{G}{1000}\cdot 0{,}97\cdot\left[1+\gamma\,(T_c-25)\right]")
    st.markdown(r"""$\gamma=-0{,}004\ \mathrm{°C^{-1}}$ (silício); 0,97 = perdas eléctricas/sujeira.
    **Alimenta:** barras amarelas. *(Duffie & Beckman, 2020; Dobos, 2014).*""")

    st.markdown("##### Equação 2 — O vento entra aqui: temperatura da célula")
    st.latex(r"T_c=T_a+(NOCT-20)\cdot\frac{G}{800}\cdot\frac{9{,}5}{5{,}7+3{,}8\,v}")
    st.markdown(r"""com $NOCT=45$ °C e $v$ = vento (m/s). O factor $\frac{9{,}5}{5{,}7+3{,}8v}$ é a correcção de vento:
    calmaria → painel quente → até ~15% menos produção → mais blackout; vento → painel fresco → produção recupera.
    **Alimenta:** modula as barras amarelas e, indirectamente, o vermelho do blackout. *(Skoplaki & Palyvos, 2009).*""")

    st.markdown("##### Equação 3 — Bateria de uma hora para a outra")
    st.latex(r"B_{t+1}=B_{t}+0{,}92\cdot E_{entra}-\frac{E_{sai}}{0{,}95}")
    st.markdown("""**Alimenta:** curva violeta do estado de carga (SOC), com linha de reserva mínima. *(Reddy, 2011).*""")

    st.markdown("##### Equação 4 — Balanço de cada hora e risco de blackout")
    st.latex(r"Falta=\max\big(0,\;\; Demanda-(E_{sol}+B_{disponível})\big)")
    st.latex(r"Risco\ (\%)=\frac{\sum Falta}{\sum Demanda}\times 100")
    st.markdown("""**Alimenta:** barras vermelhas (energia não servida), gráfico dedicado de blackout e cartões de risco.
    *(Billinton & Allan, 1996).*""")

    st.markdown("##### Equação 5 — Resiliência em dois números")
    st.latex(r"Autonomia=\frac{0{,}8\cdot Bateria}{consumo\ médio\ por\ hora}\qquad\qquad S=100-(2\cdot R_{ruim}+R_{bom})")
    st.markdown("""**Alimenta:** cartões de autonomia e índice S; o peso duplo nos dias ruins traduz o conceito de
    resiliência (Holling, 1973) aplicado a sistemas eléctricos (International Energy Agency, 2021).""")

    st.markdown("##### Equação 6 — Escolha da melhor configuração")
    st.markdown("""1.º — **Resiliência:** eliminar configurações com risco acima do limite nos dias ruins ou autonomia abaixo do mínimo;
    2.º — **Eficiência:** entre as que sobram, escolher a de menor equipamento instalado (painéis + bateria).
    **Alimenta:** as três estrelas do gráfico da aba «Optimização resiliente». Filosofia análoga à do HOMER (Lambert et al., 2006).""")

    st.markdown("#### 3. Da equação ao gráfico (resumo visual)")
    st.table(pd.DataFrame({
        "Equação":["1 — E_sol","2 — T_c (vento)","3 — B_t+1","4 — Falta / Risco","5 — Autonomia / S"],
        "Elemento gerado no gráfico":[
            "Barras amarelas (solar directo)",
            "Modulação das barras amarelas (arrefecimento dos painéis)",
            "Curva violeta (estado de carga da bateria)",
            "Barras vermelhas (blackout) + cartões de risco",
            "Cartões de autonomia/resiliência e estrelas da optimização"]}))

    st.markdown("#### 4. Referências (norma APA, 7.ª edição)")
    st.markdown("""- Billinton, R., & Allan, R. N. (1996). *Reliability evaluation of power systems* (2.ª ed.). Springer. https://doi.org/10.1007/978-1-4899-1860-4
- Dobos, A. P. (2014). *PVWatts version 5 manual* (NREL/TP-6A20-62641). National Renewable Energy Laboratory. https://doi.org/10.2172/1158307
- Duffie, J. A., & Beckman, W. A. (2020). *Solar engineering of thermal processes* (5.ª ed.). John Wiley & Sons.
- Holling, C. S. (1973). Resilience and stability of ecological systems. *Annual Review of Ecology and Systematics, 4*(1), 1–23. https://doi.org/10.1146/annurev.es.04.110173.000245
- International Energy Agency. (2021). *Power systems in transition*. IEA. https://www.iea.org/reports/power-systems-in-transition
- International Energy Agency, International Renewable Energy Agency, United Nations, World Bank, & World Health Organization. (2023). *Tracking SDG 7: The energy progress report 2023*. World Bank. https://doi.org/10.1596/978-1-4648-1993-3
- Lambert, T., Gilman, P., & Lilienthal, E. (2006). Micropower system modeling with HOMER. In F. A. Farret & M. G. Simões (Eds.), *Integration of alternative sources of energy* (pp. 379–395). John Wiley & Sons. https://doi.org/10.1002/0471755621.ch15
- Reddy, T. B. (Ed.). (2011). *Linden's handbook of batteries* (4.ª ed.). McGraw-Hill.
- Skoplaki, E., & Palyvos, J. A. (2009). On the temperature dependence of photovoltaic module electrical performance: A review of simplifying correlations and models. *Solar Energy, 83*(5), 614–624. https://doi.org/10.1016/j.solener.2008.10.008""")

    st.markdown("""##### Suposições e limites
Passo de 1 h; despacho sem previsão; bateria inicia a 90%; cinco dias de medições como prova de conceito
(roadmap: um ano de dados e extensão aos demosites EMERGE — Marrocos e Níger).""")

# ══════════════════════ EXPORTAÇÃO XLSX ══════════════════════
out = pd.DataFrame({"hora":df["Hora"],"clima":clima,"demanda_kWh":dem,"solar_kWh":r["sol"],
                    "bateria_kWh":r["db"],"nao_servida_kWh":r["un"],"desperdicada_kWh":r["des"],"soc_kWh":r["soc"]})
res_dias = pd.DataFrame({"Dia":[f"Dia {i+1}" for i in range(5)], "Clima":[clima_dia[d] for d in dias],
    "Demanda (kWh)":[round(dem[df['dia']==d].sum(),1) for d in dias],
    "Risco de blackout (%)":[round(100*r['un'][df['dia']==d].sum()/dem[df['dia']==d].sum(),1) for d in dias]})

buf = io.BytesIO()
with pd.ExcelWriter(buf, engine="openpyxl") as w:
    out.to_excel(w, sheet_name="Balanco_120h", index=False)
    res_dias.to_excel(w, sheet_name="Resumo_por_dia", index=False)
    tab_cmp.to_excel(w, sheet_name="Solucoes_referencia", index=False)

st.download_button("Exportar relatório XLSX (abre no Excel)", buf.getvalue(),
                   "resilia_mabote.xlsx",
                   mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

st.markdown(
    '<div class="foot">RESILIA MZ — Grupo 36 · Ezequias Miocha, Laura Hele, Suely Muando · '
    'Projecto EMERGE (HORIZON, GA 101118278) · UEM — Faculdade de Ciências, 13 de Agosto de 2026</div>',
    unsafe_allow_html=True)