# SiteOps – Facility Management & Document Control Toolkit

SiteOps is an independent, open-source starter project for organizing common site-administration workflows in facility management. It reflects practical workflows such as document registers, material requisitions, purchase-request follow-up, monthly billing, attendance and maintenance work orders.

## Why this project exists

Small facility-management teams often coordinate information across spreadsheets, emails and manual reports. SiteOps demonstrates how a simple Python dashboard can bring common trackers together and produce a consolidated Excel report.

## Features

- Document register with revision, status, recipient, due date and submission date
- Procurement tracker for material requests, purchase requests and quotation follow-up
- Monthly billing tracker with invoice, paid and outstanding values in OMR
- Attendance and overtime summary
- Maintenance work-order tracker with overdue identification
- Excel workbook upload and downloadable consolidated report
- Fictional sample data for safe testing

## Quick start

1. Install Python 3.10 or later.
2. Download or clone this repository.
3. Open a terminal in the project folder.
4. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

5. Run the dashboard:

   ```bash
   streamlit run app.py
   ```

6. Upload `sample_data.xlsx` in the browser.

## Workbook format

The workbook must contain these five worksheets and column headers:

- `Documents`: `Document_No`, `Title`, `Date`, `Revision`, `Status`, `Recipient`, `Due_Date`, `Submission_Date`
- `Procurement`: `Request_No`, `Material_Description`, `Category`, `Quantity`, `Unit`, `Request_Date`, `Status`, `Requested_By`
- `Billing`: `Invoice_No`, `Billing_Month`, `Service`, `Invoice_Amount_OMR`, `Paid_Amount_OMR`, `Status`, `Submission_Date`
- `Attendance`: `Date`, `Employee_ID`, `Designation`, `Attendance_Status`, `Regular_Hours`, `Overtime_Hours`
- `WorkOrders`: `Work_Order_No`, `Description`, `Discipline`, `Priority`, `Status`, `Reported_Date`, `Due_Date`, `Assigned_Team`

Use the included `sample_data.xlsx` as a template. Keep the column names unchanged.

## Example status values

These are suggestions, not enforced rules:

- Documents: `Draft`, `Submitted`, `Under Review`, `Approved`, `Rejected`
- Procurement: `Requested`, `Quotation Received`, `Pending Approval`, `PO Issued`, `Received`
- Work orders: `Open`, `In Progress`, `Completed`, `On Hold`

## Project structure

```text
siteops-facility-management-toolkit/
├── app.py
├── requirements.txt
├── README.md
├── LICENSE
├── .gitignore
└── sample_data.xlsx
```

## Privacy and responsible use

- The sample workbook contains fictional records only.
- Do not upload confidential employer, client, supplier or employee data to a public repository or an online app.
- Use anonymized or synthetic records when demonstrating the project.
- This project is an independent learning/community project and is not affiliated with any employer or airport operator.

## Current limitations

- This is an early version intended for learning and community feedback.
- It does not connect to SAP, Maximo, email, payroll or any employer system.
- It does not provide user accounts, role-based access or audit logging.
- Overdue calculations use the computer's current date.
- Data is processed for the current session; it is not stored in a database.

## Roadmap

- [ ] Add configurable status lists and validation
- [ ] Add document revision history
- [ ] Add monthly trend charts
- [ ] Add a printable PDF management summary
- [ ] Add automated data-quality checks
- [ ] Add unit tests for KPI calculations
- [ ] Improve accessibility and mobile layout

## Contributing

Issues, bug reports, documentation improvements and pull requests are welcome. Please use synthetic data in examples and include steps to reproduce bugs.

## License

MIT. See `LICENSE`.
