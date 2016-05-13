import webapp2
from google.appengine.ext import ndb
import db_defs
import json

# This function should display data by ID, or display all the data in Patient if no ID is specified
class doctorHandler(webapp2.RequestHandler):
    def get(self, **kwargs):
        if 'application/json' not in self.request.accept:
            self.response.status = 406
            self.response.status_message = "API only supports application/json"
        if 'id' in kwargs:
            out = ndb.Key(db_defs.Doctor, int(kwargs['id'])).get().to_dict
            self.response.write(json.dumps(out))
        else:
            q = db_defs.Doctor.query()
            keys = q.fetch(keys_only=True)
            results = { 'keys' : [x.id() for x in keys]}
            self.response.write(json.dumps(results))
        
    def post(self):
        if 'application/json' not in self.request.accept:
            self.response.status = 406
            self.response.status_message = "API only supports application/json"
            return
        
        new_doctor = db_defs.Doctor()
        specialty = []
        certifications = []
        firstName = self.request.get('firstName', default_value = None)
        lastName = self.request.get('lastName', default_value = None)
        specialty = (self.request.get_all('specialty', default_value = None))
        certifications = (self.request.get_all('certifications', default_value = None))
        employer = self.request.get('employer', default_value = None)
        contact = self.request.get('contact', default_value = None)
        
        if firstName:
            new_doctor.firstName = firstName
        else:
            self.response.status = 400
            self.response.status_message = "Invalid request. firstName is required"
            return
        if lastName:
            new_doctor.lastName = lastName
        else:
            self.response.status = 400
            self.response.status_message = "Invalid request. lastName is required"
            return
        if len(specialty) > 0:
            new_doctor.specialty = specialty
        if len(certifications) > 0:
            new_doctor.certifications = certifications
        if employer:
            new_doctor.employer = employer
        else:
            self.response.status = 400
            self.response.status_message = "Invalid request. employer is required"
            return
        if contact:
            new_doctor.contact = contact
        else:
            self.response.status = 400
            self.response.status_message = "Invalid request. contact is required"
            return
        
        key = new_doctor.put()
        out = new_doctor.to_dict()
        self.response.write(json.dumps(out))
        
        return
            
class doctorDelete(webapp2.RequestHandler):
    def delete(self, **kwargs):
        if 'application/json' not in self.request.accept:
            self.response.status = 406
            self.response.status_message = "API only supports application/json"
        if 'id' in kwargs:
            out = ndb.Key(db_defs.Doctor, int(kwargs['id'])).get()
            test = ndb.Key(db_defs.Doctor, int(kwargs['id']))
            if out is not None:
                out.key.delete()
            else:
                self.response.status = 404
                self.response.status_message = "Error: No object with that key was found"
                return
        else:
            self.response.status = 400
            self.response.status_message = "Error: No id was specified"    
        

        