# Data card

## Dataset 1: Alibeyköy hourly air quality measurements

- **Source and URL:** Istanbul Metropolitan Municipality (IBB), Air Quality Monitoring Center. https://havakalitesi.ibb.gov.tr/STN/VWSTN_Reports/DynamicReport
- **License:** Not yet confirmed. Public access does not establish permission to redistribute the data.
- **Date accessed:** 2026-10-22.
- **Time range and granularity:** 2026-10-15 14:00 to 2026-10-22 14:00, inclusive. Hourly measurements. The export does not explicitly specify the time zone.
- **Size:** 169 timestamped rows and 6 populated data columns: date, time, CO, O3, PM10, and SO2. The worksheet also contains four header rows and unused formatted columns. No cleaned dataset has been saved yet.
- **Columns used:** Date, time, and Alibeyköy PM10 concentration (µg/m³) are selected for the planned analysis.
- **Known issues:** PM10 has 149 numeric observations and 20 missing values, giving 88.2% coverage. No duplicate date–time pairs were found. The first and last calendar days are partial days. Validation status has not been confirmed for individual measurements. One week cannot support seasonal comparisons.
- **Cleaning decisions and why:** No changes have been made to the original workbook. Planned steps are to remove report headers, retain station and unit information, and prepare a consistent timestamp column. The date cells already include time, so the separate time column must not be added twice. Missing measurements will remain missing rather than being replaced with zero. Daily aggregation rules will be documented before analysis.
- **How to regenerate:** - **How to regenerate:** Open the source page, select Alibeyköy and the date–time range from 2026-10-15 14:00 to 2026-10-22 14:00, and query the measurements. Access to this period may require an active account once it falls outside the public last-week window. No automated download or cleaning script has been implemented yet.
