import streamlit as st
import requests
import pandas as pd

# رابط الـ Web App الخاص بك
API_URL = "https://google.com"

st.set_page_config(page_title="نظام شركة السفر الموحد", layout="wide")

# تنسيق الواجهة من اليمين لليسار
st.markdown("""<style> .main { text-align: right; direction: rtl; } div[data-testid="stSidebar"] { direction: rtl; } </style>""", unsafe_allow_html=True)

st.title("🌍 نظام إدارة الشركة (بيلاروسيا 🇧🇾 - مصر 🇪🇬)")

menu = ["🏠 عرض قاعدة البيانات", "➕ تسجيل عميل جديد"]
choice = st.sidebar.selectbox("القائمة الرئيسية", menu)

if choice == "🏠 عرض قاعدة البيانات":
    st.subheader("📋 جميع البيانات المسجلة")
    if st.button("تحديث القائمة 🔄"):
        try:
            response = requests.get(API_URL)
            data = response.json()
            if len(data) > 0:
                # عرض البيانات كما هي في الشيت تماماً
                df = pd.DataFrame(data[1:], columns=data[0])
                st.dataframe(df, use_container_width=True)
        except:
            st.error("فشل في جلب البيانات.")

elif choice == "➕ تسجيل عميل جديد":
    st.subheader("✍️ إدخال بيانات العميل (مطابق للشيت)")
    with st.form("main_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            id_val = st.text_input("رقم الملف (ID)")
            name_val = st.text_input("اسم العميل")
            type_val = st.selectbox("نوع الخدمة", ["طالب", "عقد عمل", "سياحة"])
            branch_val = st.selectbox("الفرع", ["مصر", "بيلاروسيا"])
        with col2:
            status_val = st.selectbox("حالة الملف", ["قيد التجهيز", "بانتظار الموعد", "تم الحجز"])
            passport_val = st.text_input("رابط ملفات العميل (Drive)")
            fee_val = st.text_input("إجمالي المبلغ ($)")
            paid_val = st.text_input("المبلغ المدفوع ($)")
        
        submit = st.form_submit_button("حفظ وإرسال ✅")
        if submit:
            # الترتيب المطابق لأعمدة الشيت (A إلى H)
            row = [id_val, name_val, type_val, branch_val, status_val, passport_val, fee_val, paid_val]
            try:
                requests.post(API_URL, json=row)
                st.success("✅ تم التزامن بنجاح بين الفروع!")
            except:
                st.error("خطأ في الخادم")
