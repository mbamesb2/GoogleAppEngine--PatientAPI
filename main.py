
import webapp2



app = webapp2.WSGIApplication([
    ('/patient', 'patient.patientHandler')
], debug=True)

app.router.add(webapp2.Route(r'/patient/<id:[0-9]+><:/?>', 'patient.patientHandler'))
app.router.add(webapp2.Route(r'/patient/search', 'patient.patientSearch'))
app.router.add(webapp2.Route(r'/patient/delete/<id:[0-9]+><:/?>', 'patient.patientDelete'))
app.router.add(webapp2.Route(r'/patient/update', 'patient.patientUpdate'))
app.router.add(webapp2.Route(r'/doctor', 'doctor.doctorHandler'))
app.router.add(webapp2.Route(r'/doctor/<id:[0-9]+><:/?>', 'doctor.doctorHandler'))
app.router.add(webapp2.Route(r'/doctor/delete/<id:[0-9]+><:/?>', 'doctor.doctorDelete'))