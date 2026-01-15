Automated BI Dashboard Data Pipeline (Python + GitHub Actions + Power BI)

This project demonstrates a fully automated data pipeline that generates daily transactional data, updates it without manual intervention, and refreshes a Power BI dashboard automatically using a GitHub-hosted dataset.
The goal is to simulate a real-world BI workflow where:
    Data grows daily
    IDs are unique and never repeated
    Data quality is enforced at the source
    Dashboards refresh without manual cleanup

1.)	Architecture Overview:
        Python Script (Local / GitHub Actions)
                    ↓
        CSV Dataset (GitHub Repository)
                    ↓
        Power BI (Web Connector)
                    ↓
        Scheduled Dashboard Refresh

2.)	Repository Structure:
        automated-bi-dashboard-data/
          •	data/
              o	amazon.csv           # Production dataset (auto-updated daily)
          •	test/
              o	test_data.csv      # Test dataset (used for local validation)
              o	test_data_1.csv      # Test dataset (used for local validation)
              o	generate__data_powerBi_test_code.py         # Python test data generation script
          •	generate_data.py         # Python data generation script
          •	github/
              o	workflows/
                	daily_update.yml # GitHub Actions automation
          •	README.md
 
3.)	Dataset Description (amazon.csv)
      The dataset simulates Amazon-style product reviews and pricing data.
      Key Columns:
        Column	Description
        product_id	Unique product identifier
        product_name	Name of the product
        category	Product category
        discounted_price	Final selling price (numeric)
        actual_price	Original price (numeric)
        discount_percentage	Discount percentage
        rating	User rating (1–5)
        rating_count	Total ratings per product
        user_id	Unique user identifier
        user_name	Reviewer name
        review_id	Globally unique review ID
        review_title	Review heading
        review_content	Review text
        img_link	Product image URL
        product_link	Product page URL

4.)	Key Design Decisions:
      •	Numeric Prices (BI-Friendly)
          o	Prices are stored as pure numbers, not formatted currency strings.
      •	Why?
          o	Power BI auto-detects numeric types
          o	No manual transformation needed
          o	Refreshes never break
      •	Unique Review IDs (No Duplicates)
      •	Each review ID:
          o	Is generated incrementally
          o	Never repeats across runs
          o	Is derived from the max existing ID
      •	Data Generator (generate_data.py)
          o	The Python script is responsible for:
            	Reading the existing CSV
            	Seeding initial data if the file is empty
            	Adding 10–20 new records per run
            	Cleaning price fields
            	Ensuring unique review IDs
            	Recalculating rating counts
            	Writing data back to CSV
      •	Core Logic Summary
        o	Load existing CSV
        o	If empty → seed base product
        o	Clean price columns (remove ₹, commas)
        o	Find highest existing review ID
        o	Generate 10–20 new reviews
        o	Append data
        o	Save updated CSV
        o	This design ensures idempotent, safe, repeatable runs.
      •	Automation with GitHub Actions Workflow File
        o	.github/workflows/daily_update.yml
        o	What It Does:
          	Runs once per day (or manually)
          	Executes generate_data.py
          	Commits updated CSV back to the repo
          	Pushes changes automatically
        o	Power BI Dashboard Connection
          	Data Source
          	Power BI connects directly to the raw GitHub CSV : https://raw.githubusercontent.com/<username>/<repo>/main/data/amazon.csv

5.)	Connection Method
      •	Power BI → Get Data
      •	Select Web
      •	Paste raw GitHub URL
      •	Load data
      •	Because data is already clean:
  No Power Query transformations needed
      •	Columns auto-detect correctly
      •	Refresh is stable
  Dashboard Refresh Mechanism
      Component	            Frequency
      GitHub Actions	      Daily
      CSV Update	          Daily
      Power BI Refresh	    Scheduled (Daily)

6.)	Local Testing (Best Practice):
      Before automation, the same script can be run locally using: amazon_test.csv
      This allows:
        •	Schema validation
        •	Logic testing
        •	Safe experimentation
        •	Once validated, switching to production is just a file path change.

7.)	What This Project Demonstrates?
      •	Automated data generation
      •	Data quality enforced at source
      •	No manual data entry
      •	End-to-end BI pipeline
      •	Production-style refresh logic

8.)	Real-World Use Case Mapping
        Industry Concept	      This Project
        ETL Pipeline	          Python script
        Data Lake	              GitHub CSV
        Scheduler	              GitHub Actions
        BI Tool	                Power BI
        Incremental Load	      Daily append
        Data Cleansing	        Source-level

 
9.)	System Architecture Diagram:
      High-Level Data Flow
      flowchart LR
        1.	A [Python Data Generator generate_data.py]  B [CSV Dataset amazon.csv]
        2.	B [CSV Dataset amazon.csv]  C [GitHub Repository]
        3.	C [GitHub Repository]  |Raw File URL|  D [Power BI Web Connector]
        4.	D [Power BI Web Connector]  E [Power BI Dataset]
        5.	E [Power BI Dataset]  F[Power BI Dashboard]
        6.	G [GitHub Actions Daily Scheduler]  A [Python Data Generator generate_data.py]

10.)	Architecture Explanation
      •	Python Data Generator:
          o	Generates 10–20 new records per run
          o	Ensures unique IDs
          o	Cleans numeric price fields
          o	Appends data safely to CSV
      •	CSV Dataset (amazon.csv):
          o	Acts as a lightweight data lake
          o	Version-controlled
          o	Updated automatically
      •	GitHub Actions:
          o	Runs the Python script daily
          o	Commits and pushes updated data
          o	No manual intervention
      •	Power BI Web Connector:
          o	Reads the raw GitHub CSV
          o	No transformation required
          o	Schema stays stable
      •	Power BI Dashboard:
          o	Auto-refreshes on schedule
          o	Reflects latest data instantly

Author
Hrishikesh Dixit
Master’s Student – Information Systems
University of Texas at Arlington
