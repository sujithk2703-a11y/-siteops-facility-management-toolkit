import io
from datetime import date
import pandas as pd
import streamlit as st

st.set_page_config(page_title="SiteOps Toolkit", page_icon="🗂️", layout="wide")

REQUIRED_COLUMNS = {
    "Documents": ["Document_No", "Title", "Date", "Revision", "Status", "Recipient", "Due_Date", "Submission_Date"],
    "Procurement": ["Request_No", "Material_Description", "Category", "Quantity", "Unit", "Request_Date", "Status", "Requested_By"],
    "Billing": ["Invoice_No", "Billing_Month", "Service", "Invoice_Amount_OMR", "Paid_Amount_OMR", "Status", "Submission_Date"],
    "Attendance": ["Date", "Employee_ID", "Designation", "Attendance_Status", "Regular_Hours", "Overtime_Hours"],
    "WorkOrders": ["Work_Order_No", "Description", "Discipline", "Priority", "Status", "Reported_Date", "Due_Date", "Assigned_Team"],
}

st.title("🗂️ SiteOps – Facility Management & Document Control Toolkit")
st.caption("A practical starter dashboard for document registers, procurement follow-up, billing, attendance and work orders.")
st.info("Use fictional or approved data only. Do not upload confidential employer, employee, supplier or client information.")

uploaded = st.file_uploader("Upload your SiteOps Excel workbook (.xlsx)", type=["xlsx"])
if uploaded is None:
    st.subheader("Get started")
    st.write("Upload an Excel workbook with the five sheets listed below. You can start with the included `sample_data.xlsx` file.")
    st.markdown("""
    - **Documents** – document register and submission status
    - **Procurement** – material requisitions, purchase requests and quotation follow-up
    - **Billing** – invoice and payment tracking (OMR)
    - **Attendance** – attendance and overtime records
    - **WorkOrders** – maintenance work orders and due dates
    """)
    st.stop()

try:
    workbook = pd.ExcelFile(uploaded)
    data = {sheet: pd.read_excel(workbook, sheet_name=sheet) for sheet in REQUIRED_COLUMNS if sheet in workbook.sheet_names}
except Exception as exc:
    st.error(f"Could not read this workbook: {exc}")
    st.stop()

errors = []
for sheet, columns in REQUIRED_COLUMNS.items():
    if sheet not in data:
        errors.append(f"Missing worksheet: {sheet}")
    else:
        missing = [col for col in columns if col not in data[sheet].columns]
        if missing:
            errors.append(f"{sheet}: missing columns {', '.join(missing)}")
if errors:
    st.error("Please correct the workbook structure:\n\n" + "\n".join(f"- {e}" for e in errors))
    st.stop()

docs, procurement, billing, attendance, workorders = [data[k].copy() for k in REQUIRED_COLUMNS]

# Safe numeric/date conversions
for col in ["Invoice_Amount_OMR", "Paid_Amount_OMR"]:
    billing[col] = pd.to_numeric(billing[col], errors="coerce").fillna(0)
billing["Outstanding_OMR"] = (billing["Invoice_Amount_OMR"] - billing["Paid_Amount_OMR"]).clip(lower=0)
for df, col in [(docs, "Due_Date"), (docs, "Submission_Date"), (workorders, "Due_Date")]:
    df[col] = pd.to_datetime(df[col], errors="coerce")
today = pd.Timestamp(date.today())
docs["Is_Overdue"] = docs["Due_Date"].notna() & docs["Submission_Date"].isna() & (docs["Due_Date"] < today)
workorders["Is_Overdue"] = workorders["Due_Date"].notna() & (~workorders["Status"].astype(str).str.lower().eq("completed")) & (workorders["Due_Date"] < today)

st.sidebar.header("Filters")
doc_statuses = sorted(docs["Status"].dropna().astype(str).unique().tolist())
selected_doc_status = st.sidebar.multiselect("Document status", doc_statuses, default=doc_statuses)
wo_statuses = sorted(workorders["Status"].dropna().astype(str).unique().tolist())
selected_wo_status = st.sidebar.multiselect("Work order status", wo_statuses, default=wo_statuses)
docs_view = docs[docs["Status"].astype(str).isin(selected_doc_status)]
wo_view = workorders[workorders["Status"].astype(str).isin(selected_wo_status)]

st.subheader("Operations overview")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Documents", len(docs_view))
c2.metric("Open work orders", int((wo_view["Status"].astype(str).str.lower() != "completed").sum()))
c3.metric("Procurement requests", len(procurement))
c4.metric("Outstanding billing (OMR)", f'{billing["Outstanding_OMR"].sum():,.2f}')

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Documents", "Procurement", "Billing", "Attendance", "Work Orders", "Export"])

with tab1:
    st.markdown("#### Document register")
    st.metric("Overdue, not submitted", int(docs_view["Is_Overdue"].sum()))
    st.dataframe(docs_view, use_container_width=True, hide_index=True)

with tab2:
    st.markdown("#### Procurement follow-up")
    st.dataframe(procurement, use_container_width=True, hide_index=True)
    st.caption("Track request status consistently, for example: Requested → Quotation Received → Pending Approval → PO Issued.")

with tab3:
    st.markdown("#### Billing summary")
    b1, b2 = st.columns(2)
    b1.metric("Invoice value (OMR)", f'{billing["Invoice_Amount_OMR"].sum():,.2f}')
    b2.metric("Paid value (OMR)", f'{billing["Paid_Amount_OMR"].sum():,.2f}')
    st.dataframe(billing, use_container_width=True, hide_index=True)

with tab4:
    st.markdown("#### Attendance and overtime")
    attendance["Regular_Hours"] = pd.to_numeric(attendance["Regular_Hours"], errors="coerce").fillna(0)
    attendance["Overtime_Hours"] = pd.to_numeric(attendance["Overtime_Hours"], errors="coerce").fillna(0)
    a1, a2 = st.columns(2)
    a1.metric("Attendance records", len(attendance))
    a2.metric("Overtime hours", f'{attendance["Overtime_Hours"].sum():,.1f}')
    st.dataframe(attendance, use_container_width=True, hide_index=True)

with tab5:
    st.markdown("#### Work order register")
    st.metric("Overdue, not completed", int(wo_view["Is_Overdue"].sum()))
    st.dataframe(wo_view, use_container_width=True, hide_index=True)

with tab6:
    st.markdown("#### Download processed report")
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        docs_view.to_excel(writer, sheet_name="Documents", index=False)
        procurement.to_excel(writer, sheet_name="Procurement", index=False)
        billing.to_excel(writer, sheet_name="Billing", index=False)
        attendance.to_excel(writer, sheet_name="Attendance", index=False)
        wo_view.to_excel(writer, sheet_name="WorkOrders", index=False)
    st.download_button("Download Excel report", data=output.getvalue(),
                       file_name="siteops_report.xlsx",
                       mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

st.caption("SiteOps is an independent community project. It is not affiliated with or endorsed by any employer, airport operator or software vendor.")
