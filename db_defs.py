from google.appengine.ext import ndb
import json

class Model(ndb.Model):
    def to_dict(self):
        d = super(Model, self).to_dict()
        d['key'] = self.key.id()
        return d

class Patient(Model):
    firstName=ndb.StringProperty(required=True)
    lastName=ndb.StringProperty(required=True)
    age=ndb.IntegerProperty(required=True)
    gender=ndb.StringProperty(required=True)
    checkedIn=ndb.BooleanProperty(required=True)
    roomNo=ndb.IntegerProperty()
    condition=ndb.StringProperty()
    lastVisit=ndb.DateTimeProperty()
    diseaseHistory=ndb.StringProperty(repeated=True)
    medications=ndb.StringProperty(repeated=True)
    allergies=ndb.StringProperty(repeated=True)
    doctors=ndb.KeyProperty(repeated=True)
    
    def to_dict(self):
        d = super(Patient,self).to_dict()
        d['doctors'] = [n.id() for n in d['doctors']]
        return d
    
    
    
class Doctor(Model):
    firstName = ndb.StringProperty(required=True)
    lastName = ndb.StringProperty(required=True)
    specialty=ndb.StringProperty(repeated=True)
    certifications=ndb.StringProperty(repeated=True)
    employer=ndb.StringProperty(required=True)
    contact=ndb.StringProperty(required=True)
    


        
    