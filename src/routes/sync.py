from flask_restplus import Resource, reqparse, fields, Namespace
from chanakya.src import app, db
from chanakya.src.models import Student


from chanakya.src.google_sheet_sync.utils import get_worksheet
from chanakya.src.google_sheet_sync.sync_database import SyncChanakya
from chanakya.src.google_sheet_sync.sync_google_sheet import SyncGoogleSheet

api = Namespace('sync', description='Handle complete online test of students')

@api.route('/start_sync')
class StartSync(Resource):
    put_payload_model = api.model('POST_start_sync_payload',{
        'direction':fields.String(enum=['chanakya', 'google_sheet'], required=True)
    })
    START_SYNC_DESCRIPTION = """
        Description:

        Possible values of different JSON keys which can be passed.

        - 'direction': ['chanakya', 'google_sheet']

        Pass chanakya when you want to sync the chanakya with the google sheet and when you want to sync google sheet pass google_sheet in direction.
    """

    @api.doc(description=START_SYNC_DESCRIPTION)
    @api.expect(put_payload_model)
    def put(self):
        args = api.payload
        direction = args.get('direction')

        if direction == 'chanakya':
            #Syncing the chanakya from the googlesheet
            SyncChanakya()
        elif direction == 'google_sheet':
            # getting worksheet and dataframe from the google_sheet
            worksheet = get_worksheet()
            data_frame = worksheet.get_as_df()

            # updating each student to the data_frame from chanakya
            for student in Student.query.all():
                syncgooglesheet = SyncGoogleSheet(data_frame, student)
                data_frame = syncgooglesheet.data_frame

            # updating the complete sheet with new data_frame
            worksheet.set_dataframe(data_frame, 'A1')
        return {
            'success':True
        }
