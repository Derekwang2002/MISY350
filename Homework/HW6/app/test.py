from . import db
from app.models import Suppliers

def test():
    fstsid = Suppliers.query.get(1).SupplierID
    print('Successful retireved' + str(fstsid))

test()