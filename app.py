import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import random

# إعدادات الأمان
PASSWORD = "admin"  # يمكنك تغيير كلمة المرور هنا

# رابط الـ Web App الخاص بك
API_URL = "https://google.com"

def check_password():
    if "password_correct" not in st.session_state:
        st.session_state.password_correct = False
    if not st.session_state.password_correct:
        st.markdown("<h2 style='text-align: center;'>🔐 تسجيل الدخول للنظام</h2>", unsafe_allow_html=True)
        pwd = st.text_input("أدخل كلمة المرور", type="password")
        if st.button("دخول"):
            if pwd == PASSWORD:
                st.session_state.password_correct = True
                st.rerun()
            else: st.error("❌ كلمة المرور خاطئة")
        return False
    return True

if check_password():
    st.set_page_config(page_title="Travel ERP 2026", layout="wide")

    # تصميم عصري CSS
    st.markdown("""
        <style>
        @import url('https://googleapis.com');
        * { font-family: 'Cairo', sans-serif; direction: rtl; }
        .stButton>button { background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%); color: white; border-radius: 10px; height: 3em; border: none; }
        .card { background: white; padding: 20px; border-radius: 15px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); margin-bottom: 20px; }
        </style>
    """, unsafe_allow_html=True)

    st.sidebar.title("🛂 لوحة التحكم")
    choice = st.sidebar.selectbox("القائمة", ["🏠 الرئيسية", "👤 تسجيل عميل جديد", "🔍 بحث وطباعة"])

    if choice == "🏠 الرئيسية":
        st.markdown("<h1>📊 إحصائيات النظام</h1>", unsafe_allow_html=True)
        if st.button("🔄 تحديث وعرض البيانات من السحابة"):
            res = requests.get(API_URL).json()
            df = pd.DataFrame(res[1:], columns=res)
            st.dataframe(df, use_container_width=True)

    elif choice == "👤 تسجيل عميل جديد":
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("📝 إدخال بيانات العميل")
        with st.form("modern_form", clear_on_submit=True):
            c1, c2, c3 = st.columns(3)
            with c1:
                name = st.text_input("الاسم الكامل / Name")
                passport = st.text_input("رقم الجواز / Passport")
                phone = st.text_input("الهاتف / Phone")
                email = st.text_input("الإيميل / Email")
            with c2:
                nation = st.text_input("الجنسية / Nationality")
                residence = st.text_input("الإقامة / Residence")
                service = st.selectbox("المعاملة / Service", ["دراسة", "عمل", "سياحة"])
                status = st.selectbox("الحالة / Status", ["قيد المعالجة", "تم الحجز", "مرفوض"])
            with c3:
                v_date = st.date_input("موعد السفارة")
                branch = st.selectbox("الفرع / Branch", ["بيلاروسيا", "مصر"])
                staff = st.text_input("الموظف / Staff")
                track = st.text_input("التراك / Tracking")
            
            total = st.number_input("إجمالي الحساب / Total ($)")
            paid = st.number_input("المدفوع / Paid ($)")
            
            if st.form_submit_button("حفظ وإصدار الفاتورة ✅"):
                # البيانات بالترتيب لتتوافق مع Apps Script (ID والباركود سيتم توليدهم تلقائياً)
                # نرسل 15 حقل فقط، وجوجل سيتولى الباقي
                data = [name, passport, phone, email, nation, residence, service, status, str(v_date), str(datetime.now().date()), branch, staff, total, paid, track]
                requests.post(API_URL, json=data)
                st.success("✅ تم الحفظ والمزامنة بنجاح!")
        st.markdown("</div>", unsafe_allow_html=True)

    elif choice == "🔍 بحث وطباعة":
        st.subheader("📑 البحث عن فاتورة")
        search = st.text_input("ادخل اسم العميل")
        if search and st.button("عرض الفاتورة"):
            # كود البحث والطباعة يظهر هنا
            st.info("سيتم جلب بيانات الفاتورة المصممة للطباعة...")
