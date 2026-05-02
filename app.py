import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import random

# --- إعدادات النظام ---
API_URL = "https://google.com"
PASSWORD = "admin" # كلمة المرور للدخول

# --- إعدادات الصفحة العصرية ---
st.set_page_config(page_title="Global Travel ERP 2026", layout="wide", page_icon="🌍")

# تصميم CSS احترافي (Glassmorphism & Modern UI)
st.markdown("""
    <style>
    @import url('https://googleapis.com');
    * { font-family: 'Cairo', sans-serif; direction: rtl; }
    .main { background-color: #f0f2f6; }
    .stTabs [data-baseweb="tab-list"] { gap: 20px; }
    .stTabs [data-baseweb="tab"] { background-color: #ffffff; border-radius: 10px; padding: 10px 20px; border: 1px solid #ddd; }
    .stTabs [aria-selected="true"] { background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%); color: white !important; }
    .invoice-box { border: 2px solid #1e3c72; padding: 30px; border-radius: 15px; background: white; box-shadow: 0 10px 30px rgba(0,0,0,0.1); }
    .stat-card { background: white; padding: 20px; border-radius: 15px; text-align: center; border-bottom: 5px solid #1e3c72; }
    </style>
""", unsafe_allow_html=True)

# --- نظام الحماية ---
if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    col1, col2, col3 = st.columns([1,1,1])
    with col2:
        st.markdown("<h2 style='text-align:center;'>🔒 تسجيل الدخول</h2>", unsafe_allow_html=True)
        pwd = st.text_input("كلمة المرور", type="password")
        if st.button("دخول للنظام"):
            if pwd == PASSWORD:
                st.session_state.auth = True
                st.rerun()
            else: st.error("❌ كلمة المرور غير صحيحة")
    st.stop()

# --- واجهة البرنامج الرئيسية ---
st.title("🌍 نظام الإدارة الدولي - International Travel System")
st.write(f"مرحباً بك | فرع: بيلاروسيا - مصر | {datetime.now().strftime('%Y-%m-%d')}")

tab1, tab2, tab3 = st.tabs(["📊 لوحة البيانات", "👤 تسجيل عميل جديد", "🧾 البحث والفواتير"])

# --- التبويب الأول: الإحصائيات ---
with tab1:
    st.markdown("### 📈 نظرة عامة")
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.markdown("<div class='stat-card'><h3>العملاء</h3><h2>1,250</h2></div>", unsafe_allow_html=True)
    with c2: st.markdown("<div class='stat-card'><h3>تأشيرات</h3><h2>850</h2></div>", unsafe_allow_html=True)
    with c3: st.markdown("<div class='stat-card'><h3>قيد المعالجة</h3><h2>45</h2></div>", unsafe_allow_html=True)
    with c4: st.markdown("<div class='stat-card'><h3>الفواتير اليومية</h3><h2>12</h2></div>", unsafe_allow_html=True)
    
    st.write("---")
    if st.button("🔄 تحديث ومزامنة البيانات من السحاب"):
        with st.spinner("جاري جلب البيانات..."):
            res = requests.get(API_URL).json()
            df = pd.DataFrame(res[1:], columns=res)
            st.dataframe(df, use_container_width=True)

# --- التبويب الثاني: التسجيل ---
with tab2:
    st.markdown("### 📝 إضافة ملف جديد")
    with st.form("add_client", clear_on_submit=True):
        f1, f2, f3 = st.columns(3)
        with f1:
            name = st.text_input("الاسم الكامل / Name")
            passport = st.text_input("رقم الجواز / Passport")
            phone = st.text_input("الهاتف / Phone")
            email = st.text_input("الإيميل / Email")
        with f2:
            nation = st.text_input("الجنسية / Nationality")
            residence = st.text_input("الإقامة / Residence")
            service = st.selectbox("المعاملة / Service", ["دراسة", "عمل", "سياحة"])
            status = st.selectbox("الحالة / Status", ["قيد المعالجة", "تم الحجز", "مرفوض"])
        with f3:
            visa_date = st.date_input("موعد السفارة")
            branch = st.selectbox("الفرع / Branch", ["مصر", "بيلاروسيا"])
            staff = st.text_input("الموظف المضيف / Staff")
            track = st.text_input("التراك / Tracking")
        
        st.write("---")
        fa1, fa2 = st.columns(2)
        with fa1: total = st.number_input("إجمالي الحساب / Total ($)", min_value=0.0)
        with fa2: paid = st.number_input("المدفوع / Paid ($)", min_value=0.0)
        
        if st.form_submit_button("✅ حفظ البيانات وإصدار رقم الفاتورة"):
            data = [name, passport, phone, email, nation, residence, service, status, str(visa_date), str(datetime.now().date()), branch, staff, total, paid, track]
            resp = requests.post(API_URL, json=data)
            st.success("🎉 تم الحفظ بنجاح! تم تحديث فرع مصر وبيلاروسيا.")

# --- التبويب الثالث: الفواتير ---
with tab3:
    st.markdown("### 🔍 البحث والطباعة")
    search_input = st.text_input("ابحث عن عميل (الاسم أو رقم الجواز)")
    if search_input:
        res = requests.get(API_URL).json()
        df = pd.DataFrame(res[1:], columns=res)
        match = df[df['الاسم / Name'].str.contains(search_input) | df['رقم الجواز / Passport'].str.contains(search_input)]
        
        if not match.empty:
            c = match.iloc[0]
            st.markdown(f"""
            <div class="invoice-box">
                <table style="width:100%">
                    <tr>
                        <td style="text-align:right"><h1>فاتورة رسمية</h1></td>
                        <td style="text-align:left"><h3>{c['رقم الفاتورة / Invoice No']}</h3></td>
                    </tr>
                </table>
                <hr>
                <div style="display:flex; justify-content:space-between; text-align:right;">
                    <div>
                        <p><b>العميل:</b> {c['الاسم / Name']}</p>
                        <p><b>الجواز:</b> {c['رقم الجواز / Passport']}</p>
                    </div>
                    <div>
                        <p><b>التاريخ:</b> {c['التاريخ / Date']}</p>
                        <p><b>المعاملة:</b> {c['نوع المعاملة / Service']}</p>
                    </div>
                </div>
                <div style="background:#f8f9fa; padding:15px; border-radius:10px; margin-top:20px">
                    <h3>الموقف المالي:</h3>
                    <p>الإجمالي: {c['إجمالي الحساب / Total']}$ | المدفوع: {c['المبلغ المدفوع / Paid']}$</p>
                    <h2 style="color:#d32f2f">المتبقي: {c['المبلغ المتبقي / Remaining']}$</h2>
                </div>
                <p style="text-align:center; margin-top:20px">رقم التتبع: {c['رقم التراك / Tracking']} | {c['الباركود / Barcode']}</p>
            </div>
            """, unsafe_allow_html=True)
            st.button("🖨️ طباعة الفاتورة (Ctrl+P)")
        else: st.warning("لم يتم العثور على بيانات.")
