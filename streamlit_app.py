import streamlit as st
import snowflake.connector
from PIL import Image
import time
import pandas as pd
import time
headerSection = st.container()
mainSection = st.container()
loginSection = st.container()
logOutSection = st.container()
FillSection = st.container()
AddSection = st.container()
SaveSection = st.container()
InputSection = st.container()
st.markdown(
    """<style>
        button {
            height: 1em;     
        }
        </style>""",
    unsafe_allow_html=True,
)


def init_connection():
    return snowflake.connector.connect(
        **st.secrets["snowflake"], client_session_keep_alive=True
    )


def add_data(des, pre, tex, ref, maj, obj, cov, obo, csn, cona, courde):
    use = st.session_state['User']
    passw = st.session_state['Password']
    email = st.session_state['Email']
    st.markdown(f"""
        Information：
        - Instructor: {use}
        - Password: {passw}
        - Email: {email}
        - Course Code : {csn}
        - Course Name : {cona}
        - Course Department : {courde}
        - Description : {des}
        - Prerequisites : {pre}
        - Textbook : {tex}
        - Reference : {ref}
        - Major : {maj}
        - Objectives : {obj}
        - Covered : {cov}
        - Objectives Outcomes : {obo}
        """)
    conn = init_connection()
    cursor = conn.cursor()
    add_back = st.button("Back", key='add_back')
    add_confirm = st.button('confirm', key='add_confirm')
    if add_confirm:
        sql1 = "INSERT INTO INSTRUCTORS (name, course, password, email) values ('%s', '%s', '%s', '%s')" % (use, csn, passw, email)
        cursor.execute(sql1)
        sql2 = "insert into course (id_name, course_name, course_dept, description, prerequisites, textbook, reference, major_pre, objectives, covered, objectives_outcomes) values ('%s', '%s', '%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (csn, cona, courde, des, pre, tex, ref, maj, obj, cov, obo)
        cursor.execute(sql2)
        conn.commit()
        st.write("input successfully")
    if add_back:
        st.session_state['ADD'] = True


def inputdata(des, pre, tex, ref, maj, obj, cov, obo, csn):
    st.markdown(f"""
    Information：
    - Name : {csn}
    - Description : {des}
    - Prerequisites : {pre}
    - Textbook : {tex}
    - Reference : {ref}
    - Major : {maj}
    - Objectives : {obj}
    - Covered : {cov}
    - Objectives Outcomes : {obo}
    """)
    conn = init_connection()
    cursor = conn.cursor()
    sql = "UPDATE course SET description = '%s', prerequisites = '%s', textbook = '%s', reference = '%s', major_pre = " \
          "'%s', objectives = '%s', covered = '%s', objectives_outcomes = '%s' WHERE id_name = '%s'" % (des,
                                                                                                            pre,
                                                                                                            tex,
                                                                                                            ref, maj,
                                                                                                            obj, cov,
                                                                                                            obo, csn)
    cursor.execute(sql)
    conn.commit()
    back_save = st.button("Back", key='back_save')
    confirm = st.button('confirm')

    if confirm:
        sql1 = "UPDATE course SET status = 'Confirmed' WHERE id_name = '%s'" % (csn)
        cursor.execute(sql1)
        conn.commit()
        st.write("input successfully")
    if back_save:
        st.session_state['Fill'] = True


def loading(code):
    conn = init_connection()
    cursor = conn.cursor()
    sql = "Select * from course Where id_name = '%s'" % (
        code)
    cursor.execute(sql)
    conn.commit()
    df2 = cursor.fetchall()
    #df2 = pd.read_sql(sql, con=db)  #it read the result as a dataframe very important
    return df2


def convertTuple(tup):      #convert tuple to string
    str = ''.join(tup)
    return str


def Read():
    name = st.session_state['User']
    conn = init_connection()
    cursor = conn.cursor()
    sql = "Select name, course , status from course M Join instructors F On M.id_name = F.course AND F.name = '%s'" % (
        name)
    cursor.execute(sql)
    conn.commit()
    df2 = pd.read_sql(sql, con=conn)  #it read the result as a dataframe very important
    return df2


def LoggedOut_Clicked():
    st.session_state['loggedIn'] = False
    del st.session_state['User']

def show_logout_page():
    loginSection.empty()
    with logOutSection:
        st.button("Log Out", key="logout", on_click=LoggedOut_Clicked)


def LoggedIn_Clicked(userName, password):
    conn = init_connection()
    cursor = conn.cursor()
    sql = "Select * from instructors Where name = '%s';" % (userName)
    cursor.execute(sql)
    conn.commit()
    df2 = cursor.fetchone()

    #st.write(df2[3])
    #st.write(type(df2[3]))
    df = int(df2[3])
    password = int(password) #as password is a string and df2 is tuple
    if df2 is not None and df == password:
        st.session_state['loggedIn'] = True
        if 'User' not in st.session_state:
            st.session_state['User'] = userName
        if 'Password' not in st.session_state:
            st.session_state['Password'] = df
        if 'Email' not in st.session_state:
            st.session_state['Email'] = df2[4]
    else:
        st.session_state['loggedIn'] = False
        st.error("Invalid user name or password")


def main_click(*cour):      #after click the button of main page
    if 'Fill' not in st.session_state:
        st.session_state['Fill'] = True
    else:
        st.session_state['Fill'] = True
    if 'name' not in st.session_state:
        st.session_state['name'] = convertTuple(cour)  #the paramater of course code and cour is a tuple
    else:
        st.session_state['name'] = convertTuple(cour)
    st.session_state['main'] = False
    if 'ADD' not in st.session_state:
        st.session_state['ADD'] = False
    else:
        st.session_state['ADD'] = False
    if 'Choose' not in st.session_state:
        st.session_state['Choose'] = True
    else:
        st.session_state['Choose'] = True


def Main_Add_click():
    st.session_state['main'] = False
    if 'ADD' not in st.session_state:
        st.session_state['ADD'] = True
    else:
        st.session_state['ADD'] = True
    if 'Fill' not in st.session_state:
        st.session_state['Fill'] = False
    else:
        st.session_state['Fill'] = False
    if 'Choose' not in st.session_state:
        st.session_state['Choose'] = False
    else:
        st.session_state['Choose'] = False


def show_Input_page():
    with InputSection:
        if st.session_state['ADD'] == False:
            add_data(st.session_state['des'], st.session_state['pre'], st.session_state['tex'], st.session_state['ref'], st.session_state['maj'], st.session_state['obj'], st.session_state['cov'], st.session_state['obo'], st.session_state['csn'], st.session_state['cona'], st.session_state['courde'])


def show_Save_page():
    with SaveSection:
        if st.session_state['Fill'] == False:
            inputdata(st.session_state['des'], st.session_state['pre'], st.session_state['tex'], st.session_state['ref'], st.session_state['maj'], st.session_state['obj'], st.session_state['cov'], st.session_state['obo'], st.session_state['csn'])


def Add_click(des, pre, tex, ref, maj, obj, cov, obo, csn, cona, courde):
    st.session_state['ADD'] = False
    if 'des' not in st.session_state:
        st.session_state['des'] = des
    else:
        st.session_state['des'] = des
    if 'pre' not in st.session_state:
        st.session_state['pre'] = pre
    else:
        st.session_state['pre'] = pre
    if 'tex' not in st.session_state:
        st.session_state['tex'] = tex
    else:
        st.session_state['tex'] = tex
    if 'ref' not in st.session_state:
        st.session_state['ref'] = ref
    else:
        st.session_state['ref'] = ref
    if 'maj' not in st.session_state:
        st.session_state['maj'] = maj
    else:
        st.session_state['maj'] = maj
    if 'obj' not in st.session_state:
        st.session_state['obj'] = obj
    else:
        st.session_state['obj'] = obj
    if 'cov' not in st.session_state:
        st.session_state['cov'] = cov
    else:
        st.session_state['cov'] = cov
    if 'obo' not in st.session_state:
        st.session_state['obo'] = obo
    else:
        st.session_state['obo'] = obo
    if 'csn' not in st.session_state:
        st.session_state['csn'] = csn
    else:
        st.session_state['csn'] = csn
    if 'cona' not in st.session_state:
        st.session_state['cona'] = cona
    else:
        st.session_state['cona'] = cona
    if 'courde' not in st.session_state:
        st.session_state['courde'] = courde
    else:
        st.session_state['courde'] = courde


def Fill_click(des, pre, tex, ref, maj, obj, cov, obo, csn):
    st.session_state['Fill'] = False
    if 'des' not in st.session_state:
        st.session_state['des'] = des
    else:
        st.session_state['des'] = des
    if 'pre' not in st.session_state:
        st.session_state['pre'] = pre
    else:
        st.session_state['pre'] = pre
    if 'tex' not in st.session_state:
        st.session_state['tex'] = tex
    else:
        st.session_state['tex'] = tex
    if 'ref' not in st.session_state:
        st.session_state['ref'] = ref
    else:
        st.session_state['ref'] = ref
    if 'maj' not in st.session_state:
        st.session_state['maj'] = maj
    else:
        st.session_state['maj'] = maj
    if 'obj' not in st.session_state:
        st.session_state['obj'] = obj
    else:
        st.session_state['obj'] = obj
    if 'cov' not in st.session_state:
        st.session_state['cov'] = cov
    else:
        st.session_state['cov'] = cov
    if 'obo' not in st.session_state:
        st.session_state['obo'] = obo
    else:
        st.session_state['obo'] = obo
    if 'csn' not in st.session_state:
        st.session_state['csn'] = csn
    else:
        st.session_state['csn'] = csn


def show_Add_page():
    if st.session_state['main'] == False and st.session_state['ADD'] == True and st.session_state['Choose'] == False:
        with AddSection:
            st.title('FST')
            image = Image.open('UM_logo.jpg')
            st.image(image)
            course_code = st.text_input("Course Code")
            course_name = st.text_input("Course Name")
            course_dept = st.text_input("Course Department")
            catalog_description = st.text_input("Catalog Description")
            prerequisites = st.text_input("Prerequisites")
            textbook = st.text_input("Textbook(s) and other required materia")
            references = st.text_input("References")
            major_prerequisites_by_topic = st.text_input("Major prerequisites by topic")
            course_objectives = st.text_input("Course objectives")
            topics_covered = st.text_input("Topics covered")
            objectives_and_outcomes = st.text_input("Relationship to CEE, EEE and EME program objectives and outcomes")
            submit = st.button("Save", key='add_submit')
            turn_back = st.button("Back", key='turn_back')
            if submit:
                Add_click(catalog_description, prerequisites, textbook, references, major_prerequisites_by_topic,
                           course_objectives, topics_covered, objectives_and_outcomes, course_code, course_name, course_dept)
            if turn_back:
                st.session_state['main'] = True


def show_login_page():
    with loginSection:
        st.title("User")
        if st.session_state['loggedIn'] == False:
            userName = st.text_input(label="", value="", placeholder="Enter your user name")
            password = st.text_input(label="", value="", placeholder="Enter password", type="password")
            st.button("Login", on_click=LoggedIn_Clicked, args=(userName, password))


def show_main_page():
    with mainSection:
        st.title('FST')
        image = Image.open('UM_logo.jpg')
        st.image(image)
        df2 = Read()   #return is tuples
        left_column, right_column = st.columns([2, 2])
        with left_column:
            st.table(df2)
        with right_column:
            st.write('modify')
            for i, j in zip(df2.COURSE, df2.STATUS):    #i is string
                i = st.button(j, key=i, on_click=main_click, args=i)
        add = st.button('add', on_click=Main_Add_click)      #st.session_state['User']
        show_logout_page()


def show_Fill_page():
    if st.session_state['main'] == False and st.session_state['Fill'] == True and st.session_state['Choose'] == True:
        with FillSection:
            st.title('FST')
            image = Image.open('UM_logo.jpg')
            st.image(image)
            course_code = st.session_state['name']
            df = loading(course_code)
            #st.write(df[0])
            df1 = df[0]
            #st.write(df1[0])
            #st.write(df1[1])
            if df1[4] != None:
                catalog_description = st.text_input("Catalog Description", df1[4])
            else:
                catalog_description = st.text_input("Catalog Description")

            if df1[5] != None:
                prerequisites = st.text_input("Prerequisites", df1[5])
            else:
                prerequisites = st.text_input("Prerequisites")

            if df1[6] != None:
                textbook = st.text_input("Textbook(s) and other required materia", df1[6])
            else:
                textbook = st.text_input("Textbook(s) and other required materia")

            if df1[7] != None:
                references = st.text_input("References", df1[7])
            else:
                references = st.text_input("References")

            if df1[8] != None:
                major_prerequisites_by_topic = st.text_input("Major prerequisites by topic", df1[8])
            else:
                major_prerequisites_by_topic = st.text_input("Major prerequisites by topic")

            if df1[9] != None:
                course_objectives = st.text_input("Course objectives", df1[9])
            else:
                course_objectives = st.text_input("Course objectives")

            if df1[10] != None:
                topics_covered = st.text_input("Topics covered", df1[10])
            else:
                topics_covered = st.text_input("Topics covered")

            if df1[11] != None:
                objectives_and_outcomes = st.text_input("Relationship to CEE, EEE and EME program objectives and outcomes", df1[11])
            else:
                objectives_and_outcomes = st.text_input("Relationship to CEE, EEE and EME program objectives and outcomes")

            sub_mit = st.button("Save")
            back = st.button("Back")
            if sub_mit:
                Fill_click(catalog_description, prerequisites, textbook, references, major_prerequisites_by_topic,course_objectives, topics_covered, objectives_and_outcomes, course_code)
            if back:
                st.session_state['main'] = True


with headerSection:
    if 'loggedIn' not in st.session_state:
        st.session_state['loggedIn'] = False
        show_login_page()   #st.session_state['loggedIn'] = True
    else:
        if st.session_state['loggedIn']:
              #st.session_state['loggedIn'] = True,if lock out click,then st.session_state['loggedIn']=false
            if 'main' not in st.session_state:
                st.session_state['main'] = True
                #st.write(1)
                show_main_page()  #st.session_state['main'] = True,after click st.session_state['main'] = False
                #st.write(2)
            else:
                if st.session_state['main'] == True:
                    #st.write(3)
                    show_main_page()        #st.session_state['main'] is exit and == True,when it press button,the st.session_state['main'] =False
                    #st.write(4)
                else:           # st.session_state['main'] is exit and == False
                    if st.session_state['Fill']:
                        #st.write(5)
                        show_Fill_page()  #st.session_state['main'] is false and Fill is exit and is True
                        #st.write(6)
                    elif st.session_state['Fill'] == False and st.session_state['Choose'] == True:
                        #st.write(7)
                        show_Save_page() #st.session_state['main'] is false and Fill is exit and is False
                        #st.write(8)
                    elif st.session_state['ADD']:
                        show_Add_page()
                    elif st.session_state['ADD'] == False and st.session_state['Choose'] == False:
                        show_Input_page()
        else:
            show_login_page()

