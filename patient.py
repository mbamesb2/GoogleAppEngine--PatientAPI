import webapp2
from google.appengine.ext import ndb
import db_defs
import json

# This function should display data by ID, or display all the data in Patient if no ID is specified
class patientHandler(webapp2.RequestHandler):
    def get(self, **kwargs):
        if 'application/json' not in self.request.accept:
            self.response.status = 406
            self.response.status_message = "API only supports application/json"
            return
        else:
            if 'id' in kwargs:
                out = ndb.Key(db_defs.Patient, int(kwargs['id'])).get().to_dict()
                self.response.write(json.dumps(out))
                return
            
            else:
                q = db_defs.Patient.query()
                keys = q.fetch(keys_only=True)
                results = { 'keys' : [x.id() for x in keys]}
                self.response.write(json.dumps(results))
                return

    def post(self):
        self.response.headers.add_header('Access-Control-Allow-Origin', '*')
        self.response.headers['Content-Type'] = 'application/json'
        
        if 'application/json' not in self.request.accept:
            self.response.status = 406
            self.response.status_message = "API only supports application/json"
            return
        else:
            new_patient = db_defs.Patient()
            diseaseHistory = []
            medications = []
            allergies = []
            doctors = []
            
            firstName = self.request.get('firstName', default_value = None)
            lastName = self.request.get('lastName', default_value = None)
            age = self.request.get('age', default_value = None)
            gender = self.request.get('gender', default_value = None)
            checkedIn = self.request.get('checkedIn', default_value = None)
            roomNo = self.request.get('roomNo', default_value = None)
            condition = self.request.get('condition', default_value = None)
            lastVisit = self.request.get('lastVisit', default_value = None)
            
            
            if firstName is not None:
                new_patient.firstName = firstName
            else:
                self.response.status = 400
                self.response.status_message = "Invalid request. firstName is required"
                return
            
            if lastName is not None:
                new_patient.lastName = lastName
            else:
                self.response.status = 400
                self.response.status_message = "Invalid request. lastName is required"    
                return
            
            if age is not None:
                new_patient.age = int(age)
            else:
                self.response.status = 400
                self.response.status_message = "Invalid request. Age is required"
                return
            
            if gender is not None:
                new_patient.gender = gender
            else:
                self.response.status = 400
                self.response.status_message = "Invalid request. Gender is required"
                return
            
            if checkedIn is not None:
                if (checkedIn == "True") or (checkedIn == "true") or (checkedIn =="yes") or (checkedIn =="Yes"):
                    new_patient.checkedIn = True
                    
                elif(checkedIn == "False") or (checkedIn == "false") or (checkedIn == "no") or (checkedIn == "No"):
                    new_patient.checkedIn = False
                
                else:
                    self.response.status=400
                    self.response.status_message = "Invalid request. True or False is required for checkedIn"
                    return
            else:
                self.response.status = 400
                self.response.status_message = "Invalid request. CheckIn is required"
                return
                
            if roomNo:
                new_patient.roomNo = int(roomNo)
            if condition:
                new_patient.condition = condition
            if lastVisit:
                new_patient.lastVisit = lastVisit
                
            if self.request.get_all('diseaseHistory', default_value = None):    
                diseaseHistory = (self.request.get_all('diseaseHistory', default_value = None))
                if len(diseaseHistory) is not 0:
                    new_patient.diseaseHistory = diseaseHistory
                            
            if self.request.get_all('medications', default_value = None):        
                medications = (self.request.get_all('medications', default_value = None))
                if len(medications) is not 0:
                    new_patient.medications = medications
                        
            if self.request.get_all('allergies', default_value = None):
                allergies = (self.request.get_all('allergies', default_value = None))
                if len(allergies) is not 0:
                    new_patient.allergies = allergies
                            
            if self.request.get_all('doctors', default_value = None):
                doctors = (self.request.get_all('doctors', default_value = None))
                
                
            key = new_patient.put()
            out = new_patient.to_dict()
            self.response.write(json.dumps(out))
            return
                
# This function should allow the user to search a patient by last name       
class patientSearch(webapp2.RequestHandler):
    def post(self):
        if 'application/json' not in self.request.accept:
            self.response.status = 406
            self.response.status_message = "API only supports application/json"
            return
        else:
            lastName = self.request.get('lastName', default_value=None)
            q = db_defs.Patient.query()
            if lastName:
                q = q.filter(db_defs.Patient.lastName == lastName)
                result = q.get()
                if result is not None:
                    done = result.to_dict()
                    self.response.write(json.dumps(done))
                    return
                else:
                    self.response.status = 404
                    self.response.status_message ="No object was found with specified lastName "
                    return
            else:
                self.response.status = 400
                self.response.status_message = "Error: No lastName specified "
                return
            
    # This function allows the user to delete a patient by id
class patientDelete(webapp2.RequestHandler):
    def delete(self, **kwargs):
        if 'application/json' not in self.request.accept:
            self.response.status = 406
            self.response.status_message = "API only supports application/json"
        else:
            if 'id' in kwargs:
                out = ndb.Key(db_defs.Patient, int(kwargs['id'])).get()
                if out is not None:
                    out.key.delete()
                else:
                    self.response.status = 404
                    self.response.status_message = "Error: No object with that key was found"
                    return
            else:
                self.response.status = 400
                self.response.status_message = "Error: No id was specified"
                return

class patientUpdate(webapp2.RequestHandler):
    def put(self, **kwargs):
        if 'application/json' not in self.request.accept:
            self.response.status = 406
            self.response.status_message = "API only supports application/json"
            return
        
        if self.request.get('key'):
            patUpdate = ndb.Key(db_defs.Patient, int(self.request.get('key'))).get()
            if patUpdate is None:
                self.response.status = 404
                self.response.status_message = "Error: No object found"
                return
            else:
                diseaseHistory = []
                medications = []
                allergies = []
                doctors = []
                
                firstName = self.request.get('firstName', default_value = None)
                if firstName:
                    patUpdate.firstName = firstName
                lastName = self.request.get('lastName', default_value = None)
                if lastName:
                    patUpdate.lastName = lastName
                age = self.request.get('age', default_value = None)
                if age:
                    patUpdate.age = int(age)
                
                gender = self.request.get('gender', default_value = None)
                if gender:
                    patUpdate.gender = gender
                    
                checkedIn = self.request.get('checkedIn', default_value = None)
                if checkedIn:
                    if (checkedIn == "True") or (checkedIn == "true") or (checkedIn =="yes") or (checkedIn =="Yes"):
                        patUpdate.checkedIn = True
                    
                    elif(checkedIn == "False") or (checkedIn == "false") or (checkedIn == "no") or (checkedIn == "No"):
                        patUpdate.checkedIn = False
                
                    else:
                        self.response.status=400
                        self.response.status_message = "Invalid request. True or False is required for checkedIn"
                        return
                
                roomNo = self.request.get('roomNo', default_value = None)
                if roomNo:
                    patUpdate.roomNo = int(roomNo)
                condition = self.request.get('condition', default_value = None)
                if condition:
                    patUpdate.condition = condition   
                lastVisit = self.request.get('lastVisit', default_value = None)
                if lastVisit:
                    patUpdate.lastVisit = lastVisit
                    
                if self.request.get_all('diseaseHistory', default_value = None):    
                    diseaseHistory = (self.request.get_all('diseaseHistory', default_value = None))
                    if len(diseaseHistory) is not 0:
                        patUpdate.diseaseHistory = diseaseHistory
                        
                if self.request.get_all('medications', default_value = None):        
                    medications = (self.request.get_all('medications', default_value = None))
                    if len(medications) is not 0:
                        patUpdate.medications = medications
                        
                if self.request.get_all('allergies', default_value = None):
                    allergies = (self.request.get_all('allergies', default_value = None))
                    if len(allergies) is not 0:
                        patUpdate.allergies = allergies
                        
                if self.request.get_all('doctors', default_value = None):
                    doctors = (self.request.get_all('doctors', default_value = None))
                    if len(doctors) is not 0:
                        for each in doctors:
                            results = ndb.Key(db_defs.Doctor, int(each))
                            if not results:
                                self.response.status = 404
                                self.response.status_message = "Doctor not found"
                                return
                            elif results not in patUpdate.doctors:
                                patUpdate.doctors.append(results)
                                
                        
                        
                key = patUpdate.put()
                out = patUpdate.to_dict()
                self.response.write(json.dumps(out))
                return  
        else:
            self.response.status = 400
            self.response.status_message = "Error: Key is required to update"
            return