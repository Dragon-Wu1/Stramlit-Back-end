import streamlit as st
import snowflake.connector
from PIL import Image
import pandas as pd
import time


def init_connection():
    return snowflake.connector.connect(
        **st.secrets["snowflake"], client_session_keep_alive=True
    )
# def callback1():
# Search
#   st.session_state['btn_clicked'] = True


def callback(*list1):
    st.session_state['add_course'] = False
    if 'myList' not in st.session_state:
        st.session_state['myList'] = list1
    else:
        st.session_state['myList'] = list1


def add_show():
    st.session_state['add_course'] = True


def query_add_course():
    db = init_connection()
    cursor = db.cursor()
    sql = 'Select instructor_id as ID,name as Instructor_Name, email as Email from instructors;'
    cursor.execute(sql)
    db.commit()
    df2 = pd.read_sql(sql, con=db)
    return df2


def add_new_course_save():
    if not st.session_state['add_course']:
        list2 = ['Instructor ID', 'Course Code', 'Course Name', 'Course Department', 'Description', 'Prerequisites',
                     'Textbook', 'Reference', 'Major', 'Objectives', 'Covered', 'Objectives Outcomes']
        lt1 = st.session_state['myList']
        l1 = {lt1[1]: lt1}
        df = pd.DataFrame(l1, index=list2)
        st.subheader(lt1[1])
        st.table(df)
        left_column, right_column = st.columns([5, 1])
        with left_column:
            if st.button("Back", key='add_back', on_click=add_show):
                pass
        with right_column:
            conffirm = st.button('Confirm')
        if conffirm:
            db = init_connection()
            cursor = db.cursor()
            sql = " select name, password, email from instructors where instructor_id = '%s'" % (lt1[0])
            cursor.execute(sql)
            db.commit()
            dat = cursor.fetchall()
            dat = dat[0]
            instructor_name = dat[0]
            instructor_password = dat[1]
            instructor_email = dat[2]
            #st.write(dat)
            #st.write(instructor_name)
            #st.write(instructor_password)
            #st.write(instructor_email)
            sql1 = "INSERT INTO INSTRUCTORS (instructor_id, name, course, password, email) values ('%s', '%s', '%s', " \
                   "'%s', '%s')" % (lt1[0], instructor_name, lt1[1], instructor_password, instructor_email)
            cursor.execute(sql1)
            db.commit()
            sql2 = "insert into course (id_name, course_name, course_dept, description, prerequisites, textbook, " \
                   "reference, major_pre, objectives, covered, objectives_outcomes) values ('%s', '%s', '%s','%s'," \
                   "'%s','%s','%s','%s','%s','%s','%s')" % (lt1[1], lt1[2], lt1[3], lt1[4], lt1[5], lt1[6], lt1[7], lt1[8], lt1[9], lt1[10], lt1[11])
            cursor.execute(sql2)
            db.commit()
            st.success("input successfully")
            st.session_state['add_course'] = True


def add_course_form():
    if st.session_state['add_course']:
        st.title('Filled the information in below.')
        df2 = query_add_course()
        st.write(df2)
        instr_id = st.text_input("Instructor ID")
        course_code = st.text_input("Course Code")
        course_name = st.text_input("Course Name")
        course_dept = st.text_input("Course Department")
        catalog_description = st.text_area("Catalog Description")
        prerequisites = st.text_area("Prerequisites")
        textbook = st.text_area("Textbook(s) and other required materia")
        references = st.text_area("References")
        major_prerequisites_by_topic = st.text_area("Major prerequisites by topic")
        course_objectives = st.text_area("Course objectives")
        topics_covered = st.text_area("Topics covered")
        objectives_and_outcomes = st.text_area("Relationship to CEE, EEE and EME program objectives and outcomes")
        submit = st.button("Save", on_click=callback, args=[instr_id, course_code, course_name, course_dept,
                                                                catalog_description, prerequisites, textbook,
                                                                references, major_prerequisites_by_topic,
                                                                course_objectives,
                                                                topics_covered,
                                                                objectives_and_outcomes])
