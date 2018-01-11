from flask import Flask, render_template, flash, request, redirect, url_for
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField, SelectField, RadioField, FileField
 
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
        choices = [('kdd', 'KDD_net'), ('diabetes', 'Pima Indian Diabetes'), ('wine', 'Wine Quality')], 
        validators=[validators.required()])

    fileName = FileField()

    gamma_opt_method = SelectField('Methods:', 
        choices = [('sql', 'SQL Query'), ('udf', 'User Defined Function')], 
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
            return redirect(url_for('get_result', db=db, lang=lang, dataset=dataset))
        else:
            flash('All the form fields are required. ')
 
    return render_template('hello.html', form=form)

@app.route("/result/<db>/<lang>/<dataset>", methods=['GET'])
def get_result(db, lang, dataset):
    # params = request.args.to_dict()
    # print params
    linreg = "beta coeficients <br>\
    [0] -0.8538942665<br>\
    [1]  0.0205918715<br>\
    [2]  0.0059202729<br>\
    [3] -0.0023318790<br>\
    [4]  0.0001545198<br>\
    [5] -0.0001805345<br>\
    [6]  0.0132440315<br>\
    [7]  0.1472374386<br>\
    [8]  0.0026213938<br>"
    return "Linear Regression: R+DBMS: <br>" + linreg

if __name__ == "__main__":
    app.run()
