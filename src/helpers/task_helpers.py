import os, pandas, requests
from io import BytesIO
from bs4 import BeautifulSoup
from flask import render_template
from subprocess import Popen, PIPE, STDOUT
from chanakya import ROOT_DIR
from chanakya.src import app
from chanakya.src.models import Questions


def render_pdf_phantomjs(template_name , **kwargs):
    """
        Helper that helps to convert htmll template to a pdf using phantomjs
        which is installed locally and pdf.js to generate an A4 size pdf.

        Params:
            `template_name` : Name of the template which need to be converted to PDF.
            `kwargs` : All the instance or data required inside the render_template to render it to HTML.
        Return:
            `pdf_string`: Pdf which has been rendered for the template as binary format.
    """

    # getting the path files to run
    phantomjs_path = ROOT_DIR + '/node_modules/phantomjs/bin/phantomjs'
    pdfjs_path = os.path.dirname(os.path.realpath(__file__)) + '/scripts/pdf.js'

    # creating an html file ready_for_generation.html
    file = open('ready_for_generation.html', 'w')
    html = render_template(template_name, **kwargs)
    file.write(html)
    file.close()

    # creating a pdf for ready_for_generation.html of size A4
    p = Popen([phantomjs_path, pdfjs_path, 'ready_for_generation.html','ready_for_generation.pdf', 'A4'], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
    p.communicate()

    # reading the pdf data out of the ready_for_generation.pdf file
    pdf_string = open('ready_for_generation.pdf', 'rb').read()

    # removing the file so it doesn't consume space
    os.remove('ready_for_generation.html')
    os.remove('ready_for_generation.pdf')

    return pdf_string


def get_attempts(row, enrollment):
    """
        Helps to extract the attempts of student from dataframe row which is created by pandas
        by reading a csv format of question 1-18 with student answer.

        Params:
            `row`: row dataframe of pandas which carry a row of student data from which we will get student question attempts.
            `enrollment`: the enrollment instance which we need to extract question set.

        Return attempts a list of object which look like below
            [
                {
                    'selected_option_id': 3,
                    'question_id':1
                },
                {
                    'question_id': 2,
                    'answer': 216
                },
                {
                    'question_id': 3,
                    'selected_option_id':
                }
            ]
    """
    attempts = []
    question_set = enrollment.question_set
    questions = question_set.get_questions()

    for i in range(0,18):
        question_num = str(i+1)
        attempt = {}
        question = questions[i]
        question_attempt = row.get(question_num)

        if question_attempt:
            if question.type.value == 'MCQ':
                options = question.options.all()
                option_index = ord(question_attempt)-ord('A')
                attempt['selected_option_id'] = options[option_index].id
                attempt['question_id'] = question.id
            else:
                attempt['question_id'] = question.id
                attempt['answer'] = question_attempt
            attempts.append(attempt)
    return attempts

def get_dataframe_from_csv(csv_url):
    """
        Helps to create a dataframe using pandas for the CSV file containing the partner offline test details.
        Require the url of CSV File
        Params:
            `args`: "csv_url" the Url of the csv file on s3

        Return a list of rows of student details who gave the offline test as DataFrame instance.
    """

    # getting the csv from the s3_url and converting it to DataFrame of pandas
    response = requests.get(csv_url)
    csv_buffer = BytesIO(response.content)
    dataframe = pandas.read_csv(csv_buffer, keep_default_na=False)

    rows = [row[1] for row in dataframe.iterrows()]
    return rows
