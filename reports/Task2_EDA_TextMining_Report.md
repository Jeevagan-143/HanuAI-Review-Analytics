# HanuAI — Task 2: EDA & Text Mining

## Dataset overview
- Rows after duplicate removal: 1000
- Columns: 25
- Duplicate rows removed: 0
- Text fields used: CAUSAL_VERBATIM, CORRECTION_VERBATIM, CUSTOMER_VERBATIM, Additional Context

## Data quality
- Columns with missing values: 9
- Total missing cells: 5975

## Text analysis
- Average text word count: 66.71
- Number of exploratory clusters: 5

## Frequent terms
- radio: 0.2963
- customer: 0.0769
- replaced: 0.0748
- screen: 0.0704
- states: 0.0655
- replace: 0.0616
- tac: 0.0615
- replaced radio: 0.0611
- code: 0.0591
- customer states: 0.0581
- usb: 0.0573
- internal: 0.0539
- vehicle: 0.0531
- check: 0.0518
- replace radio: 0.0515
- codes: 0.0506
- programmed: 0.0499
- program: 0.0494
- ok: 0.0481
- camera: 0.0481

## Business interpretation
- Review the category charts to identify frequently reported components or issue types.
- Review frequent terms and cluster examples to investigate recurring service concerns.
- Treat clusters as exploratory groups, not confirmed root causes.
- Validate suspected trends with domain experts before making operational decisions.

## Outputs
- cleaned_vehicle_records.csv
- missing_values.csv
- data_summary.csv
- HanuAI_Task2_Analysis.xlsx
- PNG charts