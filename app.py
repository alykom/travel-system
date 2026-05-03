import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import random

# الرابط المحدث الخاص بك
API_URL = "https://script.google.com/macros/s/AKfycbwJzkdxpvzndSeoMi85OyUjK3BFSaU-BTDcaFTJhSBBZ3UdPlJguJXtO-6lJ03wwaTk7w/exec"
PASSWORD = "admin" # كلمة المرور الافتراضية

st.set_page_config(page_title="Travel ERP Pro 2026", layout="wide", page_icon="🌍")

# تصميم واجهة 2026 العصرية
st.markdown("""
    <style>
    @import url('https://googleapis.com');
    * { font-family: 'Cairo', sans-serif; direction: rtl; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] { background-color: #fff; border-radius: 10px; padding: 10px 20px; border: 1px solid #ddd; }
    .stTabs [aria-selected="true"] { background: linear-gradient(90deg, #002147 0%, #004d99 100%); color: white !important; }
    .invoice-card { 
        background: white; border: 2px solid #002147; padding: 35px; border-radius: 15px; 
        box-shadow: 0 10px 30px rgba(0,0,0,0.1); direction: rtl; text-align: right; margin: auto; max-width: 800px;
    }
    .money-badge { background: #f8f9fa; padding: 15px; border-radius: 10px; border-right: 8px solid #002147; margin: 15px 0; }
    </style>
""", unsafe_allow_html=True)

# نظام تسجيل الدخول
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    col1, col2, col3 = st.columns([1,1,1])
    with col2:
        st.markdown("<h2 style='text-align:center;'>🔒 نظام السفر الدولي</h2>", unsafe_allow_html=True)
        pwd = st.text_input("أدخل كلمة المرور", type="password")
        if st.button("دخول"):
            if pwd == PASSWORD:
                st.session_state.authenticated = True
                st.rerun()
            else: st.error("❌ كلمة المرور غير صحيحة")
    st.stop()

# القائمة الرئيسية
tab1, tab2, tab3 = st.tabs(["📊 البيانات والحسابات", "👤 تسجيل عميل جديد", "🧾 البحث وطباعة الفاتورة"])

# --- تسجيل عميل جديد ---
with tab2:
    st.markdown("### ➕ إضافة ملف عميل متكامل")
    with st.form("main_form", clear_on_submit=True):
        c1, c2, c3 = st.columns(3)
        with c1:
            name = st.text_input("اسم العميل / Name")
            passport = st.text_input("رقم الجواز / Passport")
            phone = st.text_input("رقم الهاتف / Phone")
            email = st.text_input("الإيميل / Email")
        with c2:
            nation = st.text_input("الجنسية / Nationality")
            residence = st.text_input("بلد الإقامة / Residence")
            service = st.selectbox("المعاملة / Service", ["دراسة", "عمل", "سياحة"])
            branch = st.selectbox("الفرع / Branch", ["بيلاروسيا", "مصر"])
        with c3:
            v_date = st.date_input("موعد السفارة / Visa Date")
            staff = st.text_input("الموظف المضيف / Staff")
            status = st.selectbox("حالة الطلب / Status", ["قيد المعالجة", "تم الحجز", "مرفوض"])
        
        st.write("---")
        f1, f2 = st.columns(2)
        with f1: total = st.number_input("إجمالي المبلغ المتفق عليه ($)", min_value=0.0)
        with f2: paid = st.number_input("المبلغ المدفوع حالياً ($)", min_value=0.0)
        
        if st.form_submit_button("حفظ البيانات وإصدار التتبع ✅"):
            # توليد رقم تتبع عشوائي احترافي
            tracking_no = f"TRK-{random.randint(100000, 999999)}-{branch[:2].upper()}"
            # إرسال البيانات الـ 15 الأساسية (جوجل سيتولى توليد الفاتورة، الـ ID، وحساب المتبقي)
            data = [name, passport, phone, email, nation, residence, service, status, str(v_date), str(datetime.now().date()), branch, staff, total, paid, tracking_no]
            try:
                requests.post(API_URL, json=data)
                st.success(f"✅ تم الحفظ! رقم التتبع: {tracking_no}")
                st.balloons()
            except: st.error("خطأ في الاتصال بالسحابة.")

# --- عرض البيانات ---
with tab1:
    if st.button("🔄 تحديث ومزامنة البيانات اللحظية"):
        try:
            res = requests.get(API_URL).json()
            df = pd.DataFrame(res[1:], columns=res)
            st.dataframe(df, use_container_width=True)
        except: st.error("تأكد من اختيار Anyone في إعدادات النشر بجوجل.")

# --- البحث والطباعة ---
with tab3:
    search_q = st.text_input("ابحث عن العميل (الاسم أو رقم الجواز)")
    if search_q:
        res = requests.get(API_URL).json()
        df = pd.DataFrame(res[1:], columns=res)
        match = df[df['الاسم / Name'].astype(str).str.contains(search_q) | df['رقم الجواز / Passport'].astype(str).str.contains(search_q)]
        
        if not match.empty:
            c = match.iloc[0]
            st.markdown(f"""
            <div class="invoice-card">
                <table style="width:100%">
                    <tr>
                        <td style="text-align:right"><h1>🧾 فاتورة شركة السفر</h1><p>INTERNATIONAL TRAVEL CO.</p></td>
                        <td style="text-align:left"><h2 style="color:#002147">{c['رقم الفاتورة / Invoice No']}</h2><p>{c['الباركود / Barcode']}</p></td>
                    </tr>
                </table>
                <hr>
                <div style="display:flex; justify-content:space-between;">
                    <div>
                        <p><b>السيد/ة:</b> {c['الاسم / Name']}</p>
                        <p><b>الجواز:</b> {c['رقم الجواز / Passport']} | <b>الهاتف:</b> {c['الهاتف / Phone']}</p>
                        <p><b>المعاملة:</b> {c['نوع المعاملة / Service']} | <b>الحالة:</b> {c['حالة الطلب / Status']}</p>
                    </div>
                    <div style="text-align:left">
                        <p><b>التاريخ:</b> {c['التاريخ / Date']}</p>
                        <p><b>رقم التتبع:</b> {c['رقم التراك / Tracking']}</p>
                        <p><b>الفرع:</b> {c['الفرع / Branch']}</p>
                    </div>
                </div>
                <div class="money-badge">
                    <h3>💰 الموقف المالي:</h3>
                    <p>الإجمالي: {c['إجمالي الحساب / Total']}$ | المدفوع: {c['المبلغ المدفوع / Paid']}$</p>
                    <h2 style="color:#d32f2f">المبلغ المتبقي: {c['المبلغ المتبقي / Remaining']}$</h2>
                </div>
                <p style="text-align:center; font-size:12px; color:gray; margin-top:20px;">الموظف المسؤول: {c['الموظف المضيف / Staff']} | تم استخراجها آلياً بنظام 2026</p>
            </div>
            """, unsafe_allow_html=True)
            st.button("🖨️ اضغط Ctrl + P للطباعة")
        else: st.warning("لم يتم العثور على العميل.")
