import streamlit as st
import pandas as pd
from datetime import datetime
import os

# -----------------------------------------------------------------------------
# 1. 頁面設定與自訂高中生潮流 CSS 樣式
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Rich Teen 財商培力戰情室",
    page_icon="🚀",
    layout="wide"
)

# 注入自訂 CSS，讓介面具備圓角卡片與現代色彩感
st.markdown("""
<style>
    .stApp { background-color: #F8F9FA; }
    .card {
        background-color: #FFFFFF;
        border-radius: 16px;
        padding: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    .badge-asset { background-color: #E8F5E9; color: #2E7D32; padding: 4px 8px; border-radius: 8px; font-weight: bold; }
    .badge-liab { background-color: #FFEBEE; color: #C62828; padding: 4px 8px; border-radius: 8px; font-weight: bold; }
    .stat-title { font-size: 14px; color: #6C757D; margin-bottom: 5px; }
    .stat-value { font-size: 24px; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

CSV_FILE = "financial_records.csv"

if not os.path.exists(CSV_FILE):
    df_init = pd.DataFrame(columns=["日期", "項目名稱", "金額", "財務類別", "細項標籤", "備註"])
    df_init.to_csv(CSV_FILE, index=False, encoding="utf-8-sig")

def load_data():
    return pd.read_csv(CSV_FILE, encoding="utf-8-sig")

def save_data(df):
    df.to_csv(CSV_FILE, index=False, encoding="utf-8-sig")

def add_record(item, amt, cat, tag, note=""):
    df = load_data()
    new_row = pd.DataFrame({
        "日期": [datetime.now().strftime("%Y-%m-%d")],
        "項目名稱": [item],
        "金額": [amt],
        "財務類別": [cat],
        "細項標籤": [tag],
        "備註": [note]
    })
    df = pd.concat([df, new_row], ignore_index=True)
    save_data(df)

# -----------------------------------------------------------------------------
# 2. 頁面標題與遊戲化財商等級（FQ Rank）
# -----------------------------------------------------------------------------
df_data = load_data()

total_inc = df_data[df_data["財務類別"] == "收入"]["金額"].sum() if not df_data.empty else 0
total_ast = df_data[df_data["財務類別"] == "資產(投資自己)"]["金額"].sum() if not df_data.empty else 0
total_lia = df_data[df_data["財務類別"] == "負債(慾望消費)"]["金額"].sum() if not df_data.empty else 0

# 計算財商稱號
asset_ratio = (total_ast / total_inc * 100) if total_inc > 0 else 0
if asset_ratio >= 40:
    rank_title, rank_color = "💎 財商大師（資產大亨）", "success"
elif asset_ratio >= 20:
    rank_title, rank_color = "🛡️ 自主學習者（穩健積累）", "info"
else:
    rank_title, rank_color = "🐭 賽跑新手（小心負債陷阱）", "warning"

st.title("🚀 Rich Teen 財商培力戰情室")
st.caption("用 AI 打造的專屬財商系統 ｜ 翻轉記帳邏輯：讓每一筆消費都成為未來的資產！")

# 顯示遊戲化稱號 Header
col_rank1, col_rank2 = st.columns([2, 1])
with col_rank1:
    st.subheader(f"當前財商稱號：{rank_title}")
    st.progress(min(int(asset_ratio), 100), text=f"資產累積率：{asset_ratio:.1f}% （目標 30% 以上）")

# -----------------------------------------------------------------------------
# 3. 高中生專屬快捷記帳區（Express Preset Buttons）
# -----------------------------------------------------------------------------
st.markdown("### ⚡ 快捷一鍵記帳（高中生日常高頻項目）")
q1, q2, q3, q4, q5 = st.columns(5)

if q1.button("🧋 珍奶/手搖 ($65)"):
    add_record("珍珠奶茶", 65, "負債(慾望消費)", "飲料/零食", "課後娛樂需求")
    st.toast("已記錄：珍奶 $65（分類：負債 💸）")
    st.rerun()

if q2.button("📚 程式/參考書 ($350)"):
    add_record("專業書籍/教材", 350, "資產(投資自己)", "知識學習", "自主學習能力投資")
    st.toast("成功投資自己 $350（分類：資產 🪙）")
    st.rerun()

if q3.button("🎮 遊戲儲值 ($300)"):
    add_record("遊戲月卡/抽卡", 300, "負債(慾望消費)", "數位娛樂", "課業紓壓")
    st.toast("已記錄：遊戲儲值 $300（分類：負債 💸）")
    st.rerun()

if q4.button("🚌 公車/捷運 ($30)"):
    add_record("交通車資", 30, "必要支出", "通勤開銷", "基本日常需求")
    st.toast("已記錄：交通費 $30（分類：必要支出 🚌）")
    st.rerun()

if q5.button("💵 發零用錢 ($2000)"):
    add_record("本月零用錢", 2000, "收入", "固定零用錢", "領取零用錢")
    st.toast("收入增加 $2,000！")
    st.rerun()

st.markdown("---")

# -----------------------------------------------------------------------------
# 4. 主功能分頁：戰情儀表板 / 詳細手動輸入 / 歷史報表
# -----------------------------------------------------------------------------
tab_dashboard, tab_input, tab_history = st.tabs(["📊 財商戰情室", "✍️ 自訂輸入", "📜 財務報表明細"])

with tab_dashboard:
    if df_data.empty:
        st.info("👋 歡迎！請使用上方【快捷記帳】或前往【自訂輸入】建立你的第一筆財務紀錄。")
    else:
        total_exp = df_data[df_data["財務類別"] == "必要支出"]["金額"].sum()
        net_cash = total_inc - (total_ast + total_lia + total_exp)

        # 四大數據卡片
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("💵 總收入", f"${total_inc:,}")
        c2.metric("🪙 資產 (投資自己)", f"${total_ast:,}", delta=f"{asset_ratio:.1f}% 佔比")
        c3.metric("💸 負債 (慾望開銷)", f"${total_lia:,}", delta_color="inverse")
        c4.metric("💰 可用現金流", f"${net_cash:,}", delta="現金充裕" if net_cash >= 0 else "透支")

        st.markdown("<br>", unsafe_allow_html=True)
        
        # 視覺圖表與 AI 導師分析
        chart_col, ai_col = st.columns([3, 2])
        
        with chart_col:
            st.markdown("##### 📈 財務結構比例分析")
            chart_data = df_data.groupby("財務類別")["金額"].sum()
            st.bar_chart(chart_data, color="#4F46E5")

        with ai_col:
            st.markdown("##### 🤖 富爸爸 AI 簡明點評")
            if total_lia > total_ast:
                st.warning("⚠️ **負債大於資產！** 目前在慾望娛樂上的支出偏高，試著將下一次要買遊戲或手搖飲的錢，挪 100 元存入「線上課程/檢定報名費」的資產池中！")
            elif total_ast >= total_lia and total_ast > 0:
                st.success("🌟 **非常出色！** 你的資產累積超越了娛樂負債，正在逐步脫離「老鼠賽跑」循環！繼續保持自主學習的投資習慣。")
            else:
                st.info("💡 **小建議：** 設定「先支付給自己」的規則，每月一領到零用錢，先預留 20% 當作自我升級基金。")

with tab_input:
    st.subheader("📝 自訂財務紀錄")
    with st.form("custom_form", clear_on_submit=True):
        f_item = st.text_input("項目名稱", placeholder="例如：報名 APCS 檢定 / 買社團團服")
        f_amt = st.number_input("金額 (NTD)", min_value=1, value=100, step=10)
        f_cat = st.selectbox("財務類別（翻轉思維關鍵！）", [
            "資產(投資自己)", 
            "負債(慾望消費)", 
            "必要支出", 
            "收入"
        ])
        f_tag = st.text_input("分類標籤", placeholder="例如：課業學習、社團活動、零食")
        f_note = st.text_area("寫下這筆花費的理由或自我反省", placeholder="這筆消費能否在未來幫我產生價值？")
        
        btn_submit = st.form_submit_button("寫入戰情室")
        if btn_submit and f_item:
            add_record(f_item, f_amt, f_cat, f_tag, f_note)
            st.success(f"已記錄：{f_item} ${f_amt}")
            st.rerun()

with tab_history:
    st.subheader("📜 歷史資料紀錄簿")
    st.dataframe(df_data.sort_values(by="日期", ascending=False), use_container_width=True)