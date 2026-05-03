import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import random

# --- الرابط المحدث الخاص بك ---
API_URL = "https://script.google.com/macros/s/AKfycbyjqv9fQ7i_DPsKcKoNpt0Z9dx7Vq19UT-NwwrLG-53gaZ4v04z3-B_Ft2B2bJSOAQiww/exec"
PASSWORD = "admin" 

st.set_page_config(page_title="Travel ERP Pro 2026", layout="wide", page_icon="🌍")

# --- تصميم CSS احترافي (Modern UI & Print Optimized) ---
st.markdown("""
    <style>
    @import url('https://googleapis.com');
    * { font-family: 'Cairo', sans-serif; }
    
    /* تنسيق الطباعة: إخفاء عناصر البرنامج وإظهار الفاتورة فقط */
    @media print {
        .no-print, .stSidebar, [data-testid="stHeader"], .stTabs [data-baseweb="tab-list"] { display: none !important; }
        .invoice-card { border: none !important; box-shadow: none !important; width: 100% !important; margin: 0 !important; padding: 0 !important; }
        .main { background: white !important; }
    }

    .invoice-card { 
        background: white; border: 1px solid #e0e0e0; padding: 40px; border-radius: 5px; 
        box-shadow: 0 10px 30px rgba(0,0,0,0.05); direction: rtl; text-align: right; 
        max-width: 800px; margin: auto; border-top: 15px solid #002147;
    }
    .invoice-header { display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #002147; padding-bottom: 15px; }
    .money-section { background: #f8f9fa; padding: 20px; border-radius: 5px; margin: 25px 0; border-right: 8px solid #002147; }
    .stTabs [aria-selected="true"] { background: #002147 !important; color: white !important; border-radius: 8px; }
    </style>
""", unsafe_allow_html=True)

# --- نظام الحماية ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown("<div style='text-align:center; margin-top:100px;'><h2>🔐 تسجيل دخول النظام</h2></div>", unsafe_allow_html=True)
        pwd = st.text_input("أدخل كلمة المرور", type="password")
        if st.button("دخول"):
            if pwd == PASSWORD:
                st.session_state.authenticated = True
                st.rerun()
            else: st.error("❌ كلمة المرور غير صحيحة")
    st.stop()

# --- القائمة الرئيسية (تختفي عند الطباعة) ---
st.markdown('<div class="no-print">', unsafe_allow_html=True)
st.title("🌍 نظام شركة السفر الدولي | 2026 ERP")
tab1, tab2, tab3 = st.tabs(["📊 سجلات العملاء", "👤 إضافة ملف جديد", "🧾 البحث وطباعة الفاتورة"])
st.markdown('</div>', unsafe_allow_html=True)

# --- التبويب الأول: عرض البيانات ---
with tab1:
    if st.button("🔄 تحديث ومزامنة السحابة"):
        try:
            res = requests.get(API_URL)
            if res.status_code == 200:
                data = res.json()
                df = pd.DataFrame(data[1:], columns=data)
                st.dataframe(df, use_container_width=True)
            else: st.error("جوجل ترفض الاتصال. تأكد من إعداد Anyone في النشر.")
        except: st.error("⚠️ خطأ في قراءة البيانات. تأكد من وجود بيانات في الشيت.")

# --- التبويب الثاني: تسجيل عميل جديد ---
with tab2:
    st.subheader("📝 تسجيل بيانات عميل")
    with st.form("reg_form", clear_on_submit=True):
        c1, c2, c3 = st.columns(3)
        with c1:
            name = st.text_input("الاسم الكامل / Name")
            passport = st.text_input("رقم الجواز / Passport")
            phone = st.text_input("الهاتف / Phone")
        with c2:
            nation = st.text_input("الجنسية / Nationality")
            service = st.selectbox("المعاملة / Service", ["دراسة", "عمل", "سياحة"])
            branch = st.selectbox("الفرع / Branch", ["بيلاروسيا", "مصر"])
        with c3:
            staff = st.text_input("الموظف المضيف / Staff")
            total = st.number_input("إجمالي المبلغ ($)", min_value=0.0)
            paid = st.number_input("المدفوع ($)", min_value=0.0)
        
        if st.form_submit_button("حفظ المزامنة وإصدار التتبع ✅"):
            trk = f"TRK-{random.randint(100000, 999999)}-{branch[:2].upper()}"
            # ترتيب البيانات ليرسل لـ Apps Script
            row = [name, passport, phone, "", nation, "", service, "قيد المعالجة", "", str(datetime.now().date()), branch, staff, total, paid, trk]
            try:
                requests.post(API_URL, json=row)
                st.success(f"✅ تم الحفظ! رقم التتبع: {trk}")
            except: st.error("فشل في إرسال البيانات.")

# --- التبويب الثالث: البحث والطباعة الملكية ---
with tab3:
    st.subheader("🔍 استخراج الفاتورة الذكية")
    search_q = st.text_input("ابحث عن العميل (الاسم أو رقم الجواز)")
    if search_q:
        try:
            res = requests.get(API_URL)
            if res.status_code == 200:
                data = res.json()
                df = pd.DataFrame(data[1:], columns=data)
                # البحث الذكي في عمودي الاسم والجواز (الأعمدة رقم 3 و 4)
                match = df[df.iloc[:, 2].astype(str).str.contains(search_q) | df.iloc[:, 3].astype(str).str.contains(search_q)]
                
                if not match.empty:
                    c = match.iloc[0]
                    # توليد رابط الباركود QR من جوجل
                    qr_url = f"https://googleapis.com{c.iloc[0]}"
                    
                    st.markdown(f"""
                    <div class="invoice-card">
                        <div class="invoice-header">
                            <div><h1 style="margin:0; color:#002147;">فاتورة رسمية</h1><p style="margin:0;">INTERNATIONAL TRAVEL SERVICES</p></div>
                            <div style="text-align:left;"><img src="{qr_url}" width="110"><p style="margin:0; font-size:12px;">{c.iloc[0]}</p></div>
                        </div>
                        <div style="display:flex; justify-content:space-between; margin-top:35px; direction:rtl; text-align:right;">
                            <div><p><b>السيد/ة:</b> {c.iloc[2]}</p><p><b>الجواز:</b> {c.iloc[3]} | <b>الهاتف:</b> {c.iloc[4]}</p></div>
                            <div style="text-align:left;"><p><b>التاريخ:</b> {c.iloc[11]}</p><p><b>رقم التتبع:</b> {c.iloc[17]}</p></div>
                        </div>
                        <div class="money-section">
                            <h3 style="margin-top:0;">💰 الموقف المالي:</h3>
                            <p>إجمالي الحساب: <b>{c.iloc[14]}$</b> | المدفوع: <b>{c.iloc[15]}$</b></p>
                            <h2 style="color:#d32f2f; margin-bottom:0;">المبلغ المتبقي: {c.iloc[16]}$</h2>
                        </div>
                        <div style="text-align:center; margin-top:40px; font-size:12px; color:#666; border-top:1px solid #eee; padding-top:15px;">
                            <p>هذه الوظيفة مستخرجة آلياً بنظام 2026 - فرع {c.iloc[12]}</p>
                            <p>الموظف المسؤول: {c.iloc[13]}</p>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown('<div class="no-print" style="text-align:center; margin-top:20px;">', unsafe_allow_html=True)
                    st.info("🖨️ للطباعة: اضغط على زر الطباعة في المتصفح أو Ctrl + P")
                    st.markdown('</div>', unsafe_allow_html=True)
                else: st.warning("العميل غير موجود.")
        except: st.error("⚠️ خطأ في جلب البيانات، تأكد من وجود بيانات في الشيت.")
