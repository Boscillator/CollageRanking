from mongoengine import *

class Variable(Document):
    _id = IntField(required=True)
    name = StringField(required=True)
    variable_name = StringField(required=True)
    category = StringField(required=True)
    developer_name = StringField(required=True)
    source = StringField(required=True)
    consumer = BooleanField(required=True)

    meta = {
        'allow_inheritance': True
    }

class NumericVariable(Variable):
    
    def __repr__(self):
        return f'<NumericVariable:{self.variable_name}>'

class FactorVariable(Variable):
    factors = MapField(StringField(), required=True)

    def __repr__(self):
        return f'<FactorVariable:{self.variable_name}>'