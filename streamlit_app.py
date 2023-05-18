import streamlit as st
import pymysql
from PIL import Image
import pandas as pd
import email.message
import smtplib
import time
from revision import show_revision_form, send_email
from view_course import view_course_information
from user_management import management
from add_new_course import add_course_form,add_new_course_save


st.markdown(""" <style> .css-ejeybu {
gap:2rem;
} </style> """, unsafe_allow_html=True)
st.markdown(""" <style> .css-7czmap{
gap:2rem;
} </style> """, unsafe_allow_html=True)



headerSection = st.container()
mainSection = st.container()
loginSection = st.container()
logOutSection = st.container()
SelectSection = st.container()
InstructorSection = st.container()
CourseSection = st.container()


def view_course_form():
    view_course_information()





def show_instructor_page():
    if st.session_state['Instructor']:
        with InstructorSection:
            management()


def show_course_page():
    if st.session_state['Course']:
        with CourseSection:
            menu = ['View Course', 'Add Course']
            choice = st.sidebar.selectbox('Please select the following functions below', menu)

            if choice == 'View Course':
                view_course_form()

            if choice == 'Add Course':
                if 'add_course' not in st.session_state:
                    st.session_state['add_course'] = True
                    add_course_form()
                else:
                    if st.session_state['add_course']:
                        add_course_form()
                    else:
                        add_new_course_save()




def show_select_page():
    with SelectSection:
        st.sidebar.success("Select a Object below.")
        select = st.sidebar.selectbox(
            'Object', (" ", "Instructor", "Course")
        )
        if select == " ":
            st.session_state['main'] = False
        elif select == 'Instructor':
            st.session_state['main'] = False
            if 'Instructor' not in st.session_state:
                st.session_state['Instructor'] = True
            else:
                st.session_state['Instructor'] = True
            if 'Course' not in st.session_state:
                st.session_state['Course'] = False
            else:
                st.session_state['Course'] = False

        elif select == 'Course':
            st.session_state['main'] = False
            if 'Course' not in st.session_state:
                st.session_state['Course'] = True
            else:
                st.session_state['Course'] = True
            if 'Instructor' not in st.session_state:
                st.session_state['Instructor'] = False
            else:
                st.session_state['Instructor'] = False


def show_main_page():
    if st.session_state['main']:
        with mainSection:
            st.title("Main Page")
            image = Image.open('logo.jpg')
            st.image(image)
            st.header("Supervisor : Prof. Derek WONG ")
            left_column, right_column = st.columns([4, 1])
            with left_column:
                st.subheader("Student : WU MAN CHON")
                st.subheader("Student : CHAN CHON IP")
            with right_column:
                st.subheader(" ")
                st.subheader(" ")
                st.write(" ")
                st.button("Log Out", key="logout", on_click=LoggedOut_Clicked)


def LoggedOut_Clicked():
    st.session_state['loggedIn'] = False


def show_logout_page():
    loginSection.empty()
    with logOutSection:
        st.button("Log Out", key="logout", on_click=LoggedOut_Clicked)


def LoggedIn_Clicked(userName, password):
    db = pymysql.connect(host='127.0.0.1', user='root', passwd='a098765', port=3306, db='course_management')
    cursor = db.cursor()
    sql = "Select password from admins Where name = '%s';" % (userName)
    cursor.execute(sql)
    db.commit()
    df2 = cursor.fetchone()
    df = int(df2[0])
    password = int(password)  # as password is a string and df2 is tuple
    if df is not None and df == password:
        st.session_state['loggedIn'] = True
    else:
        st.session_state['loggedIn'] = False
        st.error("Invalid user name or password")


def show_login_page():
    with loginSection:
        st.header('Course Information Management System ')
        st.subheader("Admin")
        if st.session_state['loggedIn'] == False:
            userName = st.text_input(label="", value="", placeholder="Enter your user name")
            password = st.text_input(label="", value="", placeholder="Enter password", type="password")
            st.button("Login", on_click=LoggedIn_Clicked, args=(userName, password))


with headerSection:
    db = pymysql.connect(host='127.0.0.1', user='root', passwd='a098765', port=3306, db='course_management')
    cursor = db.cursor()
    if 'loggedIn' not in st.session_state:
        st.session_state['loggedIn'] = False
        show_login_page()
    else:
        if st.session_state['loggedIn']:
            if 'main' not in st.session_state:
                st.session_state['main'] = True
                # st.write(1)
                show_main_page()
                #show_logout_page()
                # st.write(2)
                show_select_page()
                # st.write(3)
            else:
                if st.session_state['main'] == True:
                    # st.write(4)
                    show_main_page()
                    show_logout_page()
                else:
                    show_select_page()
                    if st.session_state['Instructor']:
                        show_instructor_page()
                    if st.session_state['Course']:
                        # st.write(8)
                        show_course_page()
        else:
            show_login_page()
