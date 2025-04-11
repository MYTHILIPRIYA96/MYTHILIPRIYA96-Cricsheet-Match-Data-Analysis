import streamlit as st
import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from sqlalchemy import create_engine
from pptx import Presentation
import os
print(os.path.exists(r"C:\Users\mythi\Downloads\isrgrootx1.pem"))

# Define db_config and get_connection
def db_config():
    return {
        'host': 'gateway01.ap-southeast-1.prod.aws.tidbcloud.com',
        'port': 4000,
        'user': '342521.root',
        'password': 'asderfIT3',
        'database': 'cricsheet_analysis',
        'ssl_ca' : 'True',
        'connect_timeout': 30
        }

def get_connection():
    connection = mysql.connector.connect(**db_config())
    return connection

#Define Database class BEFORE using it
class Database:
    def __init__(self,conn):
        self.con = conn
        self.cursor = self.con.cursor(dictionary=True)

    def fetch_all(self, table_name):
        query = f"SELECT * FROM {table_name}"
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def fetch_query(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def fetch_df(self, query):
        return pd.read_sql(query, con=self.con)

    def close(self):
        
        self.cursor.close()
        self.con.close()

# Initialize DB connection
if 'db_connection' not in st.session_state:
    st.session_state['db_connection'] = get_connection()

conn = st.session_state['db_connection']
db = Database(conn)

# Load CSVs correctly
df_ipl = pd.read_csv(r"C:\Users\mythi\Downloads\JSON\IPL.csv", low_memory=False)
df_test = pd.read_csv(r"C:\Users\mythi\Downloads\JSON\Test.csv", low_memory=False)
df_odi = pd.read_csv(r"C:\Users\mythi\Downloads\JSON\ODI.csv", low_memory=False)
df_t20 = pd.read_csv(r"C:\Users\mythi\Downloads\JSON\T20.csv", low_memory=False)

# Streamlit UI
st.set_page_config(page_title="Cricsheet Analysis Dashboard", layout="wide")
st.title("cricsheet Match Data Analysis  Dashboard")
st.write("Explore match insights via SQL Queries , EDA Visualizations , Presentation and Power BI Dashboard.")
def main():
    menu = st.sidebar.selectbox("Select Action", ["Home" , "SQL Queries", "EDA", "View Presentation","Power BI Dashboard"])
#  Home Page
    if menu == "Home":
        st.header("Welcome to Cricsheet Dashboard")
        st.markdown(""" View SQL-based insights.
     Visualize data with EDA.
        powerpoint  Presentation.
     Analyze team & player performance.""")

#  SQL Query Interface 
    elif menu == "SQL Queries":
        st.subheader("SQL Query Explorer")
        query_options = [
            "Query 1: Top 10 Batsmen by Total Runs in IPL Matches",
            "Query 2: Top 10 Wicket Takers in T20 Matches",
            "Query 3: Team with Highest Win Count in Test Matches",
            "Query 4: Most Matches Played by Team in ODI",
            "Query 5: Batting Average (Player-wise in IPL)",
            "Query 6: Total Runs by Each Team per Season (T20)",
            "Query 7: Toss Winner vs Match Winner Analysis (Test)",
            "Query 8: Venue with Most Matches Played in ODI",
            "Query 9: Players with Most Sixes in IPL Matches",
            "Query 10: Match Results by Margin of Victory (IPL)",
            "Query 11: Top Partnerships (Batter + Non-striker in T20)",
            "Query 12: Best Performing Venue for Teams (Test)",
            "Query 13: Top 10 High Scoring Matches(IPL)",
            "Query 14: Top 10 Highest Individual Scores in ODI Matches",
            "Query 15: Most Common Toss Decisions in Test Matches",
            "Query 16: Highest Team Scores",
            "Query 17: Most Impactful Bowlers Wickets",
            "Query 18: Compare Average Wickets per Match Across Formats",
            "Query 19: Compare Average Runs per Match Across Formats",
            "Query 20: Most Successful Batting Pairs (Highest Partnerships)"]

        selected_query_option = st.sidebar.selectbox("Select SQL operation:", query_options)

        # SQL Queries Dictionary
        queries = {
            "Query 1: Top 10 Batsmen by Total Runs in IPL Matches": """
                SELECT batter, SUM(runs_batter) AS total_runs
                FROM ipl_matches
                GROUP BY batter
                ORDER BY total_runs DESC
                LIMIT 10;
            """,

            "Query 2: Top 10 Wicket Takers in T20 Matches": """
                SELECT bowler, COUNT(*) AS total_wickets
                FROM t20_matches
                WHERE wicket_type IS NOT NULL AND wicket_type != ''
                GROUP BY bowler
                ORDER BY total_wickets DESC
                LIMIT 10;
            """,

            "Query 3: Team with Highest Win Count in Test Matches": """
                SELECT winner, COUNT(*) AS win_count
                FROM test_matches
                WHERE winner IS NOT NULL
                GROUP BY winner
                ORDER BY win_count DESC;
            """,

            "Query 4: Most Matches Played by Team in ODI": """
                SELECT team, COUNT(*) AS matches_played
                FROM (
                    SELECT team1 AS team FROM odi_matches
                    UNION ALL
                    SELECT team2 AS team FROM odi_matches
                ) AS all_teams
                GROUP BY team
                ORDER BY matches_played DESC;
            """,

            "Query 5: Batting Average (Player-wise in IPL)": """
                SELECT batter, 
                    ROUND(SUM(runs_batter) / NULLIF(COUNT(DISTINCT match_id), 0), 2) AS avg_runs_per_match
                FROM ipl_matches
                GROUP BY batter
                ORDER BY avg_runs_per_match DESC;
            """,

            "Query 6: Total Runs by Each Team per Season (T20)": """
                SELECT season, batting_team, SUM(runs_total) AS total_team_runs
                FROM t20_matches
                GROUP BY season, batting_team
                ORDER BY season, total_team_runs DESC;
            """,

            "Query 7: Toss Winner vs Match Winner Analysis (Test)": """
                SELECT toss_winner, winner, COUNT(*) AS match_count
                FROM test_matches
                GROUP BY toss_winner, winner
                ORDER BY match_count DESC;
            """,

            "Query 8: Venue with Most Matches Played in ODI": """
                SELECT venue, COUNT(*) AS matches_played
                FROM odi_matches
                GROUP BY venue
                ORDER BY matches_played DESC
                LIMIT 5;
            """,

            "Query 9: Players with Most Sixes in IPL Matches": """
                SELECT batter, COUNT(*) AS sixes
                FROM ipl_matches
                WHERE runs_batter = 6
                GROUP BY batter
                ORDER BY sixes DESC
                LIMIT 10;
            """,

            "Query 10: Match Results by Margin of Victory (IPL)": """
                SELECT winner, COUNT(*) AS match_wins, AVG(runs_total) AS avg_runs
                FROM ipl_matches
                GROUP BY winner
                ORDER BY match_wins DESC;
            """,

            "Query 11: Top Partnerships (Batter + Non-striker in T20)": """
                SELECT batter, non_striker, COUNT(*) AS balls_played_together,
                    SUM(runs_total) AS runs_scored
                FROM t20_matches
                GROUP BY batter, non_striker
                ORDER BY runs_scored DESC
                LIMIT 10;
            """,

            "Query 12: Best Performing Venue for Teams (Test)": """
                SELECT batting_team, venue, SUM(runs_total) AS total_runs
                FROM test_matches
                GROUP BY batting_team, venue
                ORDER BY total_runs DESC;
            """,

            "Query 13: Top 10 High Scoring Matches(IPL)": """ 
                SELECT match_id, SUM(runs_total) AS  total_runs 
                FROM ipl_matches
                GROUP BY match_id
                ORDER BY total_runs DESC 
                LIMIT 10
            """,

            "Query 14: Top 10 Highest Individual Scores in ODI Matches": """
                SELECT match_id, batter, SUM(runs_batter) AS highest_score
                FROM odi_matches
                GROUP BY match_id, batter
                ORDER BY highest_score DESC
                LIMIT 10;
            """,

            "Query 15: Most Common Toss Decisions in Test Matches": """
                SELECT toss_decision, COUNT(*) AS count
                FROM test_matches
                GROUP BY toss_decision
                ORDER BY count DESC;
            """,
             
            "Query 16: Highest Team Scores": """
            SELECT match_type, season, batting_team, SUM(runs_total) AS total_score
            FROM (
            SELECT match_type, season, batting_team, runs_total FROM test_matches
            UNION ALL SELECT match_type, season, batting_team, runs_total FROM odi_matches
            UNION ALL SELECT match_type, season, batting_team, runs_total FROM t20_matches
            UNION ALL SELECT match_type, season, batting_team, runs_total FROM ipl_matches
            ) AS scores
            GROUP BY match_type, season, batting_team
            ORDER BY total_score DESC
            LIMIT 10;
            """,

            "Query 17: Most Impactful Bowlers Wickets":"""
            SELECT bowler, 
            COUNT(*) AS total_wickets 
            FROM odi_matches
            WHERE wicket_type IS NOT NULL
            GROUP BY bowler
            ORDER BY total_wickets DESC
            LIMIT 10;
      
            """,
            "Query 18: Compare Average Wickets per Match Across Formats": """
                SELECT 'Test' AS format, ROUND(SUM(CASE WHEN wicket_type IS NOT NULL AND wicket_type != '' THEN 1 ELSE 0 END) / COUNT(DISTINCT match_id), 2) AS avg_wickets
                FROM test_matches
                UNION ALL
                SELECT 'ODI' AS format, ROUND(SUM(CASE WHEN wicket_type IS NOT NULL AND wicket_type != '' THEN 1 ELSE 0 END) / COUNT(DISTINCT match_id), 2) AS avg_wickets
                FROM odi_matches
                UNION ALL
                SELECT 'T20' AS format, ROUND(SUM(CASE WHEN wicket_type IS NOT NULL AND wicket_type != '' THEN 1 ELSE 0 END) / COUNT(DISTINCT match_id), 2) AS avg_wickets
                FROM t20_matches
                UNION ALL
                SELECT 'IPL' AS format, ROUND(SUM(CASE WHEN wicket_type IS NOT NULL AND wicket_type != '' THEN 1 ELSE 0 END) / COUNT(DISTINCT match_id), 2) AS avg_wickets
                FROM ipl_matches;
            """,

            "Query 19: Compare Average Runs per Match Across Formats": """
            SELECT 'Test' AS format, ROUND(SUM(runs_total) / COUNT(DISTINCT match_id), 2) AS avg_runs
            FROM test_matches
            UNION ALL
            SELECT 'ODI' AS format, ROUND(SUM(runs_total) / COUNT(DISTINCT match_id), 2) AS avg_runs
            FROM odi_matches
            UNION ALL
            SELECT 'T20' AS format, ROUND(SUM(runs_total) / COUNT(DISTINCT match_id), 2) AS avg_runs
            FROM t20_matches
            UNION ALL
            SELECT 'IPL' AS format, ROUND(SUM(runs_total) / COUNT(DISTINCT match_id), 2) AS avg_runs
            FROM ipl_matches;""",


            "Query 20: Most Successful Batting Pairs (Highest Partnerships)": """
            SELECT batter, non_striker, SUM(runs_total) AS total_partnership
            FROM (
        SELECT batter, non_striker, runs_total FROM ipl_matches
        UNION ALL
        SELECT batter, non_striker, runs_total FROM t20_matches
        UNION ALL
        SELECT batter, non_striker, runs_total FROM odi_matches
        UNION ALL
        SELECT batter, non_striker, runs_total FROM test_matches
         ) AS partnerships
    GROUP BY batter, non_striker
    ORDER BY total_partnership DESC
    LIMIT 10;
""",

        }
   

# Run the selected query
        if st.button("Run Query"):
            conn = get_connection()
            if conn:
                st.write(f"Running: {selected_query_option}")
                df = pd.read_sql(queries[selected_query_option],conn )
                st.dataframe(df)

# EDA Visualizations
    elif menu == "EDA":
        st.title("Exploratory Data Analysis (EDA) Dashboard")
# Add match type
        df_ipl['match_type'] = 'IPL'
        df_test['match_type'] = 'Test'
        df_odi['match_type'] = 'ODI'
        df_t20['match_type'] = 'T20'
        df = pd.concat([df_ipl, df_test, df_odi, df_t20], ignore_index=True)
# Sidebar selection
        viz_options = [
    "Runs scored by top batters across formats",
    "Most wickets taken by bowlers",
    "Win margin distribution",
    "Toss decision impact",
    "Runs per over trend (Run Rate)",
    "Extras type analysis",
    "Team performance by season",
    "Player dismissal types",
    "Most successful chasing teams",
    "Match locations heatmap"
    ]

        selected_viz = st.sidebar.selectbox("Choose a Visualization", viz_options)

        if st.button("Generate Visualization"):
           st.subheader(selected_viz)

        # Visualization 
           if selected_viz == "Runs scored by top batters across formats":
              top_batters = df.groupby('batter')['runs_batter'].sum().sort_values(ascending=False).head(10)
              fig, ax = plt.subplots(figsize=(10, 5))
              sns.barplot(x=top_batters.values, y=top_batters.index, palette='viridis', ax=ax)
              ax.set_xlabel("Total Runs")
              st.pyplot(fig)

           elif selected_viz == "Most wickets taken by bowlers":
               wickets_df = df[df['wicket_type'].notnull()]
               top_bowlers = wickets_df.groupby('bowler')['player_out'].count().sort_values(ascending=False).head(10)
               fig, ax = plt.subplots(figsize=(10, 5))
               sns.barplot(x=top_bowlers.values, y=top_bowlers.index, palette='magma', ax=ax)
               ax.set_xlabel("Wickets")
               st.pyplot(fig)

           elif selected_viz == "Win margin distribution":
               win_counts = df.groupby(['winner']).size().reset_index(name='wins')
               fig = px.bar(win_counts, x='winner', y='wins', title="Total Wins by Team")
               st.plotly_chart(fig)

           elif selected_viz == "Toss decision impact":
               df['won_toss_and_match'] = df['toss_winner'] == df['winner']
               toss_df = df.groupby('toss_decision')['won_toss_and_match'].mean().reset_index()
               fig, ax = plt.subplots(figsize=(6, 4))
               sns.barplot(data=toss_df, x='toss_decision', y='won_toss_and_match', palette='coolwarm', ax=ax)
               ax.set_ylabel("Win Rate")
               st.pyplot(fig)

           elif selected_viz == "Runs per over trend (Run Rate)":
               over_runs = df.groupby('over')['runs_total'].mean().reset_index()
               fig, ax = plt.subplots(figsize=(10, 5))
               sns.lineplot(data=over_runs, x='over', y='runs_total', ax=ax)
               ax.set_xlabel("Over")
               ax.set_ylabel("Avg Runs")
               ax.grid(True)
               st.pyplot(fig)

           elif selected_viz == "Extras type analysis":
               extras = df['extras_type'].value_counts().reset_index()
               extras.columns = ['extras_type', 'count']
               fig = px.pie(extras, names='extras_type', values='count', title="Extras Type Distribution")
               st.plotly_chart(fig)

           elif selected_viz == "Team performance by season":
               season_wins = df.groupby(['season', 'winner']).size().reset_index(name='wins')
               fig = px.bar(season_wins, x='season', y='wins', color='winner', title="Wins by Team per Season")
               st.plotly_chart(fig)

           elif selected_viz == "Player dismissal types":
               dismissal_df = df[df['wicket_type'].notnull()]
               fig, ax = plt.subplots(figsize=(10, 5))
               sns.countplot(data=dismissal_df, y='wicket_type',
                        order=dismissal_df['wicket_type'].value_counts().index, ax=ax)
               ax.set_xlabel("Count")
               st.pyplot(fig)

           elif selected_viz == "Most successful chasing teams":
               chasing_teams = df[(df['toss_decision'] == 'field') & (df['toss_winner'] == df['winner'])]
               top_chasers = chasing_teams['winner'].value_counts().head(5)
               fig, ax = plt.subplots(figsize=(8, 4))
               sns.barplot(x=top_chasers.values, y=top_chasers.index, palette='YlGnBu', ax=ax)
               ax.set_xlabel("Matches Won Chasing")
               st.pyplot(fig)

           elif selected_viz == "Match locations heatmap":
               city_counts = df['city'].value_counts().reset_index()
               city_counts.columns = ['city', 'matches']
               fig = px.bar(city_counts, x='city', y='matches', title="Match Count by City")
               st.plotly_chart(fig)
    

    elif menu == "View Presentation":
        st.title("Cricket EDA Dashboard Presentation")
        st.subheader("Cricsheet Presentation")

        pptx_path = r"C:\Users\mythi\Downloads\JSON\Cricket_EDA_Dashboard_Presentation.pptx"

        if os.path.exists(pptx_path):
            with open(pptx_path, "rb") as file:
                pptx_bytes = file.read()
            st.download_button(
                label=" Download PowerPoint",
                data=pptx_bytes,
                file_name="Cricsheet_Presentation.pptx",
                mime="application/vnd.openxmlformats-officedocument.presentationml.presentation")
        else:
            st.error("The file 'Cricket_EDA_Dashboard_Presentation.pptx' was not found")

    elif menu == "Power BI Dashboard":
       st.subheader("Power BI Dashboard")

       st.write("Here's the embedded Power BI dashboard. Use filters and visuals to explore team and player performance.")

       with open(r"C:\Users\mythi\OneDrive\Documents\cricsheet.pbix", "rb") as file:
        st.download_button("Download .pbix file", data=file, file_name="cricsheet_dashboard.pbix", mime="application/octet-stream")
  
# Call main()
if __name__ == "__main__":
    main()

