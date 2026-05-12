---
name: linkedin-job-change-weekly-report
description: Weekly LinkedIn Sales Navigator job change report for 1st-degree connections, saved to Daily Accounts folder
---


## Weekly LinkedIn Job Change Report

**Objective:** Check LinkedIn Sales Navigator for 1st-degree connections who have changed jobs, compile the results into an Excel report, and save it to the Daily Accounts folder.

**Steps:**

1. Open Chrome and navigate to LinkedIn Sales Navigator:
   https://www.linkedin.com/sales/search/people
   - Wait for the page to fully load (3-4 seconds)

2. Apply the following two filters using the filter panel on the left:
   - Under "Connection": select "1st Degree Connections"
   - Under "Recent Updates": toggle ON "Changed Jobs" (this shows ~202 results)
   - If the filter panel is collapsed, click "Expand filter panel" first

3. Read all visible results from page 1 of the filtered results. For each person, capture:
   - Full name
   - Current job title
   - Current company
   - Location
   - Tenure in current role
   - Tenure at current company

4. Navigate to pages 2, 3, 4, and 5 (use the page navigation at the bottom) and collect the same data.

5. Open the existing report file at:
   /sessions/[session-id]/mnt/Daily Accounts/LinkedIn_Job_Change_Report.xlsx
   
   If the file does not exist, create a new one using openpyxl with these sheets:
   - "Weekly Summary" — key stats (total connections, number who changed jobs, date)
   - "Changed Jobs Detail" — one row per person with columns: Name, Title, Company, Location, Tenure in Role, Tenure at Company, Status (🔴 Very Recent if < 6 months, 🟡 Within 1 Year if 6-12 months)
   - "Tracking Log" — one row per week to track changes over time

6. Update the spreadsheet:
   - Add a new row to "Tracking Log" with today's date, total connections count, changed jobs count, and any notable new changes since last week
   - Refresh "Changed Jobs Detail" with the current week's data
   - Update the date in "Weekly Summary"

7. Save the updated file to:
   /sessions/[session-id]/mnt/Daily Accounts/LinkedIn_Job_Change_Report.xlsx

8. Send an email summary to bcosihardware@gmail.com with:
   - Subject: "LinkedIn Weekly Job Change Report — [Today's Date]"
   - Body: Plain summary listing total connections who changed jobs, and the top 10 most recently changed (shortest tenure), with their name, new company, and new title
   - Note: If email sending is not available, save the summary as a .txt file in the Daily Accounts folder instead

**Important notes:**
- The "Changed Jobs" filter in Sales Navigator shows connections who changed jobs in the past 90 days
- If the ZoomInfo extension blocks clicking, try using keyboard navigation (Tab + Space) to toggle the filter checkbox
- The user's email for the report is: bcosihardware@gmail.com
- Save path: the mounted workspace folder (Daily Accounts)
- If Sales Navigator requires login, navigate to linkedin.com/sales/login first — credentials are managed by the user's browser session
