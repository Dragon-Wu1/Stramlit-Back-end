import streamlit as st
import snowflake.connector
from PIL import Image
import pandas as pd
import time
import smtplib
import email.message


def init_connection():
    return snowflake.connector.connect(
        **st.secrets["snowflake"], client_session_keep_alive=True
    )


def query():
    db = init_connection()
    cursor = db.cursor()
    sql = 'Select id_name as Course_code, course_name as Course_Name, email as Email,status as Course_Status from course M Join instructors F On M.id_name = F.course;'
    cursor.execute(sql)
    db.commit()
    df2 = pd.read_sql(sql, con=db)
    return df2


def show_revision_form():
    isall = st.checkbox(label="All")
    df2 = query()
    course_name = df2[["COURSE_NAME"]]
    button_list = []
    email_list = []
    name_list = []
    left_column, right_column = st.columns([5, 1])
    with left_column:
        st.table(df2)
    with right_column:
        st.write("<Select Box!>")
        i = 0
        for j in df2.COURSE_CODE:
            j = st.checkbox(j, key=i, value=isall)
            i = i + 1
            button_list.append(j)
    left_column1, right_column1 = st.columns([5, 1])
    with left_column1:
        pass
    with right_column1:
        submit_button = st.button(label='Send')

    if submit_button:
        for t in range(0, len(button_list)):
            if button_list[t]:
                email_list.append(df2.at[t, "EMAIL"])
                name_list.append(df2.at[t, "COURSE_CODE"])
        # st.write(email_list)
        # st.write(name_list)
        st.success("You have successfully send email!")
        # send_email(email_list, name_list)


def send_email(email_list, name_list):
    for i, y in zip(email_list, name_list):
        msg = email.message.EmailMessage()
        sender_email = "dragonhunter9527@gmail.com"
        receiver_email = i  # dragonwu9523@gmail.com
        msg["From"] = sender_email
        msg["To"] = receiver_email
        msg["Subject"] = "Course information"
        msg.add_alternative(
            "<h3>The link for filled the information of course</h3><h4>The link below</h4></br>https://dragon-wu1-streamlit-example-streamlit-app-w04axx.streamlit.app/?cur_nam="+y,
            subtype="html")
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login("dragonhunter9527@gmail.com", "xvkhdwolxkdsocif")
        server.send_message(msg)
        server.close()




