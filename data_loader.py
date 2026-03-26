import pandas as pd
import pyodbc

def get_connection():
    return pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=PWVDDBSQLA055.NGIC.COM;"
        "DATABASE=D2CDIRECTMAIL;"
        "Trusted_Connection=yes;"
    )

def load_rollout_data():

    query = """
    SELECT
        RO.IID_TXT,
        RO.CAMPAIGN_NUMBER,
        RO.MAILTYPE,
        CAST(RO.DIR_FP_QT AS INT) AS DIR_FP_QT,
        TRY_CAST(S.SCORE AS FLOAT) AS SCORE
    FROM D2CDIRECTMAIL.DBO.GS_ROLLOUT_RESULTS_VIEW RO WITH (NOLOCK)

    LEFT JOIN D2CDIRECTMAIL.DBO.GS_EVENT_RO_W_SCORE S WITH (NOLOCK)
        ON RO.IID_TXT = S.IID
        AND LEFT(S.CAMPAIGN_NUMBER, 4) = LEFT(RO.CAMPAIGN_NUMBER, 4)

    WHERE TRY_CAST(S.SCORE AS FLOAT) IS NOT NULL
      AND LEFT(RO.CAMPAIGN_NUMBER, 4) >= '2500'
    """

    conn = get_connection()
    df = pd.read_sql(query, conn)
    conn.close()

    df.columns = [c.strip().upper() for c in df.columns]

    return df