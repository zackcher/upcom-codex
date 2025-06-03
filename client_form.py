from flask import Flask, request, render_template_string
import gspread
from oauth2client.service_account import ServiceAccountCredentials

SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
SHEET_ID = "YOUR_SHEET_ID"  # replace with the same sheet id as scraper
FORM_SHEET = "ClientSubmissions"

def get_sheet(tab_name: str):
    credentials = ServiceAccountCredentials.from_json_keyfile_name('service_account.json', SCOPE)
    gc = gspread.authorize(credentials)
    sh = gc.open_by_key(SHEET_ID)
    try:
        ws = sh.worksheet(tab_name)
    except gspread.WorksheetNotFound:
        ws = sh.add_worksheet(title=tab_name, rows="100", cols="20")
    return ws

app = Flask(__name__)

FORM_HTML = """
<!doctype html>
<title>Client Form</title>
<h1>Enter contact info</h1>
<form method=post>
    <label for=email>Email:</label>
    <input type=email name=email required><br>
    <label for=phone>Phone:</label>
    <input type=tel name=phone required><br>
    <input type=submit value=Submit>
</form>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        email = request.form.get('email')
        phone = request.form.get('phone')
        ws = get_sheet(FORM_SHEET)
        ws.append_row([email, phone])
        return 'Submitted successfully!'
    return render_template_string(FORM_HTML)

if __name__ == '__main__':
    app.run(debug=True)
