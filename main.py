from flask import Flask, render_template, flash, request, redirect, url_for
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField, SelectField, RadioField
 
# App config.
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'
 
class SystemChoice(Form):
    db = SelectField('Databases:', 
        choices = [('scidb', 'array (SciDB)'), ('vertica', 'columnar (Vertica)'), ('pg', 'row (PostgreSQL)')], 
        validators=[validators.required()])

    lang = SelectField('Languages:', 
        choices = [('r', 'R'), ('python', 'Python')], 
        validators=[validators.required()])

    dataset = SelectField('Datasets:', 
        choices = [('kdd', 'KDD_net (n x d)'), ('diabetes', 'Pima Indian Diabetes (n x d)'), ('wine', 'Wine Quality (n x d)')], 
        validators=[validators.required()])

    gamma_opt_density = RadioField('Density: ', choices = [('dense', 'Dense'), ('sparse', 'Sparse')])

    gamma_opt_diag = RadioField('Diagonal/Full: ', choices = [('diagonal', 'Diagonal'), ('full', 'Full')])

    gamma_opt_Y_col = RadioField('Y column?: ', choices = [('yes', 'Yes'), ('no', 'No')])

    gamma_opt_groupby = RadioField('GROUP BY column?: ', choices = [('yes', 'Yes'), ('no', 'No')])

    run = SubmitField("Run")

def call_vertica():
    print "Calling a vertica"
 
@app.route("/", methods=['GET', 'POST'])
def hello():
    form = SystemChoice(request.form)
 
    print form.errors
    if request.method == 'POST':
        db = request.form['db']
        lang = request.form['lang']
        dataset = request.form['dataset']
 
        if form.validate():
            # Save the comment here.
            #flash('Input: ' + db + ' ' + lang + ' ' + dataset)
            
            return redirect(url_for('get_result', db=db, lang=lang, dataset=dataset))
        else:
            flash('All the form fields are required. ')
 
    return render_template('hello.html', form=form)

@app.route("/result/<db>/<lang>/<dataset>", methods=['GET'])
def get_result(db, lang, dataset):
    # params = request.args.to_dict()
    # print params
    return 'input:' + db + ' ' + lang + ' ' + dataset

if __name__ == "__main__":
    app.run()
