import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import random
import barcode
from barcode.writer import ImageWriter
import base64
from io import BytesIO

API_URL = "https://google.com"
PASSWORD = "admin"

# وظيفة توليد الباركود كصورة
def generate_barcode(data):
    EAN = barcode.get_銘柄('code128', data, writer=ImageWriter())
    buffer = BytesIO()
    EAN.write(buffer)
    return base64.b64encode(buffer.getvalue()).decode()

st.set_page_config(page_title="Travel ERP Pro 2026", layout="wide")

# تصميم CSS احترافي جداً للفاتورة
st.markdown("""
    <style>
    @import url('https://googleapis.com');
    * { font-family: 'Cairo', sans-serif; direction: rtl; }
    .invoice-card { 
        background: #fff; border: 1px solid #eee; padding: 40px; border-radius: 0px;
        box-shadow: 0 0 20px rgba(0,0,0,0.1); border-top: 15px solid #002147;
        max-width: 800px; margin: auto; color: #333;
    }
    .header-table { width: 100%; border-bottom: 2px solid #002147; margin-bottom: 20px; }
    .footer-note { font-size: 12px; color: #777; margin-top: 30px; text-align: center; border-top: 1px solid #eee; padding-top: 10px; }
    .money-box { background: #f9f9f9; padding: 20px; border-radius: 5px; margin-top: 20px; border-right: 5px solid #002147; }
    </style>
""", unsafe_allow_html=True)

# (هنا يوضع كود الحماية Password كما في السابق...)
if "auth" not in st.session_state: st.session_state.auth = False
if not st.session_state.auth:
    pwd = st.sidebar.text_input("كلمة المرور", type="password")
    if st.sidebar.button("دخول"):
        if pwd == PASSWORD: st.session_state.auth = True; st.rerun()
    st.stop()

tab1, tab2, tab3 = st.tabs(["📊 البيانات", "👤 إضافة عميل", "🔍 البحث والطباعة"])

with tab2:
    st.subheader("📝 تسجيل ملف جديد")
    with st.form("reg_form"):
        c1, c2, c3 = st.columns(3)
        with c1:
            name = st.text_input("الاسم الكامل")
            passport = st.text_input("رقم الجواز")
            phone = st.text_input("رقم الهاتف")
        with c2:
            nation = st.text_input("الجنسية")
            service = st.selectbox("المعاملة", ["دراسة", "عمل", "سياحة"])
            branch = st.selectbox("الفرع", ["بيلاروسيا", "مصر"])
        with c3:
            total = st.number_input("الإجمالي ($)")
            paid = st.number_input("المدفوع ($)")
            staff = st.text_input("الموظف")

        if st.form_submit_button("حفظ وإصدار الفاتورة ✅"):
            # توليد رقم تتبع عشوائي احترافي مثل: TRK-859403-EG
            track_no = f"TRK-{random.randint(100000, 999999)}-{branch[:2].upper()}"
            row = [name, passport, phone, "", nation, "", service, "قيد المعالجة", "", str(datetime.now().date()), branch, staff, total, paid, track_no]
            requests.post(API_URL, json=row)
            st.success(f"تم الحفظ! رقم التتبع: {track_no}")

with tab3:
    search = st.text_input("ابحث عن عميل للطباعة")
    if search:
        res = requests.get(API_URL).json()
        df = pd.DataFrame(res[1:], columns=res)
        match = df[df['الاسم / Name'].str.contains(search)]
        
        if not match.empty:
            c = match.iloc[0]
            barcode_base64 = generate_barcode(str(c['رقم الفاتورة / Invoice No']))
            
            st.markdown(f"""
            <div class="invoice-card">
                <table class="header-table">
                    <tr>
                        <td style="text-align:right"><h1>فاتورة خدمات سفر</h1><p>INTERNATIONAL TRAVEL CO.</p></td>
                        <td style="text-align:left"><img src="data:image/png;base64,{barcode_base64}" width="150"><br><b>{c['رقم الفاتورة / Invoice No']}</b></td>
                    </tr>
                </table>
                <div style="display:flex; justify-content:space-between; margin-bottom:20px;">
                    <div style="text-align:right">
                        <p><b>السيد/ة:</b> {c['الاسم / Name']}</p>
                        <p><b>رقم الجواز:</b> {c['رقم الجواز / Passport']}</p>
                        <p><b>الجنسية:</b> {c['الجنسية / Nationality']}</p>
                    </div>
                    <div style="text-align:left">
                        <p><b>التاريخ:</b> {c['التاريخ / Date']}</p>
                        <p><b>رقم التتبع:</b> {c['رقم التراك / Tracking']}</p>
                        <p><b>الفرع:</b> {c['الفرع / Branch']}</p>
                    </div>
                </div>
                <div class="money-box">
                    <table style="width:100%; text-align:center;">
                        <tr style="background:#eee;"><th>الإجمالي</th><th>المدفوع</th><th>المتبقي</th></tr>
                        <tr><td>{c['إجمالي الحساب / Total']}$</td><td>{c['المبلغ المدفوع / Paid']}$</td><td style="color:red; font-weight:bold;">{c['المبلغ المتبقي / Remaining']}$</td></tr>
                    </table>
                </div>
                <div class="footer-note">
                    <p>هذه الفاتورة مستخرجة آلياً ولا تحتاج لختم - شكراً لثقتكم بنا</p>
                    <p>بيلاروسيا - مصر | 2026</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            st.button("🖨️ طباعة الفاتورة الآن")
