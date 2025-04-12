# MYTHILIPRIYA96-Cricsheet-Match-Data-Analysis
# Cricsheet Match Data Analysis

A complete end-to-end cricket data analysis project using [Cricsheet](https://cricsheet.org/) JSON files. This project extracts, transforms, and analyzes ball-by-ball data from international matches (Test, ODI, T20),IPL stores it in a SQL database, and presents insights via Streamlit dashboards, EDA  Dashboard ,Power Point Presentation  and Power BI visualizations.

##  Features

 Parse and normalize Cricsheet JSON data
 Create SQL tables for match types (Test, ODI, T20)
 Generate analytical SQL queries (top scorers, win %)
 Visualize trends using Python (Matplotlib, Seaborn, Plotly)
 Build interactive dashboards with Streamlit and Power BI
 Modular code using OOP principles

## Business Use Cases

 **Player Performance Analysis** – runs, wickets, economy across formats
 **Team Insights** – win/loss records, head-to-head
 **Match Outcomes** – margin of victories, toss impact
 **Strategic Decision-Making** – support coaches, analysts
 **Fan Engagement** – explore data using dashboards

##  Tech Stack

 **Python** – pandas, json, matplotlib, seaborn, plotly
 **SQL** – MySQL (TiDB Cloud) 
 **Streamlit** – frontend for interaction
 **Power BI** – visual dashboards
 **Cricsheet** – open-source match data

##  Project Structure
cricsheet-analysis/ 
├── data/ # Raw Cricsheet JSON files 
├── scripts/ # Python scripts for parsing and processing  
├── json_parser. 
├── db_insert 
├── sql/ # SQL DDL and query 
├── create_tables 
├──  analysis_queries 
├── streamlit_app/ # Streamlit dashboard
├── 20 sql
├── cricsheet_dashboard.py
├── cricket_EDA_Dashboard_preesentation.pptx files
├── powerbi/ # cricsheet .pbix files └── README.md 

 data/
This folder contains Cricsheet JSON files (the original data).

Each file is a match: Test, ODI, T20, or IPL.

These files are used as the raw input to your project.

 parser/
Contains Python code to read and clean the JSON files.

Example: match_parser.py reads the innings, deliveries, teams, and players.

It normalizes the nested data into clean tables (like DataFrames or SQL-ready formats).

 db/
Has all SQL files:

create_tables.sql: defines your database schema (tables for matches, players, innings, deliveries, etc.)

insights_queries.sql: stores your analysis queries (e.g., top batsman, win margin by team).

This helps manage the database creation and insights generation.

 visualizations/
Contains a Jupyter notebook (cricsheet_dashboard.py) for Exploratory Data Analysis (EDA).

You create graphs and visual insights using:

matplotlib

seaborn

plotly

Shows trends, player stats, match outcomes, and more.

 streamlit_app/
Your Streamlit dashboard code lives here ( cricsheet_dashboard.py).

Displays real-time match data.

Allows users to interact with the data.

Shows tables, insights, and charts.


 powerbi/
Contains the Power BI cricsheet.pbix file.

This dashboard gives a business-level summary of the match data.

Helps with strategic decision-making using visuals like bar charts, pie charts, and trends.


##  License
MIT License
