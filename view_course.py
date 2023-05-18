import streamlit as st
import pymysql
import pandas as pd
import time

if 'btn_clicked' not in st.session_state:
    st.session_state['btn_clicked'] = False


def view_show():
    st.session_state['view_course'] = True


def callback(course_df, id_name):
    st.session_state['view_course'] = False
    if st.session_state['view_course'] == False:
        left_column, right_column = st.columns([4, 1])
        with left_column:
            st.subheader(id_name)
        with right_column:
            back_view = st.button(label='Back', on_click=view_show)
        st.table(course_df.loc[id_name])



def callback1():
    #Search
    st.session_state['btn_clicked'] = True


@st.cache_resource
def time_consuming_func():
    time.sleep(3)
    return


conn = pymysql.connect(host='127.0.0.1', user='root', passwd='a098765', port=3306, db='course_management')


def execute_query(query, params=None):
    cursor = conn.cursor()
    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)
    return cursor.fetchall()


faculty_query = """
    SELECT faculty_name, department1, department2, department3, department4, department5, department6, department7
    FROM faculty
"""
faculties = execute_query(faculty_query)

faculty_dict = {}
for faculty in faculties:
    faculty_name = faculty[0]
    department1 = faculty[1]
    department2 = faculty[2]
    department3 = faculty[3]
    department4 = faculty[4]
    department5 = faculty[5]
    department6 = faculty[6]
    department7 = faculty[7]
    faculty_dict[faculty_name] = [department1, department2, department3, department4, department5, department6,
                                  department7]


def get_course_info(faculty, department):
    course_query = """
        SELECT id_name, course_name, offering_unit, offering_department, pre_requisite, credits, course_type, ge_area, suggested_year_of_study, duration, grading_system, medium_of_instruction, course_description, intended_learning_outcomes
        FROM course_information
        WHERE offering_unit = %s AND offering_department = %s
    """
    params = (faculty, department)
    courses = execute_query(course_query, params)
    return courses


def view_course_information():
    if 'view_course' not in st.session_state:
        st.session_state['view_course'] = True
    if st.session_state['view_course']:
        st.title('Course information')
        if 'Search' not in st.session_state:
            st.session_state['Search'] = False
        if 'btn_clicked' not in st.session_state:
            st.session_state['btn_clicked'] = False
        faculty = st.selectbox('Offering Unit', list(faculty_dict.keys()))
        departments = faculty_dict[faculty]
        department = st.selectbox('Offering Department', departments)

        if st.button("Search", on_click=callback1) or st.session_state['btn_clicked']:
            courses = get_course_info(faculty, department)
            if courses:
                course_list = []
                id_name = ' '
                for course in courses:
                    id_name = course[0]
                    course_info = {
                        'id_name': course[0],
                        'Course Name': course[1],
                        'Offering Unit': course[2],
                        'Offering Department': course[3],
                        'Prerequisites': course[4],
                        'Credits': course[5],
                        'Course Type': course[6],
                        'GE Area': course[7],
                        'Suggested Year of Study': course[8],
                        'Duration': course[9],
                        'Grading System': course[10],
                        'Medium of Instruction': course[11],
                        'Course Description': course[12],
                        'Intended Learning_outcomes': course[13]
                    }
                    course_list.append(course_info)

                if course_list:
                    course_df = pd.DataFrame(course_list, index=[course['id_name'] for course in course_list])
                    id_name = st.selectbox('Select the course', list(course_df.index))
                    print(course_df.index)
                    if st.button('View', on_click=callback, args=(course_df, id_name)):
                        st.session_state['button_clicked'] = True
                    else:
                        st.session_state['button_clicked'] = False

