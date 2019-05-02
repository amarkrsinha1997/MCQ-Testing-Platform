import pygsheets
from chanakya.src import app
from .config import SERVICE_FILE, SHEET_NAME, DATE_TIME_FORMAT

def get_worksheet():
    """
        Helps to get the google work sheet instance and connect using the service_file in config which
        path to service_file to use Google Drive API and the sheet_name on which the whole data should be sync.

        Return:
            worksheet instance made by pygsheets.
    """

    google_drive = pygsheets.authorize(service_file=SERVICE_FILE)
    sheet = google_drive.open(SHEET_NAME)
    worksheet = sheet.sheet1
    return worksheet

def get_test_duration(enrollment):
    """
        Helps to calculate the Test Duration of the student to find how quickly have he given a test or haven't he cheated in it.
        Params:
            `enrollment` : EnrolmentKey instance.
        Return:
            `time_taken`: If student has gave the test it return the duration as format (1h :2m :23s)
                          else it return None
    """

    if enrollment.is_test_ended():
        seconds = (enrollment.test_end_time - enrollment.test_start_time).seconds
        hours  = seconds//(60*60)
        seconds = seconds%(60*60)

        minutes = seconds//60
        seconds = seconds%60
        time_taken = '{0}h :{1}m :{2}s '.format(hours, minutes, seconds)
        return time_taken
    return None

def get_student_data(student_row, student):
    """
        The function helps to structured student instance data as given below either in a dictionary
        or data_frame.
        In dictionary when we need to create a new record in sheet
        In data_frame when we need to update a record in the sheet
        {
            'Name':'Amar Kumar Sinha',
            'Student Id': 1,
            'Gender': 'MALE',
            'Caste':'OBC',
            'Stage':'PERSONAL DETAIL SUBMITTED',
            'Date of Birth':18-09-1997,
            'Religion':None,
            'Monthly Family Income':None,
            ...
            ...
            ...
        }

        Params:
            `student_row` : Contains Empty dictionary {} when need to create a new record else contains
                            a data_frame.
            `student` : Student class instance through which we can extract all the link data.


        Return:
            The dictionary created below.
            {
                'Name':'Amar Kumar Sinha',
                'Student Id': 1,
                'Gender': 'MALE',
                'Date of Birth':18-09-1997,
                'Religion':None,
                'Total Family Member':None,
                ...
                ...
                ...
            }
    """
    enrollment = student.enrollment_keys.first()

    main_contact = student.contacts.filter_by(main_contact=True).first()
    contact = student.contacts.filter_by(main_contact=False).first()

    number_of_rqc = 0

    student_row['Name'] = student.name
    student_row['Gender'] = student.gender.value if student.gender else None
    student_row['Student Id'] = student.id
    student_row['Date of Birth'] = student.dob.strftime(DATE_TIME_FORMAT) if student.dob else None
    student_row['Caste'] = student.caste.value if student.caste else None
    student_row['Stage'] = student.stage
    student_row['Religion'] = student.religion.value if student.religion else None
    student_row['Monthly Family Income'] = student.monthly_family_income
    student_row['Total Family Member'] = student.total_family_member
    student_row['Family Member Income Detail'] = student.family_member_income_detail

    if main_contact:
        number_of_rqc += main_contact.incoming_calls.filter_by(call_type = app.config['INCOMING_CALL_TYPE'].rqc).count()
        student_row['Main Contact'] =  main_contact.contact

    if contact:
        number_of_rqc += contact.incoming_calls.filter_by(call_type = app.config['INCOMING_CALL_TYPE'].rqc).count()
        student_row['Alternative Contact'] = contact.contact

    student_row['Number Incoming RQC'] = number_of_rqc

    if enrollment:
        student_row['Enrollment Key'] = enrollment.key
        student_row['Test Score'] = enrollment.score
        student_row['Test Duration'] = get_test_duration(enrollment)
    else:
        student_row['Enrollment Key'] = None
        student_row['Test Score'] = None
        student_row['Test Duration'] = None

    return student_row
