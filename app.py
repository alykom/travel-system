import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import random

# الرابط الخاص بك (تأكد أنه الرابط الذي ينتهي بـ /exec)
API_URL = "https://google.com"
PASSWORD = "admin" 

st.set_page_config(page_title="Travel ERP Pro 2026", layout="wide")

# تصميم الفاتورة الملكي مع ميزة إخفاء عناصر الموقع عند الطباعة
st.markdown("""
    <style>
    @import url('https://googleapis.com');
    * { font-family: 'Cairo', sans-serif; }
    
    @media print {
        .no-print { display: none !important; }
        .invoice-card { border: none !important; box-shadow: none !important; width: 100% !important; margin: 0 !important; padding: 0 !important; }
        body { background-color: white !important; }
    }

    .invoice-card { 
        background: white; border: 1px solid #e0e0e0; padding: 50px; border-radius: 0px; 
        box-shadow: 0 0 20px rgba(0,0,0,0.05); direction: rtl; text-align: right; 
        max-width: 800px; margin: auto; border-top: 20px solid #002147;
    }
    .invoice-header { display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #002147; padding-bottom: 20px; }
    .money-section { background: #f9f9f9; padding: 25px; border-radius: 5px; margin: 30px 0; border-right: 10px solid #002147; }
    </style>
""", unsafe_allow_html=True)

# نظام الدخول
if "auth" not in st.session_state: st.session_state.auth = False
if not st.session_state.auth:
    st.markdown("<h2 style='text-align:center;'>🔐 تسجيل الدخول</h2>", unsafe_allow_html=True)
    pwd = st.text_input("كلمة المرور", type="password")
    if st.button("دخول"):
        if pwd == PASSWORD: st.session_state.auth = True; st.rerun()
        else: st.error("❌ كلمة المرور غير صحيحة")
    st.stop()

# القائمة الرئيسية
st.markdown('<div class="no-print">', unsafe_allow_html=True)
tab1, tab2, tab3 = st.tabs(["📊 السجلات", "👤 إضافة عميل", "🔍 البحث والطباعة"])
st.markdown('</div>', unsafe_allow_html=True)

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
            total = st.number_input("إجمالي المبلغ ($)")
            paid = st.number_input("المدفوع ($)")

        if st.form_submit_button("حفظ المزامنة وإصدار الفاتورة ✅"):
            trk = f"TRK-{random.randint(100000, 999999)}-{branch[:2].upper()}"
            row = [name, passport, phone, "", nation, "", service, "قيد المعالجة", "", str(datetime.now().date()), branch, staff, total, paid, trk]
            try:
                requests.post(API_URL, json=row)
                st.success(f"✅ تم الحفظ بنجاح!")
            except: st.error("❌ فشل في الاتصال بجوجل، تأكد من إعدادات النشر.")

with tab3:
    st.subheader("🔍 استخراج الفاتورة للطباعة")
    search_q = st.text_input("ابحث عن العميل (الاسم أو رقم الجواز)")
    if search_q:
        try:
            res = requests.get(API_URL)
            if res.status_code == 200:
                data_json = res.json()
                df = pd.DataFrame(data_json[1:], columns=data_json)
                match = df[df.iloc[:, 2].astype(str).str.contains(search_q) | df.iloc[:, 3].astype(str).str.contains(search_q)]
                
                if not match.empty:
                    c = match.iloc[0]
                    qr_url = f"https://googleapis.com{c.iloc[0]}"
                    st.markdown(f"""
                    <div class="invoice-card">
                        <div class="invoice-header">
                            <div><h1 style="margin:0; color:#002147;">فاتورة رسمية</h1><p style="margin:0;">INTERNATIONAL TRAVEL SERVICES</p></div>
                            <div style="text-align:left;"><img src="{qr_url}" width="100"><p style="margin:0; font-size:12px;">{c.iloc[0]}</p></div>
                        </div>
                        <div style="display:flex; justify-content:space-between; margin-top:40px;">
                            <div><p><b>السيد/ة:</b> {c.iloc[2]}</p><p><b>رقم الجواز:</b> {c.iloc[3]} | <b>الهاتف:</b> {c.iloc[4]}</p></div>
                            <div style="text-align:left;"><p><b>التاريخ:</b> {c.iloc[11]}</p><p><b>رقم التتبع:</b> {c.iloc[17]}</p></div>
                        </div>
                        <div class="money-section">
                            <h3 style="margin-top:0;">💰 الموقف المالي:</h3>
                            <p>إجمالي الحساب: <b>{c.iloc[14]}$</b> | المدفوع: <b>{c.iloc[15]}$</b></p>
                            <h2 style="color:#d32f2f;">المبلغ المتبقي: {c.iloc[16]}$</h2>
                        </div>
                        <div style="text-align:center; margin-top:50px; font-size:12px; color:#777; border-top:1px solid #eee; padding-top:10px;">
                            <p>هذه الفاتورة مستخرجة آلياً - الموظف المسؤول: {c.iloc[13]}</p>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    st.markdown('<div class="no-print">', unsafe_allow_html=True)
                    st.info("💡 اضغط Ctrl + P للطباعة.")
                    st.markdown('</div>', unsafe_allow_html=True)
                else: st.warning("العميل غير موجود.")
            else: st.error("❌ رابط جوجل لا يستجيب، يرجى تحديث النشر.")
        except: st.error("⚠️ خطأ في قراءة البيانات. يرجى مراجعة الرابط وصلاحيات الوصول.")
