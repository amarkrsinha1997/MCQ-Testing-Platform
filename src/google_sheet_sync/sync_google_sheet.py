from .utils import get_worksheet, get_student_data

class SyncGoogleSheet:
    def __init__(self, data_frame, student):
        self.student = student
        self.data_frame = data_frame

        id_df = self.data_frame.get('Student Id', None)
        # when there is no header or data in the sheet
        # create a new headers
        if id_df is None:
            self.create_a_new_record_in_sheet()
        # when there is headers in the table
        else:
            student_row = self.data_frame[id_df == self.student.id]
            # create a new record if id is not present
            if student_row.empty:
                self.create_a_new_record_in_sheet()
            # update a record if id is present
            else:
                self.update_from_chanakya_to_sheet()

    def replace_NaN(self):
        """
            Updates the DataFrame NaN value to '' string.
        """
        # for removing NaN values that are set for None values by default in pandas
        self.data_frame.fillna(value='', inplace=True)


    def create_a_new_record_in_sheet(self):
        """
            Helps to create a new row of student details on Google sheets using DataFrame.
        """

        # student row as dictionary to add in the DataFrame
        student_row = get_student_data({}, self.student)
        self.data_frame = self.data_frame.append(student_row, ignore_index=True)

        # #updating the sheet with new DataFrame
        self.replace_NaN()


    def update_from_chanakya_to_sheet(self):
        """
            Helps to Sync a new row of student details on google sheets using DataFrame.
        """
        student_id = self.student.id

        # get the student row as DataFrame
        id_df = self.data_frame['Student Id']
        student_row_df = self.data_frame[id_df == student_id]

        # getting the updated data_frame and adding to data_frame
        updated_data_frame = get_student_data(student_row, student)(student_row_df, self.student)
        self.data_frame.update(updated_data_frame)
        self.replace_NaN()
