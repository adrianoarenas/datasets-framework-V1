from datetime import timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator


from datetime import datetime

import pandas as pd
from sqlalchemy import create_engine

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


# Scraping (excecute scraper) + removing duplicates
def scrape_and_clean(job_titles):
    general_dataframe = create_dataframe()
    for job in job_titles:
        general_dataframe = general_dataframe.append(main(job))
        general_dataframe.drop_duplicates(subset=['job_url'], inplace=True)
    return (general_dataframe)


def run_scrape_and_db():
    # Etablishing connection with the database
    engine = create_engine('postgresql://****@localhost:****/*****')
    con = engine.connect()

    # Scrape
    final_jobs = scrape_and_clean(['data scientist', 'data engineer', 'data analyst'])

    # Append to the database
    final_jobs.to_sql('jobs', engine, if_exists='append', index=False)

    # Close Connection
    con.close()

def extract_from_db():
    #define today's date to pull today's jobs from the database
    date = datetime.today().strftime('%Y-%m-%d')
    #define the connection to postgres
    engine = create_engine('postgresql://****@localhost:*****/*****')
    #define the query
    query = '''select * 
                from jobs 
                where posting_date = '{}' '''
    #import the data
    df = pd.read_sql_query(query.format(date),
                           con=engine)
    return(df)

def filter_job_descriptions(df):
    #Everthing gets lowercased
    df['description'] = df['description'].str.lower()
    #We filter for python, sql and ml as those are my interests
    python_filter = df['description'].str.contains(("python"))
    sql_filter = df['description'].str.contains(("sql"))
    ml_filter = sql_filter = df['description'].str.contains(("machine learning"))
    #Apply the filters defined above
    desc_filtered = df[(python_filter & sql_filter) | ml_filter]
    #Filter out senior roles
    title_filtered = desc_filtered[~desc_filtered['job_title'].str.contains("Manager|Senior|Lead|Principal")]
    #Final df to be sent will just contain the title, the company and the url
    final_df = title_filtered[['job_title','company','job_url']]
    return(final_df)

def email_filtered_jobs(final_df):
    date = datetime.today().strftime('%Y-%m-%d')
    EMAIL_ADDRESS = "********"
    EMAIL_PASSWORD = '**********'

    msg = MIMEMultipart()

    msg['Subject'] = "{} found jobs".format(date)
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = '*******'

    html = """Hi Adriano,\n\n
            Find attached the jobs found with your desired requirements \n\n
            <html>
              <head></head>
              <body>
                {}
              </body>
            </html>
            """.format(final_df.to_html(index=False))

    part1 = MIMEText(html, 'html')
    msg.attach(part1)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    server.sendmail(EMAIL_ADDRESS, '**********', msg.as_string())

def main_email_execute():
    df = extract_from_db()
    final_df = filter_job_descriptions(df)
    email_filtered_jobs(final_df)



default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2021, 4, 13, 22, 00),
    'email': ['*******'],
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 1,
    'retry_delay': timedelta(minutes=15)
}

dag = DAG(
    dag_id='indeed_scraper_dag',
    default_args=default_args,
    description='Scraping indeed and inputting to database',
    schedule_interval="00 22 * * *",
    catchup=False
)

run_etl = PythonOperator(
    task_id='scrape_and_saveDB',
    python_callable=run_scrape_and_db,
    dag = dag
)

run_email = PythonOperator(
    task_id='load_db_filter_and_email',
    python_callable=main_email_execute,
    dag=dag
)

run_etl >> run_email
