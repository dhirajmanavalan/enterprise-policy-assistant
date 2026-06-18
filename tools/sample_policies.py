# Creates policy text files for RAG pipeline
# Run: python sample_policies.py

import os

os.makedirs("../data/policies", exist_ok=True)


# POLICY 1 — Leave Policy
leave_policy = """
LEAVE POLICY 2026
Company: Enterprise Corp
Department: Human Resources
Version: 2026.1

1. CASUAL LEAVE
Every employee is entitled to 12 casual leaves per calendar year.
Casual leave cannot be carried forward to the next year.
Casual leave can be taken for personal emergencies and personal work.
Maximum 3 consecutive casual leaves can be taken at one time.
Prior approval from manager is required for planned casual leaves.
Casual leave balance will be reset to 12 at the start of every year.

2. SICK LEAVE
Every employee is entitled to 10 sick leaves per calendar year.
Sick leave can be taken when the employee is unwell or injured.
For sick leave more than 3 consecutive days, a medical certificate is required.
Sick leave cannot be carried forward to the next year.
Unused sick leave will lapse at the end of the calendar year.
Sick leave cannot be combined with casual leave without HR approval.

3. EARNED LEAVE
Every employee is entitled to 15 earned leaves per calendar year.
Earned leave is accrued at 1.25 days per month of service.
Earned leave can be carried forward up to a maximum of 30 days.
Minimum 5 earned leaves must be taken in a year.
Earned leave encashment is allowed up to 10 days per year.
Employees with more than 30 carried forward leaves will lose the excess.

4. LEAVE APPLICATION PROCESS
All leave requests must be submitted through the HR portal.
Casual leave must be applied minimum 1 day in advance.
Earned leave must be applied minimum 7 days in advance.
Emergency sick leave can be informed on the same day before 10 AM.
Manager approval is mandatory for all leave types.
Leave without manager approval will be treated as unauthorized absence.

5. LEAVE WITHOUT PAY
If all leaves are exhausted, additional leaves will be treated as Leave Without Pay.
Leave Without Pay requires HR Manager approval.
Salary will be deducted proportionally for LWP days.
Excessive LWP may impact annual performance review.

6. MATERNITY AND PATERNITY LEAVE
Female employees are entitled to 26 weeks of paid maternity leave.
Male employees are entitled to 5 days of paid paternity leave.
Maternity and paternity leave are fully paid and do not impact other leave balances.
Application must be submitted to HR at least 4 weeks before expected date.
Maternity leave can be extended by 4 weeks unpaid with medical recommendation.

7. LEAVE ENCASHMENT
Earned leave encashment is allowed at the time of resignation or retirement.
Maximum 30 days of earned leave can be encashed.
Encashment amount is calculated based on basic salary per day.
Casual and sick leave cannot be encashed.
"""

# POLICY 2 — Travel Policy
travel_policy = """
TRAVEL POLICY 2026
Company: Enterprise Corp
Department: Human Resources
Version: 2026.1

1. DOMESTIC TRAVEL
All domestic travel must be pre-approved by the department manager.
Travel requests must be submitted minimum 3 days in advance.
Economy class air travel is permitted for distances above 500 km.
Train travel AC 2-tier is the standard for overnight journeys.
Bus travel is acceptable for distances below 100 km.
All travel bookings must be done through the company travel desk.

2. TRAVEL ALLOWANCE — DOMESTIC
City Category A (Mumbai, Delhi, Bangalore, Chennai): Rs 3000 per day.
City Category B (Hyderabad, Pune, Kolkata): Rs 2500 per day.
City Category C (Other cities and towns): Rs 2000 per day.
Daily allowance covers meals, local transport, and incidental expenses.
Daily allowance is paid as flat amount without requiring individual bills.

3. HOTEL ACCOMMODATION
Category A cities: Maximum Rs 5000 per night reimbursable.
Category B cities: Maximum Rs 4000 per night reimbursable.
Category C cities: Maximum Rs 3000 per night reimbursable.
Hotel bills must be submitted with original GST invoice.
Employees must stay in company empanelled hotels wherever available.
Luxury hotel stays above the limit require VP approval.

4. INTERNATIONAL TRAVEL
International travel requires approval from department head and HR Director.
Business class air travel is permitted for flights above 8 hours duration.
Economy class for flights below 8 hours even for international travel.
International daily allowance varies by country — refer to HR portal for country rates.
Travel insurance is mandatory for all international travel and arranged by HR.
Visa and passport expenses are fully reimbursable for official international travel.

5. REIMBURSEMENT PROCESS
All travel expense claims must be submitted within 7 days of return.
Original bills and receipts are mandatory for all reimbursement.
Reimbursement will be processed within 15 working days of claim submission.
Expenses submitted without original bills will not be reimbursed.
Travel advance can be taken from accounts department before travel.
Unused travel advance must be returned within 3 days of return.

6. LOCAL CONVEYANCE
Cab and auto receipts are reimbursable for official local travel.
Personal vehicle usage reimbursement: Rs 10 per km for two-wheeler.
Personal vehicle usage reimbursement: Rs 15 per km for four-wheeler.
Metro, bus, and local train tickets are fully reimbursable.
Cab booking through company account does not require reimbursement claim.
Personal cab bookings must have original receipts for reimbursement.
"""

# POLICY 3 — Work From Home Policy
wfh_policy = """
WORK FROM HOME POLICY 2026
Company: Enterprise Corp
Department: Human Resources
Version: 2026.1

1. ELIGIBILITY FOR WFH
All permanent employees who have completed 6 months of service are eligible for WFH.
Probationary employees during their first 6 months are not eligible for WFH.
Contract and temporary employees require special written approval for WFH.
Employees with active performance improvement plans are not eligible for WFH.

2. WFH DAYS ALLOWED
Employees are allowed maximum 2 WFH days per week.
WFH days cannot be on Monday or Friday without special manager approval.
WFH is not permitted on days with mandatory all-hands or team meetings.
Maximum 8 WFH days per month are allowed per employee.
WFH cannot be taken on consecutive weeks for more than 4 days total.

3. WFH APPROVAL PROCESS
WFH request must be submitted through the HR portal under WFH section.
Request must be submitted minimum 1 day in advance for planned WFH.
Manager approval is required before the WFH day begins.
Emergency WFH due to unforeseen circumstances can be approved on the same day by manager via message.
WFH without approval will be marked as absent.

4. WORK EXPECTATIONS DURING WFH
Employee must be available on all communication channels during work hours.
Work hours remain 9 AM to 6 PM during WFH same as office hours.
Employee must attend all scheduled video calls and team meetings with camera on.
Deliverables and productivity standards remain exactly the same as office work.
Response time to messages and emails must be within 30 minutes during work hours.
Lunch break is from 1 PM to 2 PM only during WFH.

5. EQUIPMENT AND CONNECTIVITY
Company will not provide additional equipment or devices for WFH purpose.
Employee is fully responsible for stable and reliable internet connectivity.
VPN must be used at all times for accessing company systems from home.
Any data security breach or policy violation during WFH is the employee responsibility.
Company laptop must be used for all official work during WFH.
Personal devices must not be used for accessing company confidential data.

6. WFH REVOCATION AND PENALTIES
Manager can revoke WFH privileges immediately if productivity is impacted.
Repeated WFH violations will result in permanent WFH access removal.
HR has the right to review, audit, and cancel WFH arrangements at any time.
Misuse of WFH policy will lead to disciplinary action.
Three violations in a quarter will result in WFH suspension for that quarter.
"""

# POLICY 4 — Insurance Policy
insurance_policy = """
INSURANCE POLICY 2026
Company: Enterprise Corp
Department: Human Resources
Version: 2026.1

1. HEALTH INSURANCE
All permanent employees are covered under group health insurance from day 1 of joining.
Coverage amount is Rs 5 lakhs per employee per year.
Family floater option is available — spouse and up to 2 dependent children can be added.
Additional family members such as parents can be added at employee cost with 50 percent premium sharing.
Insurance coverage is active as long as the employee is on company rolls.

2. WHAT IS COVERED UNDER HEALTH INSURANCE
Hospitalization expenses including room rent, doctor fees, surgery, and medicines are covered.
Pre-hospitalization expenses covered for 30 days before admission.
Post-hospitalization expenses covered for 60 days after discharge.
Day care procedures that do not require 24-hour hospitalization are fully covered.
Maternity expenses including delivery and newborn care covered up to Rs 50000.
Pre-existing diseases are covered after 2 years of continuous policy with company.
Ambulance charges up to Rs 2000 per hospitalization are covered.

3. INSURANCE CLAIM PROCESS
For planned hospitalization inform HR and insurance company 3 days in advance for cashless treatment.
For emergency hospitalization inform HR within 24 hours of admission.
Cashless treatment facility is available at all network hospitals empanelled with insurer.
For non-network hospitals pay first and claim reimbursement with original bills.
Reimbursement claims must be submitted within 30 days of hospital discharge.
Required documents: Original bills, discharge summary, doctor prescriptions, and diagnostic reports.
Claims submitted after 30 days will be rejected by insurer.

4. LIFE INSURANCE
All permanent employees are covered under group term life insurance.
Coverage amount is 3 times the annual CTC of the employee.
Nominee details must be submitted to HR within 30 days of joining.
In case of employee death coverage amount is paid to the registered nominee.
Coverage automatically ends on the last working day of employment.
Suicide and self-inflicted injury are not covered under life insurance.

5. PERSONAL ACCIDENT INSURANCE
Personal accident cover of Rs 10 lakhs for all employees.
Covers accidental death and permanent total disability.
Partial disability is covered proportionally as per the policy terms table.
Accident during official travel is fully covered.
Accident during personal travel is also covered under this policy.
Claims must be submitted within 7 days of accident occurrence.

6. INSURANCE ENROLLMENT AND CHANGES
New employees must submit insurance enrollment form within 30 days of joining date.
Late enrollment after 30 days will result in coverage starting from next renewal cycle.
Family addition requests must be submitted within 30 days of marriage or childbirth.
Changes to nominee details must be submitted in writing to HR department.
Annual policy renewal happens on April 1st every year.
Employees must verify their coverage details every year during renewal.
"""


# Save as .txt files
policies = {
    "leave_policy.txt": leave_policy,
    "travel_policy.txt": travel_policy,
    "wfh_policy.txt": wfh_policy,
    "insurance_policy.txt": insurance_policy,
}

for filename, content in policies.items():
    filepath = os.path.join("../data/policies", filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content.strip())
    print(f"Created: {filepath}")

print("")
print("=" * 50)
print("  ALL 4 POLICY FILES CREATED SUCCESSFULLY")
print("=" * 50)
print("  Location : data/policies/")
print("  Files    : leave_policy.txt")
print("           : travel_policy.txt")
print("           : wfh_policy.txt")
print("           : insurance_policy.txt")
print("=" * 50)