import streamlit as st
import pymysql
import pandas as pd
from revision import show_revision_form



def connect():
    conn = pymysql.connect(host='127.0.0.1', user='root', passwd='a098765', port=3306, db='course_management')
    return conn


def get_instructors():
    conn = connect()
    cur = conn.cursor()
    cur.execute('SELECT * FROM instructors')
    instructors = cur.fetchall()

    return instructors


def add_instructor(instructor_id, name, course, password, email):
    conn = connect()
    cur = conn.cursor()
    cur.execute(
        f"INSERT INTO instructors (instructor_id, name, course, password, email) VALUES ('{instructor_id}','{name}', '{course}', '{password}', '{email}')")
    conn.commit()


def delete_instructor(instructor_id):
    conn = connect()
    cur = conn.cursor()
    cur.execute(f"DELETE FROM instructors WHERE instructor_id = '{instructor_id}'")
    conn.commit()


def edit_instructor(instructor_id, name, course, password, email):
    conn = connect()
    cur = conn.cursor()
    cur.execute(
        f"UPDATE instructors SET name = '{name}', course = '{course}', password = '{password}', email = '{email}' WHERE instructor_id = '{instructor_id}'")
    conn.commit()


def show_instructors(instructors):
    st.write('## User Information')
    df = pd.DataFrame(instructors, columns=['ID', 'User ID', 'Name', 'Course', 'Password', 'Email'])
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', None)
    st.dataframe(df)


def add_instructor_form():
    instructors = get_instructors()
    show_instructors(instructors)
    st.write('## Add User Form')
    instructor_id = st.text_input('Instructor ID')
    name = st.text_input('Name')
    course = st.text_input('Course')
    password = st.text_input('Password', type='password')
    email = st.text_input('Email')

    if not (instructor_id and name and course and password and email):
        st.warning('Please fill in all information!')
        return

    if 'add_confirm' not in st.session_state:
        st.session_state.add_confirm = False

    if st.button('Submit'):
        if not st.session_state.add_confirm:
            if st.button('Cancel'):
                st.session_state.add_confirm = False
            st.warning('Are you sure you want to submit? Please click the Submit button again to submit it!')
            st.session_state.add_confirm = True
        else:
            add_instructor(instructor_id, name, course, password, email)
            st.success('User information has been added!')
            st.session_state.add_confirm = False


def delete_instructor_form():
    instructors = get_instructors()
    show_instructors(instructors)
    st.write('## Delete User Information')
    instructor_id = st.text_input('Please enter the user ID to delete')

    if 'delete_confirm' not in st.session_state:
        st.session_state.delete_confirm = False

    if st.button('Delete'):
        if not st.session_state.delete_confirm:
            if st.button('Cancel'):
                st.session_state.delete_confirm = False
            st.warning(
                'Are you sure to delete this user information? Please click the Delete button again to delete it!')
            st.session_state.delete_confirm = True
        else:
            try:
                delete_instructor(instructor_id)
                st.success('User information has been deleted!')
            except Exception as e:
                st.error('Invalid user id：{}'.format(str(e)))
            finally:
                st.session_state.delete_confirm = False


def edit_instructor_form():
    instructors = get_instructors()
    show_instructors(instructors)
    st.write('## Modify User Information')
    instructor_id = st.text_input('Please enter the user ID to edit')
    name = st.text_input('Name')
    course = st.text_input('Course')
    password = st.text_input('Password', type='password')
    email = st.text_input('Email')

    if not (instructor_id and name and course and password and email):
        st.warning('Please fill in all information to modify!')
        return

    if 'edit_confirm' not in st.session_state:
        st.session_state.edit_confirm = False

    if st.button('Modify'):
        if not st.session_state.edit_confirm:
            if st.button('Cancel'):
                st.session_state.edit_confirm = False
            st.warning(
                'Are you sure you want to modify this user information? Please click the Modify button again to modify it!')
            st.session_state.edit_confirm = True
        else:
            edit_instructor(instructor_id, name, course, password, email)
            st.success('User information has been modified!')
            st.session_state.edit_confirm = False


def management():
    menu = ['View Instructor', 'Add Instructor', 'Delete Instructor',
            'Modify Instructor', 'Revision']
    choice = st.sidebar.selectbox('Please select the following functions below', menu)

    if choice == 'View Instructor':
        instructors = get_instructors()
        show_instructors(instructors)
    elif choice == 'Add Instructor':
        add_instructor_form()
    elif choice == 'Delete Instructor':
        delete_instructor_form()
    elif choice == 'Modify Instructor':
        edit_instructor_form()
    elif choice == 'Revision':
        show_revision_form()

