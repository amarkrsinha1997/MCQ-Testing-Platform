from datetime import datetime
from .utils import get_worksheet
from .config import DATE_TIME_FORMAT
from chanakya.src import db, app
from chanakya.src.models import Student

class SyncChanakya:
    def __init__(self):
        self.worksheet = get_worksheet()
        self.data_frame = self.worksheet.get_as_df()
        self.update_from_sheet_to_chanakya()

    def update_from_sheet_to_chanakya(self):
        """
            Sync the data of student on Google Sheets to Chanakya.
            The function iterate over each data_frame and search for the student id in Database
            and update it all one by one.
        """
        # self.data_frame.replace(to_replace='', value=None,inplace=True)

        # createing list of student as a row which was initally column wise
        # due to pandas dataframe
        student_rows = [row[1] for row in self.data_frame.iterrows()]

        # If there is any data on sheet
        if student_rows:
            for student_row in student_rows:
                student_id = student_row['Student Id']
                student = Student.query.get(student_id)

                student.name = student_row['Name']

                if student_row['Date of Birth']:
                    student.dob = datetime.strptime(student_row['Date of Birth'], DATE_TIME_FORMAT)
                if student_row['Gender']:
                    student.gender = app.config['GENDER'](student_row['Gender'])
                if student_row['Caste']:
                    student.caste = app.config['CASTE'](student_row['Caste'])
                if student_row['Religion']:
                    student.religion = app.config['RELIGION'](student_row['Religion'])

                stage = student_row['Stage'] or None
                if stage and student.stage != stage:
                    student.change_stage(stage)

                student.monthly_family_income = student_row['Monthly Family Income'] or None
                student.total_family_member = student_row['Total Family Member'] or None
                student.family_member_income_detail = student_row['Family Member Income Detail'] or None

                ## TODO: something to add new contact or update old contact
                db.session.add(student)

            db.session.commit()
