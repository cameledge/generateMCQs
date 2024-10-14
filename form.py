import json
from google.oauth2 import service_account
from googleapiclient.discovery import build

def create_google_quiz(formId, mcqs):

    try:
        mcqs_ = json.loads(mcqs)

        scopes = ['https://www.googleapis.com/auth/forms.body']
        ## Service credential file here. (see )
        credentials_path = './atomic-rune-391314-ef1d03d774b2.json'

        # Create a service account credentials object
        credentials = service_account.Credentials.from_service_account_file(credentials_path, scopes=scopes)
        # Build the Google Forms API service
        service = build('forms', 'v1', credentials=credentials)
        
        update = {
                "requests": [
                    {
                    "updateSettings": {
                        "settings": {
                        "quizSettings": {
                            "isQuiz": True
                        }
                        },
                        "updateMask": "quizSettings"
                    }
                    }
                ]
            }

        request = service.forms().batchUpdate(
            body=update,
            formId=formId
            ).execute()
        
    except:
        return 'Error accessing the Quiz. Check form ID. Check if you have added app to Quiz list of collaboraters'
        
    try:
        count = 0
        for q in mcqs_:

            question = {
            "requests": [
                {
                "createItem": {
                    "item": {
                    "title": q['Question'].replace('\n','\r'), # newline \n replaced with \r because i was getting error
                    "questionItem": {
                        "question": {
                        "choiceQuestion": {
                            "options": [
                            {
                                "value": q['A']
                            },
                            {
                                "value": q['B']
                            },
                            {
                                "value": q['C']
                            },
                            {
                                "value": q['D']
                            }
                            ],
                            "type": "RADIO"
                        },
                        "required": True,
                        "grading": {
                            "pointValue": 1,
                            "correctAnswers": {
                            "answers": [
                                {
                                "value": q[q['correct_choice']]
                                }
                            ]
                            }
                        }
                        }
                    }
                    },
                    "location": {
                    "index": 0
                    }
                }
                }
            ]
            }

            request = service.forms().batchUpdate(
                body=question,
                formId=formId
                ).execute()
            count += 1
    except:
        print('Problem with a Question')

    return f'Done. {count} MCQs added'