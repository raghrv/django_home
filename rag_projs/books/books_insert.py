from models import Publisher

p1 = Publisher(name='raghav', address='kk', city='Ban', state='KA', country='India', website='www.google.com')
p1.save()


a = """   "name" varchar(30) NOT NULL,
    "address" varchar(50) NOT NULL,
    "city" varchar(30) NOT NULL,
    "state" varchar(50) NOT NULL,
    "country" varchar(30) NOT NULL,
    "website" varchar(200) NOT NULL
"""
