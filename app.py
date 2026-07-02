from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "medicarepro123"

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hospital.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ---------------- MODELS ----------------

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    disease = db.Column(db.String(100), nullable=False)


class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    specialization = db.Column(db.String(100), nullable=False)
    experience = db.Column(db.Integer, nullable=False)


class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)

    appointment_date = db.Column(db.String(50), nullable=False)

    patient = db.relationship('Patient', backref='appointments')
    doctor = db.relationship('Doctor', backref='appointments')


# Create DB
with app.app_context():
    db.create_all()   


# ---------------- HOME ----------------
@app.route('/')
def home():
    return redirect(url_for('dashboard'))


# ---------------- DASHBOARD ----------------
@app.route('/dashboard')
def dashboard():
    return render_template(
        'dashboard.html',
        patient_count=Patient.query.count(),
        doctor_count=Doctor.query.count(),
        appointment_count=Appointment.query.count()
    )


# ---------------- PATIENTS ----------------
@app.route('/patients')
def patients():
    return render_template('patients.html', patients=Patient.query.all())


@app.route('/add_patient', methods=['GET', 'POST'])
def add_patient():
    if request.method == 'POST':
        db.session.add(Patient(
            name=request.form['name'],
            age=request.form['age'],
            disease=request.form['disease']
        ))
        db.session.commit()
        return redirect(url_for('patients'))

    return render_template('add_patient.html')


@app.route('/delete_patient/<int:id>')
def delete_patient(id):
    db.session.delete(Patient.query.get_or_404(id))
    db.session.commit()
    return redirect(url_for('patients'))


# ---------------- DOCTORS ----------------
@app.route('/doctors')
def doctors():
    return render_template('doctors.html', doctors=Doctor.query.all())


@app.route('/add_doctor', methods=['GET', 'POST'])
def add_doctor():
    if request.method == 'POST':
        db.session.add(Doctor(
            name=request.form['name'],
            specialization=request.form['specialization'],
            experience=request.form['experience']
        ))
        db.session.commit()
        return redirect(url_for('doctors'))

    return render_template('add_doctor.html')


@app.route('/delete_doctor/<int:id>')
def delete_doctor(id):
    db.session.delete(Doctor.query.get_or_404(id))
    db.session.commit()
    return redirect(url_for('doctors'))


# ---------------- APPOINTMENTS ----------------
@app.route('/appointments')
def appointments():
    return render_template(
        'appointments.html',
        appointments=Appointment.query.all()
    )


@app.route('/add_appointment', methods=['GET', 'POST'])
def add_appointment():
    if request.method == 'POST':
        db.session.add(Appointment(
            patient_id=request.form['patient_id'],
            doctor_id=request.form['doctor_id'],
            appointment_date=request.form['appointment_date']
        ))
        db.session.commit()
        return redirect(url_for('appointments'))

    return render_template(
        'add_appointment.html',
        patients=Patient.query.all(),
        doctors=Doctor.query.all()
    )


# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)