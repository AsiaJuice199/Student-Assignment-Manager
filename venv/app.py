# import streamlit as st
# import sqlite3
# import pandas as pd
# from datetime import datetime, date

# # --- 1. DATABASE SETUP ---
# def init_db():
#     conn = sqlite3.connect('study_tracker.db')
#     c = conn.cursor()
#     c.execute('''CREATE TABLE IF NOT EXISTS users 
#                  (username TEXT PRIMARY KEY, password TEXT, role TEXT)''')
#     c.execute('''CREATE TABLE IF NOT EXISTS assignments 
#                  (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, description TEXT, 
#                   due_date TEXT, status TEXT, subject TEXT, priority TEXT, grade TEXT, feedback TEXT)''')
#     c.execute('''CREATE TABLE IF NOT EXISTS announcements 
#                  (id INTEGER PRIMARY KEY AUTOINCREMENT, content TEXT, date_posted TEXT)''')
    
#     # Default accounts
#     c.execute("INSERT OR IGNORE INTO users VALUES ('teacher1', '1234', 'Teacher')")
#     c.execute("INSERT OR IGNORE INTO users VALUES ('student1', '1234', 'Student')")
#     conn.commit()
#     conn.close()

# init_db()

# # --- 2. LOGIN SESSION ---
# if 'logged_in' not in st.session_state:
#     st.session_state['logged_in'] = False
#     st.session_state['user_role'] = None

# if not st.session_state['logged_in']:
#     st.title("🔐 Login to Study Tracker")
#     user = st.text_input("Username")
#     pw = st.text_input("Password", type="password")
#     if st.button("Login"):
#         conn = sqlite3.connect('study_tracker.db')
#         c = conn.cursor()
#         c.execute("SELECT role FROM users WHERE username=? AND password=?", (user, pw))
#         result = c.fetchone()
#         if result:
#             st.session_state['logged_in'] = True
#             st.session_state['user_role'] = result[0]
#             st.rerun()
#         else:
#             st.error("Invalid credentials (teacher1/1234)")
#     st.stop()

# # --- 3. SIDEBAR ---
# role = st.session_state['user_role']
# st.sidebar.write(f"Logged in as: **{role}**")
# if st.sidebar.button("Logout"):
#     st.session_state['logged_in'] = False
#     st.rerun()

# # --- 4. TEACHER VIEW ---
# if role == "Teacher":
#     tab1, tab2, tab3 = st.tabs(["➕ Manage Assignments", "📣 Post Announcement", "📝 Grading Portal"])
    
#     with tab1:
#         st.subheader("Create Assignment")
#         with st.form("teacher_add", clear_on_submit=True): # clear_on_submit makes the form empty after posting
#             title = st.text_input("Title")
#             subj = st.selectbox("Subject", ["Math", "Science", "History", "English"])
#             prio = st.select_slider("Priority", options=["Low", "Medium", "High"])
#             desc = st.text_area("Detailed Instructions")
#             due = st.date_input("Due Date")
            
#             if st.form_submit_button("Post Assignment"):
#                 if title: # Check if title isn't empty
#                     conn = sqlite3.connect('study_tracker.db')
#                     c = conn.cursor()
#                     c.execute("INSERT INTO assignments (title, description, due_date, status, subject, priority) VALUES (?,?,?,?,?,?)", 
#                               (title, desc, str(due), "Pending", subj, prio))
#                     conn.commit()
#                     conn.close()
                    
#                     # --- THE POP-UP EFFECTS ---
#                     st.toast(f"Successfully posted: {title}", icon='✅')
#                     st.balloons() # Visual celebration
#                     st.success(f"Assignment '{title}' is now live for students!")
#                 else:
#                     st.error("Please enter an assignment title.")

#     with tab2:
#         st.subheader("New Announcement")
#         news = st.text_area("Message to all students")
#         if st.button("Broadcast"):
#             conn = sqlite3.connect('study_tracker.db')
#             c = conn.cursor()
#             c.execute("INSERT INTO announcements (content, date_posted) VALUES (?, ?)", (news, str(date.today())))
#             conn.commit()
#             st.success("Broadcasted!")

#     with tab3:
#         st.subheader("Student Submissions")
#         conn = sqlite3.connect('study_tracker.db')
#         df = pd.read_sql_query("SELECT * FROM assignments WHERE status = 'Done'", conn)
#         for _, row in df.iterrows():
#             with st.expander(f"Grade: {row['title']}"):
#                 st.write(f"Description: {row['description']}")
#                 grade = st.selectbox("Grade", ["A","B","C","D","F"], key=f"g_{row['id']}")
#                 feed = st.text_input("Feedback", key=f"f_{row['id']}")
#                 if st.button("Submit Grade", key=f"btn_{row['id']}"):
#                     c = conn.cursor()
#                     c.execute("UPDATE assignments SET grade=?, feedback=? WHERE id=?", (grade, feed, row['id']))
#                     conn.commit()
#                     st.success("Graded!")

# # --- 5. STUDENT VIEW ---
# else:
#     st.header("📖 Student Portal")
    
#     # Announcements Section
#     st.subheader("📣 Announcements")
#     conn = sqlite3.connect('study_tracker.db')
#     news_df = pd.read_sql_query("SELECT * FROM announcements ORDER BY id DESC", conn)
#     for _, msg in news_df.iterrows():
#         st.info(f"**{msg['date_posted']}:** {msg['content']}")

#     # Assignments Section
#     st.subheader("📝 Your Tasks")
#     assign_df = pd.read_sql_query("SELECT * FROM assignments", conn)
    
#     for _, row in assign_df.iterrows():
#         with st.container(border=True):
#             col1, col2 = st.columns([3, 1])
#             with col1:
#                 st.markdown(f"### {row['title']} ({row['subject']})")
#                 st.write(f"**Instructions:** {row['description']}")
#                 st.caption(f"Due: {row['due_date']} | Priority: {row['priority']}")
#             with col2:
#                 if row['status'] == 'Pending':
#                     if st.button("Mark as Done", key=f"done_{row['id']}"):
#                         c = conn.cursor()
#                         c.execute("UPDATE assignments SET status='Done' WHERE id=?", (row['id'],))
#                         conn.commit()
#                         st.rerun()
#                 else:
#                     st.success(f"Status: {row['status']}")
#                     if row['grade']:
#                         st.write(f"Grade: **{row['grade']}**")
#                         st.caption(f"Feedback: {row['feedback']}")

#     conn.close()
#------------------------------------------------------------------------------------------------------------------------------------------
# import streamlit as st
# import sqlite3
# import pandas as pd
# from datetime import date

# # Initialize database - run once kinda thing
# def setup_database():
#     conn = sqlite3.connect('study_tracker.db')
#     cur = conn.cursor()
    
#     # users table
#     cur.execute('''
#         CREATE TABLE IF NOT EXISTS users (
#             username TEXT PRIMARY KEY,
#             password TEXT,
#             role TEXT
#         )
#     ''')
    
#     # assignments table (student + teacher stuff)
#     cur.execute('''
#         CREATE TABLE IF NOT EXISTS assignments (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             title TEXT,
#             description TEXT,
#             due_date TEXT,
#             status TEXT DEFAULT 'Pending',
#             subject TEXT,
#             priority TEXT,
#             grade TEXT,
#             feedback TEXT
#         )
#     ''')
    
#     # announcements from teacher
#     cur.execute('''
#         CREATE TABLE IF NOT EXISTS announcements (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             content TEXT,
#             date_posted TEXT
#         )
#     ''')
    
#     # add some default accounts (very secure lol)
#     cur.execute("INSERT OR IGNORE INTO users VALUES ('teacher1', '1234', 'Teacher')")
#     cur.execute("INSERT OR IGNORE INTO users VALUES ('student1', '1234', 'Student')")
    
#     conn.commit()
#     conn.close()

# setup_database()

# # Session state stuff for login
# if 'logged_in' not in st.session_state:
#     st.session_state.logged_in = False
#     st.session_state.user_role = None

# # Not logged in → show login screen
# if not st.session_state.logged_in:
#     st.title("Study Tracker - Login")
#     username = st.text_input("Username")
#     password = st.text_input("Password", type="password")
    
#     if st.button("Login"):
#         conn = sqlite3.connect('study_tracker.db')
#         cursor = conn.cursor()
#         cursor.execute("SELECT role FROM users WHERE username = ? AND password = ?", 
#                       (username, password))
#         user = cursor.fetchone()
        
#         if user:
#             st.session_state.logged_in = True
#             st.session_state.user_role = user[0]
#             st.rerun()
#         else:
#             st.error("Wrong username or password... try teacher1 / 1234")
    
#     st.stop()  # important - dont run rest of app

# # Sidebar - simple info + logout
# st.sidebar.write(f"**Logged in as:** {st.session_state.user_role}")
# if st.sidebar.button("Logout"):
#     st.session_state.logged_in = False
#     st.rerun()

# # ────────────────────────────────────────────────
# #                TEACHER PART
# # ────────────────────────────────────────────────
# if st.session_state.user_role == "Teacher":
#     st.header("Teacher Dashboard")
#     tab_manage, tab_announce, tab_grade = st.tabs(["Assignments", "Announcements", "Grading"])

#     # Tab 1 - Add new assignment
#     with tab_manage:
#         st.subheader("Create New Assignment")
        
#         with st.form("new_assignment_form"):
#             ass_title = st.text_input("Assignment Title")
#             subject = st.selectbox("Subject", ["Math", "Science", "History", "English", "Other"])
#             priority = st.select_slider("How important?", ["Low", "Medium", "High"])
#             instructions = st.text_area("What should students do?")
#             due_date = st.date_input("Due date")
            
#             submitted = st.form_submit_button("Post Assignment")
            
#             if submitted:
#                 if not ass_title.strip():
#                     st.warning("Bro... you forgot the title")
#                 else:
#                     conn = sqlite3.connect('study_tracker.db')
#                     c = conn.cursor()
#                     c.execute("""
#     INSERT INTO assignments 
#     (title, description, due_date, status, subject, priority, grade, feedback) 
#     VALUES (?, ?, ?, ?, ?, ?, ?, ?)
# """, (ass_title, instructions, str(due_date), "Pending", subject, priority, None, None))
#                     conn.commit()
#                     conn.close()
                    
#                     st.success(f"Assignment '{ass_title}' posted!")
#                     st.balloons()

#     # Tab 2 - Announcements
#     with tab_announce:
#         st.subheader("Post Announcement")
#         message = st.text_area("Message for everyone")
        
#         if st.button("Send to all students"):
#             if message.strip():
#                 conn = sqlite3.connect('study_tracker.db')
#                 cur = conn.cursor()
#                 cur.execute("INSERT INTO announcements (content, date_posted) VALUES (?, ?)",
#                            (message, str(date.today())))
#                 conn.commit()
#                 conn.close()
#                 st.success("Announcement sent ✓")
#             else:
#                 st.warning("Write something first...")

#     # Tab 3 - Grade submissions
#     with tab_grade:
#         st.subheader("Grade Student Work")
#         conn = sqlite3.connect('study_tracker.db')
#         done_assignments = pd.read_sql_query(
#             "SELECT * FROM assignments WHERE status = 'Done'", conn)
        
#         if done_assignments.empty:
#             st.info("No submissions to grade yet...")
#         else:
#             for idx, ass in done_assignments.iterrows():
#                 with st.expander(f"{ass['title']} (ID: {ass['id']})"):
#                     st.write(ass['description'])
#                     grade = st.selectbox("Give grade", ["A", "B", "C", "D", "F"], 
#                                        key=f"grade_{ass['id']}")
#                     feedback_text = st.text_input("Feedback / comments", 
#                                                 key=f"fb_{ass['id']}")
                    
#                     if st.button("Save Grade", key=f"save_{ass['id']}"):
#                         c = conn.cursor()
#                         c.execute("UPDATE assignments SET grade=?, feedback=? WHERE id=?",
#                                  (grade, feedback_text, ass['id']))
#                         conn.commit()
#                         st.success("Grade saved!")

#         conn.close()

# # ────────────────────────────────────────────────
# #                STUDENT PART
# # ────────────────────────────────────────────────
# else:
#     st.title("📚 My Study Tracker")
    
#     conn = sqlite3.connect('study_tracker.db')
    
#     # Show announcements first
#     st.subheader("School Announcements")
#     announcements = pd.read_sql_query("SELECT * FROM announcements ORDER BY id DESC", conn)
    
#     if announcements.empty:
#         st.caption("No announcements yet...")
#     else:
#         for _, row in announcements.iterrows():
#             st.info(f"{row['date_posted']} — {row['content']}")

#     # Show assignments
#     st.subheader("My Assignments")
#     tasks = pd.read_sql_query("SELECT * FROM assignments", conn)
    
#     for _, task in tasks.iterrows():
#         with st.container(border=True):
#             left, right = st.columns([4, 1])
            
#             with left:
#                 st.markdown(f"**{task['title']}**  ({task['subject']})")
#                 st.write(task['description'])
#                 st.caption(f"Due: {task['due_date']}  •  Priority: {task['priority']}")
            
#             with right:
#                 if task['status'] == 'Pending':
#                     if st.button("✓ Done!", key=f"mark_{task['id']}"):
#                         cur = conn.cursor()
#                         cur.execute("UPDATE assignments SET status='Done' WHERE id=?", 
#                                    (task['id'],))
#                         conn.commit()
#                         st.rerun()
#                 else:
#                     st.success("Completed!")
#                     if task['grade']:
#                         st.markdown(f"**Grade:** {task['grade']}")
#                         if task['feedback']:
#                             st.caption(f"Teacher: {task['feedback']}")

#     conn.close()
#-------------------------------------------------------------------------------------------------------
import streamlit as st
import sqlite3
import pandas as pd
from datetime import date
import os

if not os.path.exists("uploads"):
    os.makedirs("uploads")

def setup_database():
    conn = sqlite3.connect('study_tracker.db')
    cur = conn.cursor()
    #users
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT,
            role TEXT
        )
    ''')
    #assignments
    cur.execute('''
    CREATE TABLE IF NOT EXISTS assignments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        description TEXT,
        due_date TEXT,
        status TEXT DEFAULT 'Pending',
        subject TEXT,
        priority TEXT,
        grade TEXT,
        feedback TEXT,
        file_path TEXT   -- NEW
    )
''')
    # announcements 
    cur.execute('''
        CREATE TABLE IF NOT EXISTS announcements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT,
            date_posted TEXT
        )
    ''')
    

    #accounts 
    cur.execute("INSERT OR IGNORE INTO users VALUES ('teacher1','1234','Teacher')")
    cur.execute("INSERT OR IGNORE INTO users VALUES ('student1', '1234', 'Student')")
    conn.commit()
    conn.close()

setup_database()

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_role = None
#login
if not st.session_state.logged_in:
    st.title("Study Tracker - Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type=
                             "password")
    if st.button("Login"):
        conn = sqlite3.connect('study_tracker.db')
        cursor = conn.cursor()
        cursor.execute("SELECT role FROM users WHERE username = ? AND password = ?", 
                      (username, password))
        
        user = cursor.fetchone()
        

        if user:
            st.session_state.logged_in = True
            st.session_state.user_role = user[0]

            st.rerun()
        else:

            st.error("Wrong name or password")
    
    st.stop()

# Sidebar
st.sidebar.write(f"**Logged in as:** {st.session_state.user_role}")
if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.rerun()

# TEACHER

if st.session_state.user_role == "Teacher":
    st.header("Teacher Dashboard")
    tab_manage, tab_announce, tab_grade = st.tabs(["Assignments", "Announcements", "Grading"])

    # new ass
    with tab_manage:
        st.subheader("Create New assignment")
        

        with st.form("new_assignment_form"):
            ass_title = st.text_input("Assignment Title")
            subject = st.selectbox("Subject", ["Math", "Science", "History ", "English", "Other"])
            priority = st.select_slider("How important?", ["Low", "Medium", "High"])
            instructions = st.text_area("What should students do?")
            due_date = st.date_input("Due date")
            submitted = st.form_submit_button("Post Assignment")
            
            if submitted:
                if not ass_title.strip():
                    st.warning("Bro... you forgot the title")

                else:
                    conn = sqlite3.connect('study_tracker.db')
                    c = conn.cursor()
                    c.execute("""
                              
    INSERT INTO assignments 
    (title, description, due_date, status, subject, priority, grade, feedback) 
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
""", (ass_title, instructions, str(due_date), "Pending", subject, priority, None, None))
                    conn.commit()
                    conn.close()
                    st.success(f"Assignment '{ass_title}' posted!")
                    


    # Announcements

    with tab_announce:
        st.subheader("Post Announcement")
        message = st.text_area("Message for everyone")
        if st.button("Send"):
            if message.strip():
                conn = sqlite3.connect('study_tracker.db')
                cur = conn.cursor()
                cur.execute("INSERT INTO announcements (content, date_posted) VALUES (?, ?)",
                           (message, str(date.today())))
                conn.commit()
                conn.close()
                st.success("Announcement sent ✓")

            else:

                st.warning("Write something")

    #submissions

    with tab_grade:
        st.subheader("Grade Student Work")
        conn = sqlite3.connect('study_tracker.db')
        done_assignments = pd.read_sql_query(
            "SELECT * FROM assignments WHERE status = 'Done'", conn)
        
        if done_assignments.empty:
            st.info("No submissions yet")
        else:
            for idx, ass in done_assignments.iterrows():
                with st.expander(f"{ass['title']} (ID: {ass['id']})"):
                    st.write(ass['description'])
                    if ass['file_path']:
                        with open(ass['file_path'], "rb") as file:
                            st.download_button(
                                label="Download Submission",
                                data=file,
                                file_name=ass['file_path'].split("/")[-1]
                            )

                    else:
                        st.warning("No file submitted")
                    grade = st.selectbox("Give grade", ["A", "B", "C", "D", "E", "F"], 
                                       key=f"grade_{ass['id']}")
                    feedback_text = st.text_input("Feedback / comments", 
                                                key=f"fb_{ass['id']}")
                    

                    if st.button("Save Grade", key=f"save_{ass['id']}"):
                        c = conn.cursor()
                        c.execute("UPDATE assignments SET grade=?, feedback=? WHERE id=?",
                                 (grade, feedback_text, ass['id']))
                        conn.commit()
                        st.success("Grade saved!")

        conn.close()

#student

else:
    st.title("📚 My Study Tracker")
    
    conn = sqlite3.connect('study_tracker.db')
    #announcements
    st.subheader("School Announcements")
    announcements = pd.read_sql_query("SELECT * FROM announcements ORDER BY id DESC", conn)
    
    if announcements.empty:
        st.caption("No announcements yet...")
    else:
        for _, row in announcements.iterrows():
            st.info(f"{row['date_posted']} — {row['content']}")
    # assignment
    st.subheader("My Assignments")
    tasks = pd.read_sql_query("SELECT * FROM assignments", conn)
    for _, task in tasks.iterrows():
        with st.container(border=True):
            left, right = st.columns([4, 1])
            

            with left:
                st.markdown(f"**{task['title']}**  ({task['subject']})")
                st.write(task['description'])
                st.caption(f"Due: {task['due_date']}  •  Priority: {task['priority']}")
            
            with right:
                if task['status'] == 'Pending':

                    uploaded_file = st.file_uploader(
                        "Upload your work",
                        key=f"upload_{task['id']}"
                    )
                    
                    if uploaded_file is not None:
                        file_path = f"uploads/{task['id']}_{uploaded_file.name}"
                        
                        # save
                        with open(file_path, "wb") as f:
                            f.write(uploaded_file.getbuffer())
                        
                        cur = conn.cursor()
                        cur.execute("""
                            UPDATE assignments 
                            SET status='Done', file_path=? 
                            WHERE id=?
                        """, (file_path, task['id']))
                        
                        conn.commit()
                        st.success("Submitted successfully!")
                        st.rerun()
                else:
                    st.success("Completed!")
                    if task['grade']:
                        st.markdown(f"**Grade:** {task['grade']}")
                        if task['feedback']:
                            st.caption(f"Teacher: {task['feedback']}")

    conn.close()