import streamlit as st
import requests
import pandas as pd

# رابطك الجديد والنهائي
API_URL = "https://script.google.com/macros/s/AKfycbw1dL-U7qw0apQ5UZO0226QzTDhFIneAldHdUlzTTyuT6rC2FGNM3SNNAC5eU1iwsxVVg/exec"

st.set_page_config(page_title="نظام شركة السفر الموحد", layout="wide", page_icon="🌍")

# تنسيق الواجهة للغة العربية
st.markdown("""<style> .main { text-align: right; direction: rtl; } div[data-testid="stSidebar"] { direction: rtl; } </style>""", unsafe_allow_html=True)

st.title("🌍 نظام إدارة الشركة (بيلاروسيا 🇧🇾 - مصر 🇪🇬)")
st.write("---")

menu = ["🏠 عرض قاعدة البيانات", "➕ تسجيل عميل جديد"]
choice = st.sidebar.selectbox("القائمة الرئيسية", menu)

if choice == "🏠 عرض قاعدة البيانات":
    st.subheader("📋 قائمة البيانات الحالية")
    if st.button("تحديث البيانات 🔄"):
        try:
            with st.spinner('جاري التحميل...'):
                response = requests.get(API_URL)
                data = response.json()
                if len(data) > 0:
                    df = pd.DataFrame(data[1:], columns=data[0])
                    st.table(df) # عرض كجدول ثابت وواضح
                else:
                    st.info("لا توجد بيانات حالياً.")
        except:
            st.error("فشل في الاتصال بجوجل شيت.")

elif choice == "➕ تسجيل عميل جديد":
    st.subheader("✍️ إدخال بيانات العميل")
    with st.form("main_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            id_val = st.text_input("رقم الملف (ID)")
            name_val = st.text_input("اسم العميل")
            type_val = st.selectbox("نوع الخدمة", ["طالب", "عقد عمل", "سياحة"])
            branch_val = st.selectbox("الفرع", ["مصر", "بيلاروسيا"])
        with col2:
            status_val = st.selectbox("حالة الملف", ["قيد التجهيز", "بانتظار الموعد", "تم الحجز"])
            passport_val = st.text_input("رابط الأوراق (Drive)")
            fee_val = st.text_input("إجمالي المبلغ ($)")
            paid_val = st.text_input("المبلغ المدفوع ($)")
        
        submit = st.form_submit_button("حفظ وإرسال بنجاح ✅")
        
        if submit:
            # الترتيب المطابق للشيت تماماً
            row = [id_val, name_val, type_val, branch_val, status_val, passport_val, fee_val, paid_val]
            try:
                with st.spinner('جاري المزامنة...'):
                    resp = requests.post(API_URL, json=row)
                    st.success(f"✅ تم حفظ بيانات العميل ({name_val}) بنجاح في الفرعين!")
            except:
                st.error("خطأ في الخادم")
