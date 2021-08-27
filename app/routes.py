from app import app
from flask import render_template, json, request, url_for, redirect, flash
import app.database.db_connector as db

# Route for index
@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    '''Displays the homepage'''
    return render_template('index.j2', style='styles/index.css')

# Route for Students
@app.route('/students', methods=['GET'])
def students():
    '''SELECT all Students and displays data'''
    db_connection = db.connect_to_database()
    query = 'SELECT * from Students ORDER BY studentID ASC;'
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()

    db_connection.close()

    return render_template('students.j2', style='styles/students.css', results=results, script='js/students.js')

@app.route('/insert_student', methods=['POST'])
def insert_student():
    '''INSERT new Student'''
    db_connection = db.connect_to_database()
    f_name = request.form.get('firstName')
    m_name = request.form.get('middleName')
    l_name = request.form.get('lastName')

    if m_name == "":
        m_name = None

    query = 'INSERT INTO Students(firstName, middleName, lastName) VALUES (%s, %s, %s);'
    db.execute_query(db_connection=db_connection, query=query, query_params=(f_name, m_name, l_name))

    db_connection.close()

    flash('Student successfully added.')
    return redirect(url_for('students'))

@app.route('/delete_student', methods=['POST'])
def delete_student():
    '''DELETE a Student'''
    db_connection = db.connect_to_database()
    student_id = request.form.get("Delete")
    query = 'DELETE FROM Students WHERE studentID=%s;'
    db.execute_query(db_connection=db_connection, query=query, query_params=(student_id,))

    db_connection.close()

    flash('Student successfully deleted.')
    return redirect(url_for('students'))

@app.route('/update_student', methods=['POST'])
def update_student():
    '''Updates a Student'''
    db_connection = db.connect_to_database()
    student_id = request.form.get('id')
    f_name = request.form.get('fname')
    m_name = request.form.get('mname')
    l_name = request.form.get('lname')

    if m_name == "":
        m_name = None

    query = 'UPDATE Students SET firstName= %s, middleName= %s, lastName= %s WHERE studentID= %s;'
    db.execute_query(db_connection=db_connection, query=query, query_params=(f_name, m_name, l_name, student_id))

    db_connection.close()

    flash('Student successfully updated.')
    return redirect(url_for('students'))

# Routes for Terms
@app.route('/terms', methods=['GET'])
def terms():
    '''SELECT all Terms and displays data'''
    db_connection = db.connect_to_database()

    query = 'SELECT * FROM Terms ORDER BY termID ASC;'
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()

    db_connection.close()

    return render_template('terms.j2', style='styles/terms.css',results=results, script='js/terms.js')

@app.route('/insert_term', methods=['POST'])
def insert_term():
    '''Insert a new Term'''
    db_connection = db.connect_to_database()

    session = request.form.get('termSession')
    year = int(request.form.get('termYear'))

    # Check for Year restrictions
    if year < 1901 or year > 2155:
        flash('Invalid year. Year must be between 1901 and 2155 inclusive.')
        db_connection.close()

        return redirect(url_for('terms'))

    # Check for duplicate entry
    query = 'SELECT * FROM Terms WHERE session=%s AND year=%s;'
    cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(session, year))
    results = cursor.rowcount
    
    if results == 0:
        query = 'INSERT INTO Terms(session, year) VALUES (%s, %s)'
        db.execute_query(db_connection=db_connection, query=query, query_params=(session, year))
        flash('Term successfully added.')
    else:
        flash('Error. Duplicate Term found!')

    db_connection.close()

    return redirect(url_for('terms'))

@app.route('/delete_term', methods=['POST'])
def delete_term():
    '''DELETE a Term'''
    db_connection = db.connect_to_database()
    term_id = request.form.get('Delete')
    query = 'DELETE FROM Terms WHERE termID=%s;'
    db.execute_query(db_connection=db_connection, query=query, query_params=(term_id,))

    db_connection.close()

    flash('Term successfully deleted.')
    return redirect(url_for('terms'))

# Route for Classes
@app.route('/classes', methods=['GET'])
def classes():
    '''Generates list of options for the insertion form and displays all classes available'''
    db_connection = db.connect_to_database()
    # Query to get all Department names for INSERT form
    dept_query = 'SELECT * FROM Departments;'
    dept_cursor = db.execute_query(db_connection=db_connection, query=dept_query)
    dept_results = dept_cursor.fetchall()

    # Query to get Terms for INSERT form
    term_query = 'SELECT CONCAT_WS(" ", session, year) AS term, termID AS id FROM Terms;'
    term_cursor = db.execute_query(db_connection=db_connection, query=term_query)
    term_results = term_cursor.fetchall()

    # Query to get Instructors for INSERT form
    inst_query = 'SELECT CONCAT_WS(" ", firstName, middleName, lastName) AS name, instructorID AS id FROM Instructors;'
    inst_cursor = db.execute_query(db_connection=db_connection, query=inst_query)
    inst_results = inst_cursor.fetchall()

    # Query to get Class data to display in table
    display_query = 'SELECT c.classID AS id, c.name, CONCAT_WS(" ", t.session, t.year) AS term, CONCAT_WS(" ", i.firstName, i.middleName, i.lastName) AS instructor, d.name as dept FROM Classes c LEFT JOIN Terms t ON t.termID = c.term LEFT JOIN Instructors i ON i.instructorID = c.instructor LEFT JOIN Departments d ON d.deptID = c.department;'
    display_cursor = db.execute_query(db_connection=db_connection, query=display_query)
    display_results = display_cursor.fetchall()

    db_connection.close()

    return render_template('classes.j2', style='styles/students.css', dept_results=dept_results, term_results=term_results, inst_results=inst_results, display_results=display_results, script='js/classes.js')

@app.route('/insert_class', methods=['POST'])
def insert_class():
    '''Inserts a new Class'''
    db_connection = db.connect_to_database()
    class_name = request.form.get('className')
    class_dept = request.form.get('classDepartment')
    class_term = request.form.get('classTerm')
    class_inst = request.form.get('classInstructor')

    if class_dept == "":
        class_dept = None

    if class_term == "":
        class_term = None

    if class_inst == "":
        class_inst = None

    insert_query = 'INSERT INTO Classes(name, department, term, instructor) VALUES (%s, %s, %s, %s);'
    db.execute_query(db_connection=db_connection, query=insert_query, query_params=(class_name, class_dept, class_term, class_inst))

    db_connection.close()

    flash('Class successfully added.')
    return redirect(url_for('classes'))

@app.route('/delete_class', methods=['POST'])
def delete_class():
    '''Deletes a Class'''
    db_connection = db.connect_to_database()
    class_id = request.form.get("Delete")
    query = 'DELETE FROM Classes WHERE classID=%s;'
    db.execute_query(db_connection=db_connection, query=query, query_params=(class_id,))

    db_connection.close()

    flash('Class successfully deleted.')
    return redirect(url_for('classes'))

@app.route('/update_class', methods=['POST'])
def update_class():
    '''Updates a Class'''
    db_connection = db.connect_to_database()
    class_id = request.form.get('updateid')
    class_name = request.form.get('updatename')
    class_dept = request.form.get('updatedept')
    class_term = request.form.get('updateterm')
    class_inst = request.form.get('updateinst')

    if class_dept == "":
        class_dept = None

    if class_term == "":
        class_term = None

    if class_inst == "":
        class_inst = None
    
    query = 'UPDATE Classes SET name= %s, department= %s, term= %s, instructor= %s WHERE classID= %s;'
    db.execute_query(db_connection=db_connection, query=query, query_params=(class_name, class_dept, class_term, class_inst, class_id))

    db_connection.close()

    flash('Class successfully updated.')
    return redirect(url_for('classes'))


# Routes for Departments
@app.route('/departments', methods=['GET', 'POST'])
def departments():
    '''SELECT all from Departments.'''
    db_connection = db.connect_to_database()
    query = 'SELECT * FROM Departments ORDER BY deptID ASC;'
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()

    db_connection.close()

    return render_template('departments.j2', style='styles/terms.css', results=results, script='js/departments.js')

@app.route('/delete_dept', methods=['POST'])
def delete_dept():
    '''Deletes a Department.'''
    db_connection = db.connect_to_database()
    dept_id = request.form.get("Delete")
    query = 'DELETE FROM Departments WHERE deptID = %s;'
    db.execute_query(db_connection=db_connection, query=query, query_params=(dept_id,))

    db_connection.close()

    flash('Department successfully deleted.')
    return redirect(url_for('departments'))

@app.route('/insert_dept', methods=['POST'])
def insert_dept():
    '''Inserts a new Department.'''
    db_connection = db.connect_to_database()
    dept_name = request.form.get('deptName')
    #Check for a duplicate department.
    query = 'SELECT * FROM Departments WHERE name=%s;'
    cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(dept_name,))
    results = cursor.rowcount

    if results == 0:
        query = 'INSERT INTO Departments(name) VALUES (%s);'
        db.execute_query(db_connection=db_connection, query=query, query_params=(dept_name,))
        flash('Department successfully added.')
    else:
        flash('Error. Duplicate Department found!')

    db_connection.close()

    return redirect(url_for('departments'))

@app.route('/update_dept', methods=['POST'])
def update_dept():
    '''Updates a Department.'''
    db_connection = db.connect_to_database()
    dept_id = request.form.get('id')
    dept_name = request.form.get('name')

    query = 'UPDATE Departments SET name = %s WHERE deptID = %s;'
    db.execute_query(db_connection=db_connection, query=query, query_params=(dept_name, dept_id))

    db_connection.close()

    flash('Department successfully updated.')
    return redirect(url_for('departments'))


# Routes for Instructors
@app.route('/instructors', methods=['GET', 'POST'])
def instructors():
    '''SELECT all from Instructors.'''
    db_connection = db.connect_to_database()
    # Query to get all Department names for INSERT form
    dept_query = 'SELECT * FROM Departments;'
    dept_cursor = db.execute_query(db_connection=db_connection, query=dept_query)
    dept_results = dept_cursor.fetchall()

    #Query to get all Instructor data and display it.
    display_query = 'SELECT Instructors.instructorID, Instructors.firstName, Instructors.middleName, Instructors.lastName, ' \
            'Departments.name as department FROM Instructors LEFT JOIN Departments ON Instructors.department = ' \
            'Departments.deptID ORDER BY instructorID ASC;'
    display_cursor = db.execute_query(db_connection=db_connection, query=display_query)
    display_results = display_cursor.fetchall()

    db_connection.close()

    return render_template('instructors.j2', style='styles/instructors.css', dept_results = dept_results,
                           results=display_results, script='js/instructors.js')

@app.route('/delete_instructor', methods=['POST'])
def delete_instructor():
    '''Deletes an Instructor.'''
    db_connection = db.connect_to_database()
    instructor_id = request.form.get("Delete")
    query = 'DELETE FROM Instructors WHERE instructorID = %s;'
    db.execute_query(db_connection=db_connection, query=query, query_params=(instructor_id,))

    db_connection.close()

    flash('Instructor successfully deleted.')
    return redirect(url_for('instructors'))

@app.route('/insert_instructor', methods=['POST'])
def insert_instructor():
    '''INSERTS a new Instructor.'''
    db_connection = db.connect_to_database()
    f_name = request.form.get('firstName')
    m_name = request.form.get('middleName')
    l_name = request.form.get('lastName')
    dept = request.form.get('classDepartment')
    
    if dept == "":
        dept = None

    if m_name == "":
        m_name = None

    query = 'INSERT INTO Instructors(firstName, middleName, lastName, department) VALUES (%s, %s, %s, %s);'
    db.execute_query(db_connection=db_connection, query=query, query_params=(f_name, m_name, l_name, dept))

    db_connection.close()

    flash('Instructor successfully added.')
    return redirect(url_for('instructors'))

@app.route('/update_instructor', methods=['POST'])
def update_instructor():
    '''Updates an Instructor'''
    db_connection = db.connect_to_database()
    instructor_id = request.form.get('updateid')
    f_name = request.form.get('updatefname')
    m_name = request.form.get('updatemname')
    l_name = request.form.get('updatelname')
    dept = request.form.get('updatedept')

    if m_name == "":
        m_name = None
    
    if dept == "":
        dept = None

    query = 'UPDATE Instructors SET firstName = %s, middleName = %s, lastName = %s, department = %s WHERE instructorID = %s;'
    db.execute_query(db_connection=db_connection, query=query, query_params=(f_name, m_name, l_name, dept, instructor_id))

    db_connection.close()

    flash('Instructor successfully updated.')
    return redirect(url_for('instructors'))


# Routes for StudentEnrollments
@app.route('/studentEnrollments', methods=['GET', 'POST'])
def studentEnrollments():
    '''SELECT all from Student Enrollments.'''
    db_connection = db.connect_to_database()
    # Query to get all Class names for INSERT form
    class_query = 'SELECT * FROM Classes;'
    class_cursor = db.execute_query(db_connection=db_connection, query=class_query)
    class_results = class_cursor.fetchall()

    # Query to get all Student names for INSERT form
    student_query = 'SELECT * FROM Students;'
    student_cursor = db.execute_query(db_connection=db_connection, query=student_query)
    student_results = student_cursor.fetchall()

    # Query to get all studentEnrollments for search
    enrollment_query = 'SELECT DISTINCT class FROM StudentEnrollments;'
    enrollment_cursor = db.execute_query(db_connection=db_connection, query=enrollment_query)
    enrollment_results = enrollment_cursor.fetchall()

    display_query = 'SELECT Classes.classID as classID, Classes.name as className, Students.studentID as studentID, Students.firstName as first, ' \
                    'Students.middleName as middle, Students.lastName as last FROM StudentEnrollments INNER JOIN Students ON ' \
                    'StudentEnrollments.student = Students.studentID INNER JOIN Classes ON StudentEnrollments.class = ' \
                    'Classes.classID ORDER BY classID ASC'
    display_cursor = db.execute_query(db_connection=db_connection, query=display_query)
    display_results = display_cursor.fetchall()

    db_connection.close()

    return render_template('studentEnrollments.j2', style='styles/studentEnrollments.css', class_results=class_results,
                           student_results=student_results, enrollment_results=enrollment_results,
                           display_results=display_results, script='js/studentEnrollments.js')


@app.route('/delete_studentEnrollment', methods=['POST'])
def delete_studentEnrollment():
    '''Deletes a StudentEnrollment.'''
    db_connection = db.connect_to_database()
    enrollment_id = request.form.get("Delete")
    split_enrollment = enrollment_id.split(",")
    class_id = split_enrollment[0]
    student_id = split_enrollment[1]
    query = 'DELETE FROM StudentEnrollments WHERE class = %s and student = %s'
    db.execute_query(db_connection=db_connection, query=query, query_params=(class_id, student_id))

    db_connection.close()

    flash('Student Enrollment successfully deleted.')
    return redirect(url_for('studentEnrollments'))


@app.route('/insert_studentEnrollment', methods=['POST'])
def insert_studentEnrollment():
    '''Inserts a new Student Enrollment'''
    db_connection = db.connect_to_database()
    class_id = request.form.get('class')
    student_id = request.form.get('student')

    # Check for duplicate entry
    query = 'SELECT * FROM StudentEnrollments WHERE class=%s AND student=%s;'
    cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(class_id, student_id))
    results = cursor.rowcount

    if results == 0:
        insert_query = 'INSERT INTO StudentEnrollments(class, student) VALUES (%s, %s)'
        db.execute_query(db_connection=db_connection, query=insert_query, query_params=(class_id, student_id))
        flash('Student Enrollment successfully added.')
    else:
        flash('Error. Duplicate Enrollment found!')

    db_connection.close()

    return redirect(url_for('studentEnrollments'))


@app.route('/search_studentEnrollment', methods=['POST'])
def search_studentEnrollment():
    '''Searches for all Students enrolled in a Class by Class ID.'''
    db_connection = db.connect_to_database()
    # Query to get all Class names for INSERT form
    class_query = 'SELECT * FROM Classes;'
    class_cursor = db.execute_query(db_connection=db_connection, query=class_query)
    class_results = class_cursor.fetchall()

    # Query to get all Student names for INSERT form
    student_query = 'SELECT * FROM Students;'
    student_cursor = db.execute_query(db_connection=db_connection, query=student_query)
    student_results = student_cursor.fetchall()

    # Query to get all studentEnrollments for search
    enrollment_query = 'SELECT DISTINCT class FROM StudentEnrollments;'
    enrollment_cursor = db.execute_query(db_connection=db_connection, query=enrollment_query)
    enrollment_results = enrollment_cursor.fetchall()

    class_id = request.form.get('enrollClass')
    query = 'SELECT Classes.classID as classID, Classes.name as className, Students.studentID as studentID, ' \
                   'Students.firstName as first, Students.middleName as middle, Students.lastName as last ' \
                   'FROM StudentEnrollments INNER JOIN Classes ON StudentEnrollments.class = Classes.classID ' \
                   'INNER JOIN Students WHERE StudentEnrollments.student = Students.studentID AND ' \
                   'StudentEnrollments.class = %s;'
    cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(class_id,))
    results = cursor.fetchall()

    display_query = 'SELECT Classes.classID as classID, Classes.name as className, Students.studentID as studentID, Students.firstName as first, ' \
                    'Students.middleName as middle, Students.lastName as last FROM StudentEnrollments INNER JOIN Students ON ' \
                    'StudentEnrollments.student = Students.studentID INNER JOIN Classes ON StudentEnrollments.class = ' \
                    'Classes.classID ORDER BY classID ASC'
    display_cursor = db.execute_query(db_connection=db_connection, query=display_query)
    display_results = display_cursor.fetchall()

    db_connection.close()

    return render_template('studentEnrollments.j2', style='styles/studentEnrollments.css', class_results=class_results,
                           student_results=student_results, enrollment_results=enrollment_results, results=results,
                           display_results=display_results, script='js/studentEnrollments.js')
