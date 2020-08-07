from flask import Flask, request, render_template
app = Flask(__name__)

@app.route('/')
def home_page():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit_textarea():
    # store the given text in a variable
    text = request.form.get("text")

    # split the text to get each line in a list
    text2 = text.split('\n')

    # change the text (add 'Hi' to each new line)
    text_changed = ''.join(['<br>Hi ' + line for line in text2])
    # (i used <br> to materialize a newline in the returned value)

    return "You entered: {}".format(text_changed)




@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()
