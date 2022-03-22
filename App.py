from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, length
import datetime

app = Flask(__name__)
app.secret_key = "Secret key"

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://math:uJGCwUM2@150.254.5.101:3306/math'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

list_building = ["BM", "BL", "CW", "BT", "WTCh", "EL", "WA/WIZ", "CM", "Łącznik"]

day_order = ['pn', 'wt', 'sr', 'cz', 'pt', 'so', 'nd']

list_day = ['Poniedziałek', 'Wtorek', 'Środa', 'Czwartek', 'Piątek']

list_department = ["WA", "WARiE", "WIiT", "WILiT", "WIMiFT", "WIM", "WISiE", "WIZ", "WTCh"]

list_course = ['Architecture',
               'Architektura',
               'Architektura wnętrz',
               'Artificial intelligence',
               'Automatic control and robotics',
               'Automatyka i robotyka',
               'B',
               'Bioinformatyka',
               'Budownictwo',
               'C',
               'Chemical technology',
               'Civil engineering',
               'Construction and exploatation of means of transport',
               'E',
               'Edukacja techniczno-informatyczna',
               'Electronics and telecommunications',
               'Elektroenergetyka',
               'Elektromobilność',
               'Elektronika i telekomunikacja',
               'Elektrotechnika',
               'Energetyka',
               'Engineering management',
               'Erasmus',
               'F',
               'Fizyka techniczna',
               'I',
               'Informatyka',
               'Inżynieria bezpieczeństwa',
               'Inżynieria biomedyczna',
               'Inżynieria chemiczna i procesowa',
               'Inżynieria farmaceutyczna',
               'Inżynieria lotnicza',
               'Inżynieria materiałowa',
               'Inżynieria środowiska',
               'Inżynieria zarządzania',
               'K',
               'Konstrukcja i eksploatacja środków transportu',
               'L',
               'Logistyka',
               'Lotnictwo i kosmonautyka',
               'Lotnictwo i kosmonautyka-prakt.',
               'M',
               'Matematyka w technice',
               'Mechanical and automotive engineering',
               'Mechanika i budowa maszyn',
               'Mechanika i budowa pojazdów',
               'Mechatronika',
               'S',
               'Sustainable Building Engineering',
               'T',
               'Technologia chemiczna',
               'Technologie obiegu zamkniętego',
               'Technologie ochrony środowiska',
               'Teleinformatyka',
               'Transport',
               'Z',
               'Zarządzanie i inżynieria produkcji'
               ]

list_name = ['Algebra',
             'Algebra abstrakcyjna',
             'Algebra liniowa',
             'Algebra liniowa z geometrią analityczną',
             'Algebra z geometrią',
             'Algorytmy i struktury danych',
             'Analiza funkcjonalna',
             'Analiza matematyczna',
             'Analiza matematyczna 2',
             'Analiza matematyczna I',
             'Analiza matematyczna i algebra liniowa',
             'Analiza matematyczna II',
             'Analiza zespolona',
             'Applied mathematics and mathematical methods',
             'B',
             'Badania operacyjne',
             'C',
             'Calculus I',
             'Calculus II',
             'D',
             'Descriptive geometry',
             'Descriptive statistics ',
             'E',
             'Ekonomia matematyczna',
             'Elementy analizy numerycznej',
             'G',
             'Geometria wykreślna',
             'Grafika inżynierska',
             'H',
             'Historia matematyki',
             'I',
             'Introduction to mathematics',
             'K',
             'Komputerowa analiza inżynierska',
             'M',
             'Matematyczne wspomaganie decyzji',
             'Matematyka',
             'Matematyka dyskretna',
             'Matematyka I (Analiza)',
             'Matematyka II (Algebra)',
             'Matematyka II (Rachunek prawdopodob.)',
             'Matematyka stosowana',
             'Matematyka stosowana i metody matemat.',
             'Mathematics',
             'Mathematics I',
             'Mathematics I (Analysis)',
             'Mathematics II',
             'Mathematics II (Algebra)',
             'Metoda różnic skończonych',
             'Metody numeryczne',
             'Metody numeryczne i statystyka',
             'Metody numeryczne w technice',
             'Metody optymalizacji',
             'Metody probabilistyczne i statystyka',
             'Metody statystyczne w bad. nauk.',
             'N',
             'Numeryczna algebra liniowa',
             'O',
             'Obliczenia symboliczne',
             'P',
             'Podstawy statystyki',
             'Praca dyplomowa inżynierska',
             'Probabilistyka i statystyka',
             'Probabilistyka matematyczna',
             'Procesy stochastyczne',
             'Programowanie I',
             'Programowanie II',
             'Programowanie liniowe i kwadratowe',
             'Przedmiot obieralny',
             'R',
             'Rachunek prawdopodobieństwa',
             'Równania różnicowe',
             'Równania różniczkowe i przekształcenia całkowe',
             'Równania różniczkowe zwyczajne',
             'S',
             'Selected topics in mathematics',
             'Selected topics in mathematics I',
             'Selected topics in mathematics II',
             'Seminarium dyplomowe',
             'Statistics',
             'Statystyka',
             'Statystyka dla inżynierów',
             'Statystyka i analiza danych',
             'Statystyka inżynierska',
             'Statystyka matematyczna',
             'Statystyka opisowa',
             'Statystyka opisowa z elementami stosowanej',
             'T',
             'Technologie informacyjne I',
             'Technologie informacyjne II',
             'Teoria eksperymentu',
             'Teoria liczb i elementy kryptografii',
             'Teoria niezawodności',
             'W',
             'Wielowymiarowa analiza statystyczna',
             'Wstęp do programowania',
             'Wstęp do teorii aproksymacji',
             'Wybrane zagadnienia z matematyki']


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.String(10))
    week = db.Column(db.Integer)
    start = db.Column(db.Time)
    end = db.Column(db.Time)
    unit_type = db.Column(db.String(1))
    unit_name = db.Column(db.String(100))
    unit_department = db.Column(db.String(100))
    unit_course = db.Column(db.String(100))
    unit_degree = db.Column(db.Integer)
    unit_term = db.Column(db.Integer)
    unit_building = db.Column(db.String(100))
    unit_room = db.Column(db.String(100))
    comment = db.Column(db.String(100))
    data_user = db.Column(db.String(50))

    def __init__(self, day, week, start, end, unit_type, unit_name, unit_department, unit_course, unit_degree,
                 unit_term, unit_building, unit_room, comment, data_user):
        self.day = day
        self.week = week
        self.start = start
        self.end = end
        self.unit_type = unit_type
        self.unit_name = unit_name
        self.unit_department = unit_department
        self.unit_course = unit_course
        self.unit_degree = unit_degree
        self.unit_term = unit_term
        self.unit_building = unit_building
        self.unit_room = unit_room
        self.comment = comment
        self.data_user = data_user


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(50), nullable=False, unique=True)
    user_pass = db.Column(db.String(50), nullable=False)
    user_title = db.Column(db.String(50), nullable=False)
    user_depar = db.Column(db.String(50), nullable=False)
    user_room = db.Column(db.Integer, nullable=False)


class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), length(min=4, max=20)], render_kw={"placehodler": "Username"})
    password = PasswordField(validators=[InputRequired(), length(min=4, max=20)], render_kw={"placehodler": "Password"})
    submit = SubmitField("Zaloguj się")


@app.route('/', methods=['GET', 'POST'])
def Index():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(user_name=form.username.data).first()
        if user:
            if user.user_pass == form.password.data:
                login_user(user)
                return redirect(url_for('home'))
    return render_template("login.html", form=form)


@app.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    all_data = Data.query.all()

    all_data = sorted(all_data, key=lambda x: list_day.index(x.day), reverse=False)

    return render_template('index.html', units=all_data, list_name=list_name, list_course=list_course,
                           list_department=list_department, list_day=list_day,list_building=list_building)


class Unit():
    day = None
    start = None
    end = None
    unit_type = None
    unit_name = None
    unit_course = None
    unit_room = None
    data_user = None
    comment = None
    hours = None
    unit_building = None

    def __init__(self, day, start, end, unit_type, unit_name, unit_course, unit_room, unit_building,data_user, comment, hours):
        self.day = day
        self.start = start
        self.end = end
        self.unit_type = unit_type
        self.unit_name = unit_name
        self.unit_course = unit_course
        self.unit_room = unit_room
        self.unit_building = unit_building
        self.data_user = data_user
        self.comment = comment
        self.hours = hours


@app.route('/generate', methods=['GET', 'POST'])
@login_required
def generate():
    all_data = Data.query.all()
    all_data = sorted(all_data, key=lambda x: list_day.index(x.day), reverse=False)

    units = []
    for date in all_data:
        if date.data_user == current_user.user_name:
            unit_type = None

            hours = ''

            day = day_order[list_day.index(date.day)]
            if date.week == 1:
                week = "_np"
            elif date.week == 2:
                week = "_p"
            else:
                week = ""

            start = str(date.start)[:2] + str(date.start)[3:5]
            end = str(date.end)[:2] + str(date.end)[3:5]

            if start not in ['0800', '0945', '1145', '1330', '1510', '1650', '1830'] or end not in ['0930', '1115',
                                                                                                    '1315',
                                                                                                    '1500', '1640',
                                                                                                    '1820',
                                                                                                    '2000']:
                hours = start[:2] + ':' + start[2:] + ' - ' + end[:2] + ':' + end[2:]

            end = datetime.timedelta(hours=int(str(date.end)[:2]),
                                     minutes=int(str(date.end)[3:5])) - datetime.timedelta(
                minutes=5)
            end = str(end).split(':')[0].rjust(2, '0') + str(end).split(':')[1].rjust(2, '0')

            if date.unit_type == 'W':
                unit_type = "Wykład"
            elif date.unit_type == 'C':
                unit_type = "Ćwiczenia"
            elif date.unit_type == 'P':
                unit_type = "Projekt"
            elif date.unit_type == 'S':
                unit_type = "Seminarium"
            elif date.unit_type == 'D':
                unit_type = "Dyżur"
            elif date.unit_type == 'L':
                unit_type = "Laboratorium"

            unit_room = date.unit_room + ' ' + date.unit_building

            unit_course = date.unit_department + ' ' + str(date.unit_course) + ' st. ' + str(
                date.unit_degree) + ' sem. ' + str(date.unit_term)
            units.append(Unit(day + week, start, end, unit_type, date.unit_name, unit_course, unit_room,'', date.data_user,
                              date.comment, hours))

    return render_template('calendar.html', units=units)

@app.route('/generate_all', methods=['GET', 'POST'])
@login_required
def generate_all():
    all_data = Data.query.all()
    all_data = sorted(all_data, key=lambda x: list_day.index(x.day), reverse=False)

    all_users = User.query.all()
    all_users = sorted(all_users, key=lambda x: x.user_name.split(' ')[1], reverse=False)

    units = []
    for date in all_data:

        day = day_order[list_day.index(date.day)]
        if date.week == 1:
            week = "_np"
        elif date.week == 2:
            week = "_p"
        else:
            week = ""

        start = str(date.start)[:2] +':'+ str(date.start)[3:5]
        end = str(date.end)[:2] +':'+ str(date.end)[3:5]

        comment = start +' - '+ end +' '+ date.unit_type +' '+ str(date.unit_room) +'<sup>' + date.unit_building+'</sup>'

        unit_course = date.unit_department + ' ' + str(date.unit_course) + ' st. ' + str(
            date.unit_degree) + ' sem. ' + str(date.unit_term)
        units.append(Unit(day, start, end, date.unit_type, date.unit_name, unit_course, date.unit_room, date.unit_building, date.data_user,
                          comment,''))

    return render_template('calendar_all.html', units=units, all_users = all_users)



@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('Index'))


@app.route('/insert', methods=['POST'])
@login_required
def insert():
    if request.method == 'POST':
        day = request.form['day']
        week = request.form['week']
        start = request.form['start']
        end = request.form['end']
        unit_type = request.form['unit_type']
        unit_name = request.form['unit_name']
        unit_department = request.form['unit_department']
        unit_course = request.form['unit_course']
        unit_degree = request.form['unit_degree']
        unit_term = request.form['unit_term']
        unit_building = request.form['unit_building']
        unit_room = request.form['unit_room']
        comment = request.form['comment']
        data_user = request.form['data_user']

        my_data = Data(day, week, start, end, unit_type, unit_name, unit_department, unit_course, unit_degree,
                       unit_term, unit_building, unit_room, comment, data_user)

        db.session.add(my_data)
        db.session.commit()

        flash('POMYŚLNIE DODANO ZAJĘCIA')
        return redirect(url_for('home'))


@app.route('/update', methods=['GET', 'POST'])
@login_required
def update():
    if request.method == 'POST':
        my_data = Data.query.get(request.form.get('id'))

        my_data.day = request.form['day']
        my_data.week = request.form['week']
        my_data.start = request.form['start']
        my_data.end = request.form['end']
        my_data.unit_type = request.form['unit_type']
        my_data.unit_name = request.form['unit_name']
        my_data.unit_department = request.form['unit_department']
        my_data.unit_course = request.form['unit_course']
        my_data.unit_degree = request.form['unit_degree']
        my_data.unit_term = request.form['unit_term']
        my_data.unit_building = request.form['unit_building']
        my_data.unit_room = request.form['unit_room']
        my_data.comment = request.form['comment']
        my_data.data_user = request.form['data_user']

        db.session.commit()
        flash("POMYŚLNIE ZEDYTOWANO ZAJĘCIA")

        return redirect(url_for('home'))


@app.route('/delete/<id>/', methods=['GET', 'POST'])
@login_required
def delete(id):
    my_data = Data.query.get(id)
    db.session.delete(my_data)
    db.session.commit()

    flash("POMYŚLNIE USUNIĘTO ZAJĘCIA")

    return redirect(url_for('home'))


@app.route('/duplicate/<id>/', methods=['GET', 'POST'])
@login_required
def duplicate(id):
    my_data = Data.query.get(id)

    my_duplicate_data = Data(my_data.day, my_data.week, my_data.start, my_data.end, my_data.unit_type,
                             my_data.unit_name, my_data.unit_department, my_data.unit_course, my_data.unit_degree,
                             my_data.unit_term, my_data.unit_building, my_data.unit_room, my_data.comment,
                             my_data.data_user)
    db.session.add(my_duplicate_data)
    db.session.commit()

    flash("POMYŚLNIE ZDUPLIKOWANO ZAJĘCIA")

    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)
