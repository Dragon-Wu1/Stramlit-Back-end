import streamlit as st
import snowflake.connector
from PIL import Image
import pandas as pd
import email.message
import smtplib
import time

st.set_page_config(
    page_title="Multipage App",
)


def init_connection():
    return snowflake.connector.connect(
        **st.secrets["snowflake"], client_session_keep_alive=True
    )


def get_instructors(cursor):
    cursor.execute('SELECT * FROM instructors')
    conn.commit()
    instructors = cursor.fetchall()
    return instructors


def add_instructor(cursor, name, course, password, email):
    cursor.execute(
        f"INSERT INTO instructors (name, course, password, email) VALUES ('{name}', '{course}', '{password}', '{email}')")
    conn.commit()


def delete_instructor(cursor, id):
    cursor.execute(f"DELETE FROM instructors WHERE id = {id}")
    conn.commit()


def edit_instructor(cursor, id, name, course, password, email):
    cursor.execute(
        f"UPDATE instructors SET name = '{name}', course = '{course}', password = '{password}', email = '{email}' WHERE id = {id}")
    conn.commit()


def show_instructors(instructors):
    st.write('## View User')
    df = pd.DataFrame(instructors, columns=['ID', 'NAME', 'COURSE', 'PASSWORD', 'Email'])
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', None)
    st.dataframe(df)


def add_instructor_form():
    st.write('## Add User Form')
    name = st.text_input('Name')
    course = st.text_input('Course')
    password = st.text_input('Password', type='password')
    email = st.text_input('Email')

    if not (name and course and password and email):
        st.warning('Please fill in all information!')
        return

    if st.button('Submit'):
        add_instructor(cursor, name, course, password, email)
        st.success('User information has been added!')


def delete_instructor_form():
    st.write('## Delete User Information')
    id = st.number_input('Please enter the user ID to delete', step=1, value=1)

    if 'delete_confirm' not in st.session_state:
        st.session_state.delete_confirm = False

    if st.button('Delete'):
        if not st.session_state.delete_confirm:
            st.warning('Are you sure to delete this user information?')
            st.session_state.delete_confirm = True
        else:
            try:
                delete_instructor(cursor, id)
                st.success('User information has been deleted!')
            except Exception as e:
                st.error('Invalid user id：{}'.format(str(e)))
            finally:
                st.session_state.delete_confirm = False


def edit_instructor_form():
    st.write('## Modify User Information')
    id = st.number_input('Please enter the user ID to edit', step=1, value=1)
    name = st.text_input('Name')
    course = st.text_input('Course')
    password = st.text_input('Password', type='password')
    email = st.text_input('Email')
    if st.button('Modify'):
        edit_instructor(cursor, id, name, course, password, email)
        st.success('User information has been modified!')


if 'btn_clicked' not in st.session_state:
    st.session_state['btn_clicked'] = False


def callback():
    st.session_state['btn_clicked'] = True


@st.cache_resource
def time_consuming_func():
    time.sleep(3)
    return


headerSection = st.container()
mainSection = st.container()
loginSection = st.container()
logOutSection = st.container()
RevisionSection = st.container()
ViewSection = st.container()
UserSection = st.container()
SelectSection = st.container()


def send_email(email_list, name_list):
    for i, y in zip(email_list, name_list):
        msg = email.message.EmailMessage()
        sender_email = "dragonhunter9527@gmail.com"
        receiver_email = i  # dragonwu9523@gmail.com
        msg["From"] = sender_email
        msg["To"] = receiver_email
        msg["Subject"] = "Filled the Course information"
        msg.add_alternative(
            "<h1>Dear Professor,</h1><br><p>Sorry to brother you,we are the member in the University of Macau,and we are writting this email for complete the course information,Moreover,This is the link for fill the information of course</p><br><h4>The link below</h4><br>https://dragon-wu1-streamlit-example-streamlit-app-w04axx.streamlit.app?cur_nam=" + y,
            subtype="html")
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login("dragonhunter9527@gmail.com", "xvkhdwolxkdsocif")
        server.send_message(msg)
        server.close()


def show_All_page():
    if st.session_state['SELECT_ALL_FUNCTION']:
        df2 = query(cursor)
        with AllSection:
            button_list = []
            email_list = []
            name_list = []
            select_all = st.button("All", on_click=all_click)
            left_column, right_column = st.columns([3, 1])
            with left_column:
                st.write(df2)

            with right_column:
                for j in df2.ID_NAME:
                    j = st.checkbox(j, value=True, key=j)
                    button_list.append(j)
            left_column1, right_column1 = st.columns([3, 1])
            with left_column1:
                bac = st.button(label='Back')
            with right_column1:
                sub = st.button(label='Send')
            if sub:
                for t in range(0, len(button_list)):
                    if button_list[t]:
                        email_list.append(df2.at[t, "EMAIL"])
                        name_list.append(df2.at[t, "ID_NAME"])
                st.write(email_list)
                st.write(name_list)
                st.success("You have successfully send email!")
                send_email(email_list, name_list)
                show_logout_page()
                st.session_state['SELECT_ALL_FUNCTION'] = False
                st.session_state['Revision'] = False

            if bac:
                st.session_state['Revision'] = False
                st.session_state['SELECT_ALL_FUNCTION'] = False


def all_click():
    st.session_state['SELECT_ALL_FUNCTION'] = True


def query(cursor):
    sql = 'Select id_name,course_name , status, email from course M Join instructors F On M.id_name = F.course;'
    cursor.execute(sql)
    conn.commit()
    df2 = pd.read_sql(sql, con=conn)
    return df2


def department1_find_course(cursor, fac_name):
    sql = "select id_name,course_name,status from course left join faculty on course.course_dept = faculty.department1 where faculty.faculty_name='%s';" % (
        fac_name)
    cursor.execute(sql)
    conn.commit()
    df2 = pd.read_sql(sql, con=conn)
    return df2


def department2_find_course(cursor, fac_name):
    sql = "select id_name,course_name,status from course left join faculty on course.course_dept = faculty.department2 where faculty.faculty_name='%s';" % (
        fac_name)
    cursor.execute(sql)
    conn.commit()
    df2 = pd.read_sql(sql, con=conn)
    return df2


def department3_find_course(cursor, fac_name):
    sql = "select id_name,course_name,status from course left join faculty on course.course_dept = faculty.department3 where faculty.faculty_name='%s';" % (
        fac_name)
    cursor.execute(sql)
    conn.commit()
    df2 = pd.read_sql(sql, con=conn)
    return df2


def department4_find_course(cursor, fac_name):
    sql = "select id_name,course_name,status from course left join faculty on course.course_dept = faculty.department4 where faculty.faculty_name='%s';" % (
        fac_name)
    cursor.execute(sql)
    conn.commit()
    df2 = pd.read_sql(sql, con=conn)
    return df2


def department5_find_course(cursor, fac_name):
    sql = "select id_name,course_name,status from course left join faculty on course.course_dept = faculty.department5 where faculty.faculty_name='%s';" % (
        fac_name)
    cursor.execute(sql)
    conn.commit()
    df2 = pd.read_sql(sql, con=conn)
    return df2


def department6_find_course(cursor, fac_name):
    sql = "select id_name,course_name,status from course left join faculty on course.course_dept = faculty.department6 where faculty.faculty_name='%s';" % (
        fac_name)
    cursor.execute(sql)
    conn.commit()
    df2 = pd.read_sql(sql, con=conn)
    return df2


def department7_find_course(cursor, fac_name):
    sql = "select id_name,course_name,status from course left join faculty on course.course_dept = faculty.department7 where faculty.faculty_name='%s';" % (
        fac_name)
    cursor.execute(sql)
    conn.commit()
    df2 = pd.read_sql(sql, con=conn)
    return df2


def departmentall_find_course(cursor, fac_name):
    sql = "select id_name,course_name,status from course left join faculty on course.course_dept = faculty.department1 or course.course_dept = faculty.department2 or course.course_dept = faculty.department3 or course.course_dept = faculty.department4 or course.course_dept = faculty.department5 or course.course_dept = faculty.department6 or course.course_dept = faculty.department7 where faculty.faculty_name='%s';" % (
        fac_name)
    cursor.execute(sql)
    conn.commit()
    df2 = pd.read_sql(sql, con=conn)
    return df2


def find_class(cursor, id_na):
    sql = "select * from course where id_name = '%s';" % (id_na)
    cursor.execute(sql)
    conn.commit()
    df2 = pd.read_sql(sql, con=conn)
    return df2


def show_revision_page():
    if st.session_state['Revision'] and st.session_state['SELECT_ALL_FUNCTION'] == False:
        with RevisionSection:
            select_all = st.button("All", on_click=all_click)
            df2 = query(cursor)
            course_name = df2[["COURSE_NAME"]]
            button_list = []
            email_list = []
            name_list = []
            left_column, right_column = st.columns([3, 1])
            with left_column:
                st.write(df2)

            with right_column:

                for j in df2.ID_NAME:
                    j = st.checkbox(j, key=j)
                    button_list.append(j)
            left_column1, right_column1 = st.columns([3, 1])
            with left_column1:
                back = st.button(label='Back')
            with right_column1:
                submit_button = st.button(label='Send')

            if submit_button:
                for t in range(0, len(button_list)):
                    if button_list[t]:
                        email_list.append(df2.at[t, "EMAIL"])
                        name_list.append(df2.at[t, "ID_NAME"])
                st.write(email_list)
                st.write(name_list)
                st.success("You have successfully send email!")
                send_email(email_list, name_list)
                show_logout_page()
                st.session_state['Revision'] = False

            if back:
                st.session_state['Revision'] = False


def show_view_page():
    if st.session_state['View']:
        with ViewSection:
            st.subheader("Course information")
            if 'Search' not in st.session_state:
                st.session_state['Search'] = False
            faculty_list = ['FAH - FACULTY OF ARTS AND HUMANITIES',
                            'FBA - FACULTY OF BUSINESS ADMINISTRATION',
                            'FED - FACULTY OF EDUCATION',
                            'FHS - FACULTY OF HEALTH SCIENCES', 'FLL - FACULTY OF LAW',
                            'FSS - FACULTY OF SOCIAL SCIENCES',
                            'FST - FACULTY OF SCIENCE AND TECHNOLOGY',
                            'HC - HONOURS COLLEGE',
                            'IAPME - INSTITUTE OF APPLIED PHYSICS AND MATERIALS ENGINEERING',
                            'ICI - INSTITUTE OF COLLABORATIVE INNOVATION',
                            'ICMS - INSTITUTE OF CHINESE MEDICAL SCIENCES',
                            'IME - INSTITUTE OF MICROELECTRONICS',
                            'RC - RESIDENTIAL COLLEGES']
            Offering_Unit = st.selectbox("Offering Unit", faculty_list, index=1)
            st.write('You selected {}.'.format(Offering_Unit))

            if 'FAH - FACULTY OF ARTS AND HUMANITIES' in Offering_Unit:
                Department = ['--- All ---', 'CJS - CENTRE FOR JAPANESE STUDIES',
                              'DCH - DEPARTMENT OF CHINESE LANGUAGE AND LITERATURE',
                              'DENG - DEPARTMENT OF ENGLISH', 'DHIST - DEPARTMENT OF HISTORY',
                              'DPHIL - DEPARTMENT OF PHILOSOPHY AND RELIGIOUS STUDIES',
                              'DPT - DEPARTMENT OF PORTUGUESE', 'ELC - ENGLISH LANGUAGE CENTRE']
                Offering_Department = st.selectbox("Offering Department", Department
                                                   ,
                                                   index=1)
                st.write('You selected {}.'.format(Offering_Department))

            elif 'FBA - FACULTY OF BUSINESS ADMINISTRATION' in Offering_Unit:
                Department = ['--- All ---', 'AIM - DEPARTMENT OF ACCOUNTING AND INFORMATION MANAGEMENT',
                              'DRTM - DEPARTMENT OF INTEGRATED RESORT AND TOURISM MANAGEMENT',
                              'FBE - DEPARTMENT OF FINANCE AND BUSINESS ECONOMICS',
                              'IIRM - INTERNATIONAL INTEGRATED RESORT MANAGEMENT',
                              'MMI - DEPARTMENT OF MANAGEMENT AND MARKETING']
                Offering_Department = st.selectbox("Offering Department", Department,
                                                   index=1)
                st.write('You selected {}.'.format(Offering_Department))

            elif 'FED - FACULTY OF EDUCATION' in Offering_Unit:
                Department = ['--- All ---']
                Offering_Department = st.selectbox("Offering Department", Department)
                st.write('You selected {}.'.format(Offering_Department))

            elif 'FHS - FACULTY OF HEALTH SCIENCES' in Offering_Unit:
                Department = ['--- All ---', 'DBS - DEPARTMENT OF BIOMEDICAL SCIENCES',
                              'DPM - DEPARTMENT OF PUBLIC HEALTH AND MEDICINAL ADMINISTRATION',
                              'DPS - DEPARTMENT OF PHARMACEUTICAL SCIENCES']
                Offering_Department = st.selectbox("Offering Department", Department
                                                   )
                st.write('You selected {}.'.format(Offering_Department))

            elif 'FLL - FACULTY OF LAW' in Offering_Unit:
                Department = ['--- All ---', 'GLS - DEPARTMENT OF GLOBAL LEGAL STUDIES',
                              'MLS - DEPARTMENT OF MACAO LEGAL STUDIES']
                Offering_Department = st.selectbox("Offering Department", Department
                                                   )
                st.write('You selected {}.'.format(Offering_Department))

            elif 'FSS - FACULTY OF SOCIAL SCIENCES' in Offering_Unit:
                Department = ['--- All ---', 'DCOM - DEPARTMENT OF COMMUNICATION',
                              'DECO - DEPARTMENT OF ECONOMICS',
                              'DGPA - DEPARTMENT OF GOVERNMENT AND PUBLIC ADMINISTRATION',
                              'DPSY - DEPARTMENT OF PSYCHOLOGY',
                              'DSOC - DEPARTMENT OF SOCIOLOGY']
                Offering_Department = st.selectbox("Offering Department", Department
                                                   )
                st.write('You selected {}.'.format(Offering_Department))

            elif 'FST - FACULTY OF SCIENCE AND TECHNOLOGY' in Offering_Unit:
                Department = ['--- All ---',
                              'CEE - DEPARTMENT OF CIVIL AND ENVIRONMENTAL ENGINEERING',
                              'CIS - DEPARTMENT OF COMPUTER AND INFORMATION SCIENCE',
                              'CSG - CHEMISTRY SUPPORTING GROUP',
                              'DPC - DEPARTMENT OF PHYSICS AND CHEMISTRY',
                              'ECE - DEPARTMENT OF ELECTRICAL AND COMPUTER ENGINEERING',
                              'EME - DEPARTMENT OF ELECTROMECHANICAL ENGINEERING',
                              'MAT - DEPARTMENT OF MATHEMATICS']
                Offering_Department = st.selectbox("Offering Department", Department)
                st.write('You selected {}.'.format(Offering_Department))

            elif 'HC - HONOURS COLLEGE' in Offering_Unit:
                Department = ['--- All ---']
                Offering_Department = st.selectbox("Offering Department", Department)
                st.write('You selected {}.'.format(Offering_Department))

            elif 'IAPME - INSTITUTE OF APPLIED PHYSICS AND MATERIALS ENGINEERING' in Offering_Unit:
                Department = ['--- All ---']
                Offering_Department = st.selectbox("Offering Department", Department)
                st.write('You selected {}.'.format(Offering_Department))

            elif 'ICI - INSTITUTE OF COLLABORATIVE INNOVATION' in Offering_Unit:
                Department = ['--- All ---', 'CIE - CENTRE FOR INNOVATION AND ENTREPRENEURSHIP']
                Offering_Department = st.selectbox("Offering Department", Department
                                                   )
                st.write('You selected {}.'.format(Offering_Department))

            elif 'ICMS - INSTITUTE OF CHINESE MEDICAL SCIENCES' in Offering_Unit:
                Department = ['--- All ---']
                Offering_Department = st.selectbox("Offering Department", Department)
                st.write('You selected {}.'.format(Offering_Department))

            elif 'IME - INSTITUTE OF MICROELECTRONICS' in Offering_Unit:
                Department = ['--- All ---']
                Offering_Department = st.selectbox("Offering Department", Department)
                st.write('You selected {}.'.format(Offering_Department))

            elif 'RC - RESIDENTIAL COLLEGES' in Offering_Unit:
                Department = ['--- All ---']
                Offering_Department = st.selectbox("Offering Department", Department)
                st.write('You selected {}.'.format(Offering_Department))

            if st.button("Search", on_click=callback) or st.session_state['btn_clicked']:
                for produect in faculty_list:
                    if produect in Offering_Unit:
                        for depart in range(0, len(Department)):  # the length of the department list
                            if Department[depart] in Offering_Department:
                                time_consuming_func()
                                if depart == 0:
                                    df2 = departmentall_find_course(cursor,
                                                                    produect)  # dataframe df2 = df2[' '].values.tolist(),change to list
                                elif depart == 1:
                                    df2 = department1_find_course(cursor, produect)
                                elif depart == 2:
                                    df2 = department2_find_course(cursor, produect)
                                elif depart == 3:
                                    df2 = department3_find_course(cursor, produect)
                                elif depart == 4:
                                    df2 = department4_find_course(cursor, produect)
                                elif depart == 5:
                                    df2 = department5_find_course(cursor, produect)
                                elif depart == 6:
                                    df2 = department6_find_course(cursor, produect)
                                elif depart == 7:
                                    df2 = department7_find_course(cursor, produect)
                                st.write(df2)
                                df2 = df2['ID_NAME'].values.tolist()
                                selected_subject = st.selectbox("Select the course", df2)
                                for item in df2:
                                    if item in selected_subject:
                                        dc2 = find_class(cursor, item)
                                        if st.button("View"):
                                            st.write(dc2)


def show_user_page():
    if st.session_state['User']:
        with UserSection:
            menu = ['View user information', 'Add user information', 'Delete user information',
                    'Modify user information']
            choice = st.sidebar.selectbox('Please select the following functions below', menu)

            if choice == 'View user information':
                instructors = get_instructors(cursor)
                show_instructors(instructors)
            elif choice == 'Add user information':
                add_instructor_form()
            elif choice == 'Delete user information':
                delete_instructor_form()
            elif choice == 'Modify user information':
                edit_instructor_form()


def show_select_page():
    with SelectSection:
        st.sidebar.success("Select a function below.")
        select = st.sidebar.selectbox(
            'Function', (" ", "Revision", "View", "User")
        )
        if select == " ":
            st.session_state['main'] = False
        elif select == 'Revision':
            st.session_state['main'] = False
            if 'Revision' not in st.session_state:
                st.session_state['Revision'] = True
            else:
                st.session_state['Revision'] = True
            if 'View' not in st.session_state:
                st.session_state['View'] = False
            else:
                st.session_state['View'] = False
            if 'User' not in st.session_state:
                st.session_state['User'] = False
            else:
                st.session_state['User'] = False

        elif select == 'View':
            st.session_state['main'] = False
            if 'View' not in st.session_state:
                st.session_state['View'] = True
            else:
                st.session_state['View'] = True
            if 'Revision' not in st.session_state:
                st.session_state['Revision'] = False
            else:
                st.session_state['Revision'] = False
            if 'User' not in st.session_state:
                st.session_state['User'] = False
            else:
                st.session_state['User'] = False

        elif select == 'User':
            st.session_state['main'] = False
            if 'User' not in st.session_state:
                st.session_state['User'] = True
            else:
                st.session_state['User'] = True
            if 'Revision' not in st.session_state:
                st.session_state['Revision'] = False
            else:
                st.session_state['Revision'] = False
            if 'View' not in st.session_state:
                st.session_state['View'] = False
            else:
                st.session_state['View'] = False


def show_main_page():
    if st.session_state['main']:
        with mainSection:
            st.title("Main Page")
            image = Image.open('logo.jpg')
            st.image(image)
            st.header("Supervisor : Prof. Derek WONG ")
            st.subheader("Student : WU MAN CHON")
            st.subheader("Student : CHAN CHON IP")


def LoggedOut_Clicked():
    st.session_state['loggedIn'] = False


def show_logout_page():
    loginSection.empty()
    with logOutSection:
        st.button("Log Out", key="logout", on_click=LoggedOut_Clicked)


def LoggedIn_Clicked(userName, password):
    conn = init_connection()
    cursor = conn.cursor()
    sql = "Select * from admins Where name = '%s';" % (userName)
    cursor.execute(sql)
    conn.commit()
    df2 = cursor.fetchone()
    # st.write(type(df2[2])) int
    # st.write(type(password)) string
    df = df2[2]
    # mark down
    st.write(type(passwor))
    if df2 is not None and df == password:
        st.session_state['loggedIn'] = True
        if 'UserName' not in st.session_state:
            st.session_state['UserName'] = userName
    else:
        st.session_state['loggedIn'] = False
        st.error("Invalid user name or password")


def show_login_page():
    with loginSection:
        st.title("Admin")
        if st.session_state['loggedIn'] == False:
            userName = st.text_input(label="", value="", placeholder="Enter your user name")
            password = st.text_input(label="", value="", placeholder="Enter password", type="password")
            st.button("Login", on_click=LoggedIn_Clicked, args=(userName, password)

with headerSection:
    conn = init_connection()
    cursor = conn.cursor()
    if 'loggedIn' not in st.session_state:
        st.session_state['loggedIn'] = False
        show_login_page()
    else:
        if st.session_state['loggedIn']:
        if 'main' not in st.session_state:
            st.session_state['main'] = True
            # st.write(1)
            show_main_page()
            show_logout_page()
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
                # st.session_state['main'] is exit and == False
                if 'SELECT_ALL_FUNCTION' not in st.session_state:
                    st.session_state['SELECT_ALL_FUNCTION'] = False
                if st.session_state['Revision'] and st.session_state['SELECT_ALL_FUNCTION'] == False:
                    # st.write(5)
                    show_revision_page()

                if st.session_state['SELECT_ALL_FUNCTION']:
                    # st.write(6)
                    show_All_page()

                if st.session_state['View']:
                    # st.write(7)
                    show_view_page()

                if st.session_state['User']:
                    # st.write(8)
                    show_user_page()
        else:
            show_login_page()
