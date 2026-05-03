import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import random

# الرابط الخاص بك
API_URL = "https://google.com"
PASSWORD = "admin" 

st.set_page_config(page_title="Travel ERP Pro 2026", layout="wide")

# تصميم الفاتورة العصرية (Modern 2026)
st.markdown("""
    <style>
    @import url('https://googleapis.com');
    * { font-family: 'Cairo', sans-serif; direction: rtl; }
    .invoice-card { 
        background: white; border: 2px solid #002147; padding: 40px; border-radius: 15px; 
        box-shadow: 0 10px 30px rgba(0,0,0,0.1); direction: rtl; text-align: right; 
        max-width: 800px; margin: auto;
    }
    .money-badge { background: #f8f9fa; padding: 15px; border-radius: 10px; border-right: 10px solid #002147; margin: 15px 0; }
    </style>
""", unsafe_allow_html=True)

if "auth" not in st.session_state: st.session_state.auth = False
if not st.session_state.auth:
    col1, col2, col3 = st.columns(3)
    with col2:
        st.markdown("<h2 style='text-align:center;'>🔐 تسجيل الدخول</h2>", unsafe_allow_html=True)
        pwd = st.text_input("كلمة المرور", type="password")
        if st.button("دخول"):
            if pwd == PASSWORD: st.session_state.auth = True; st.rerun()
            else: st.error("❌ كلمة المرور غير صحيحة")
    st.stop()

tab1, tab2, tab3 = st.tabs(["📊 السجلات", "👤 إضافة عميل", "🔍 البحث والطباعة"])

with tab2:
    st.subheader("📝 تسجيل ملف جديد")
    with st.form("reg_form", clear_on_submit=True):
        c1, c2, c3 = st.columns(3)
        with c1:
            name = st.text_input("اسم العميل")
            passport = st.text_input("رقم الجواز")
            phone = st.text_input("الهاتف")
        with c2:
            nation = st.text_input("الجنسية")
            service = st.selectbox("المعاملة", ["دراسة", "عقد عمل", "سياحة"])
            branch = st.selectbox("الفرع", ["بيلاروسيا", "مصر"])
        with c3:
            staff = st.text_input("الموظف المضيف")
            total = st.number_input("إجمالي المبلغ ($)", min_value=0.0)
            paid = st.number_input("المدفوع ($)", min_value=0.0)

        if st.form_submit_button("حفظ المزامنة وإصدار التتبع ✅"):
            # توليد رقم تتبع عشوائي احترافي
            trk = f"TRK-{random.randint(100000, 999999)}-{branch[:2].upper()}"
            # نرسل البيانات الأساسية (سيتم ملء الفراغات في الشيت تلقائياً)
            row = [name, passport, phone, "", nation, "", service, "قيد المعالجة", "", str(datetime.now().date()), branch, staff, total, paid, trk]
            try:
                requests.post(API_URL, json=row)
                st.success(f"✅ تم الحفظ! رقم التتبع: {trk}")
            except: st.error("فشل في المزامنة")

with tab3:
    st.subheader("🔍 استخراج الفاتورة")
    search_q = st.text_input("ابحث عن اسم العميل أو رقم جواز السفر")
    if search_q:
        try:
            res = requests.get(API_URL).json()
            df = pd.DataFrame(res[1:], columns=res)
            # بحث مرن يتجاهل أسماء الأعمدة ويستخدم الترتيب
            match = df[df.iloc[:, 2].astype(str).str.contains(search_q) | df.iloc[:, 3].astype(str).str.contains(search_q)]
            
            if not match.empty:
                c = match.iloc[0]
                st.markdown(f"""
                <div class="invoice-card">
                    <table style="width:100%">
                        <tr>
                            <td style="text-align:right"><h1>🧾 فاتورة رسمية</h1></td>
                            <td style="text-align:left"><h2 style="color:#002147">{c.iloc[0]}</h2></td>
                        </tr>
                    </table>
                    <hr>
                    <p><b>السيد/ة:</b> {c.iloc[2]} | <b>الجواز:</b> {c.iloc[3]}</p>
                    <p><b>نوع الخدمة:</b> {c.iloc[8]} | <b>التاريخ:</b> {c.iloc[11]}</p>
                    <div class="money-badge">
                        <h3>💰 الحساب المالي:</h3>
                        <p>الإجمالي: {c.iloc[14]}$ | المدفوع: {c.iloc[15]}$</p>
                        <h2 style="color:#d32f2f">المتبقي: {c.iloc[16]}$</h2>
                    </div>
                    <p style="text-align:center;">رقم التتبع: {c.iloc[17]} | الباركود: {c.iloc[18]}</p>
                </div>
                """, unsafe_allow_html=True)
                st.button("🖨️ طباعة الفاتورة (Ctrl+P)")
            else: st.warning("⚠️ العميل غير موجود")
        except: st.error("تأكد من إدخال بيانات صحيحة في الشيت أولاً")

with tab1:
    if st.button("🔄 تحديث السجلات"):
        res = requests.get(API_URL).json()
        st.dataframe(pd.DataFrame(res[1:], columns=res), use_container_width=True)
