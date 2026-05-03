import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import random

# --- إعدادات النظام المحدثة برابطك الأخير ---
API_URL = "https://script.google.com/macros/s/AKfycbwjcFf7WYycY2sAGpTpgb0sBHWGEY2Yc1ArcOdAH6A7ZtioibgEdfBxkCkNaoEoe84FkQ/exec"
PASSWORD = "admin" # كلمة المرور للدخول

# --- إعدادات الصفحة العصرية ---
st.set_page_config(page_title="Global Travel ERP 2026", layout="wide", page_icon="🌍")

# تصميم CSS احترافي (Glassmorphism & Modern UI)
st.markdown("""
    <style>
    @import url('https://googleapis.com');
    * { font-family: 'Cairo', sans-serif; direction: rtl; }
    .main { background-color: #f8f9fa; }
    .stTabs [data-baseweb="tab-list"] { gap: 20px; }
    .stTabs [data-baseweb="tab"] { background-color: #ffffff; border-radius: 12px; padding: 10px 25px; border: 1px solid #e0e0e0; font-weight: bold; }
    .stTabs [aria-selected="true"] { background: linear-gradient(135deg, #002147 0%, #004d99 100%); color: white !important; box-shadow: 0 4px 15px rgba(0,0,0,0.2); }
    .invoice-card { border: 3px solid #002147; padding: 40px; border-radius: 20px; background: white; box-shadow: 0 15px 35px rgba(0,0,0,0.1); margin-top: 20px; }
    .stat-box { background: white; padding: 25px; border-radius: 15px; text-align: center; border-bottom: 6px solid #002147; box-shadow: 0 4px 10px rgba(0,0,0,0.05); }
    .stButton>button { border-radius: 10px; height: 3.5em; font-weight: bold; transition: 0.3s; }
    </style>
""", unsafe_allow_html=True)

# --- نظام الحماية ---
if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    col1, col2, col3 = st.columns([1,1,1])
    with col2:
        st.markdown("<div style='margin-top: 100px; text-align: center;'>", unsafe_allow_html=True)
        st.image("https://flaticon.com", width=100)
        st.markdown("<h2>🔑 دخول النظام الآمن</h2>", unsafe_allow_html=True)
        pwd = st.text_input("أدخل كلمة المرور الخاصة بالمدير", type="password")
        if st.button("تسجيل الدخول"):
            if pwd == PASSWORD:
                st.session_state.auth = True
                st.rerun()
            else: st.error("❌ كلمة المرور غير صحيحة، حاول مرة أخرى")
    st.stop()

# --- واجهة البرنامج الرئيسية ---
st.title("🌍 نظام إدارة شركة السفر الدولي | 2026 ERP")
st.write(f"مرحباً بك في لوحة التحكم | **فرع بيلاروسيا & مصر** | {datetime.now().strftime('%Y-%m-%d')}")

tab1, tab2, tab3 = st.tabs(["📊 الإحصائيات والقاعدة", "👤 إضافة ملف جديد", "🔍 البحث وطباعة فاتورة"])

# --- التبويب الأول: الإحصائيات والبيانات ---
with tab1:
    st.markdown("### 📈 حالة العمل اليوم")
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.markdown("<div class='stat-box'><h3>مجموع العملاء</h3><h2 style='color:#002147'>1,250</h2></div>", unsafe_allow_html=True)
    with c2: st.markdown("<div class='stat-box'><h3>ملفات ناجحة</h3><h2 style='color:green'>850</h2></div>", unsafe_allow_html=True)
    with c3: st.markdown("<div class='stat-box'><h3>قيد الانتظار</h3><h2 style='color:orange'>45</h2></div>", unsafe_allow_html=True)
    with c4: st.markdown("<div class='stat-box'><h3>ديون متبقية</h3><h2 style='color:red'>$12,400</h2></div>", unsafe_allow_html=True)
    
    st.write("---")
    if st.button("🔄 تحديث ومزامنة البيانات اللحظية من السحابة"):
        with st.spinner("جاري جلب البيانات من Google Sheets..."):
            try:
                res = requests.get(API_URL)
                data_json = res.json()
                df = pd.DataFrame(data_json[1:], columns=data_json[0])
                st.dataframe(df, use_container_width=True)
            except:
                st.error("فشل الاتصال! تأكد من ضبط الـ Deploy في جوجل على Anyone.")

# --- التبويب الثاني: تسجيل عميل جديد ---
with tab2:
    st.markdown("### 📝 تسجيل بيانات عميل جديد")
    with st.form("client_reg", clear_on_submit=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            name = st.text_input("الاسم الكامل / Full Name")
            passport = st.text_input("رقم الجواز / Passport")
            phone = st.text_input("الهاتف / Phone")
            email = st.text_input("الإيميل / Email")
        with col2:
            nation = st.text_input("الجنسية / Nationality")
            residence = st.text_input("بلد الإقامة / Residence")
            service = st.selectbox("المعاملة / Service", ["دراسة/Study", "عقد عمل/Work", "سياحة/Tourism"])
            status = st.selectbox("الحالة / Status", ["قيد المعالجة", "تم الحجز", "مرفوض"])
        with col3:
            visa_date = st.date_input("موعد السفارة / Visa Date")
            branch = st.selectbox("الفرع / Branch", ["بيلاروسيا", "مصر"])
            staff = st.text_input("الموظف المضيف / Staff")
            track = st.text_input("رقم التراك / Tracking No")
        
        st.write("---")
        fa1, fa2 = st.columns(2)
        with fa1: total = st.number_input("إجمالي المبلغ المتفق عليه / Total ($)", min_value=0.0)
        with fa2: paid = st.number_input("المبلغ المدفوع حالياً / Paid ($)", min_value=0.0)
        
        if st.form_submit_button("✅ حفظ البيانات وتوليد الفاتورة"):
            # الترتيب ليرسل إلى Apps Script: Name, Passport, Phone, Email, Nation, Residence, Service, Status, VisaDate, Date, Branch, Staff, Total, Paid, Track
            row_data = [name, passport, phone, email, nation, residence, service, status, str(visa_date), str(datetime.now().date()), branch, staff, total, paid, track]
            try:
                requests.post(API_URL, json=row_data)
                st.success(f"🎉 تم الحفظ بنجاح! تم مزامنة ملف ({name}) بين مصر وبيلاروسيا.")
                st.balloons()
            except: st.error("حدث خطأ في المزامنة.")

# --- التبويب الثالث: البحث والطباعة ---
with tab3:
    st.markdown("### 🔍 استخراج الفواتير والبحث الذكي")
    search_q = st.text_input("ابحث عن اسم العميل أو رقم الجواز لتوليد الفاتورة")
    if search_q:
        res = requests.get(API_URL).json()
        df = pd.DataFrame(res[1:], columns=res[0])
        # البحث في عمودي الاسم والجواز
        match = df[df['الاسم / Name'].astype(str).str.contains(search_q) | df['رقم الجواز / Passport'].astype(str).str.contains(search_q)]
        
        if not match.empty:
            c = match.iloc[0] # جلب أول نتيجة بحث
            st.markdown(f"""
            <div class="invoice-card">
                <table style="width:100%">
                    <tr>
                        <td style="text-align:right"><h1>🧾 فاتورة رسمية</h1></td>
                        <td style="text-align:left"><h2 style="color:#002147">{c['رقم الفاتورة / Invoice No']}</h2></td>
                    </tr>
                </table>
                <hr style="border:1px solid #002147">
                <div style="display:flex; justify-content:space-between; text-align:right; margin-top:20px;">
                    <div>
                        <p style="font-size:1.2em"><b>العميل:</b> {c['الاسم / Name']}</p>
                        <p><b>رقم الجواز:</b> {c['رقم الجواز / Passport']}</p>
                        <p><b>رقم الهاتف:</b> {c['الهاتف / Phone']}</p>
                    </div>
                    <div style="text-align:left">
                        <p><b>التاريخ:</b> {c['التاريخ / Date']}</p>
                        <p><b>نوع الخدمة:</b> {c['نوع المعاملة / Service']}</p>
                        <p><b>الفرع المسجل:</b> {c['الفرع / Branch']}</p>
                    </div>
                </div>
                <div style="background:#f1f3f5; padding:25px; border-radius:15px; margin-top:30px; border-right:10px solid #002147">
                    <h3 style="margin-top:0">📊 التفاصيل المالية:</h3>
                    <p style="font-size:1.1em">إجمالي الحساب: {c['إجمالي الحساب / Total']}$</p>
                    <p style="font-size:1.1em">المبلغ المدفوع: {c['المبلغ المدفوع / Paid']}$</p>
                    <h2 style="color:#d32f2f; margin-bottom:0">المبلغ المتبقي: {c['المبلغ المتبقي / Remaining']}$</h2>
                </div>
                <div style="margin-top:30px; text-align:center; color:#666">
                    <p>باركود التتبع: {c['الباركود / Barcode']} | الموظف المسؤول: {c['الموظف المضيف / Staff']}</p>
                    <p><i>شكراً لتعاملكم مع شركتنا - رحلة سعيدة!</i></p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            st.info("💡 نصيحة: اضغط Ctrl + P لطباعة الفاتورة أو حفظها كـ PDF.")
        else: st.warning("⚠️ لم يتم العثور على أي بيانات مطابقة لهذا البحث.")
