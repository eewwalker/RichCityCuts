"""Initial data."""


from app import db
from models import Neighborhood, Stop, User


db.drop_all()
db.create_all()


#######################################
# add neighborhoods
all = Neighborhood(code='all', name='All neighborhoods')
point = Neighborhood(code='point', name='Point Richmond')
marina = Neighborhood(code='marina', name='Marina Bay')
hills = Neighborhood(code='hills', name='Richmond Hills')
pablo = Neighborhood(code='pablo', name='Point San Pablo')
northeast = Neighborhood(code='northeast', name='North and East')
north = Neighborhood(code='north', name='North Richmond')
annex = Neighborhood(code='annex', name='Richmond Annex')

db.session.add_all([all, point, marina, hills, pablo, northeast, north, annex])
db.session.commit()


#######################################
# add stops

s1 = Stop(
    name="Fairy Houses",
    description='Take a hike up Washington Avenue in Point Richmond to see '
    'fairy homes.',
    address="300 Washington Avenue",
    hood_code='point',
    url='https://52bayareadaytrips.medium.com/the-fairy-houses-of-point'
    '-richmond-teaser-alert-34-pictures-28400a0123d5',
    image_url='https://miro.medium.com/v2/resize:fit:1400/format:webp/'
    '1*Jmk5VhFH-NQLJElkzNdy3g.jpeg'
)

s2 = Stop(
    name='Marina Bay',
    description='Beautiful walk along the bay, great for bird watching and views'
    ' of the bay',
    address='Marina Bay Pkwy & Peninsula Dr, 79 Harbor View Dr',
    hood_code='marina',
    url='https://www.nps.gov/places/richmond-marina-bay-trail.htm',
    image_url='https://dynamic-media-cdn.tripadvisor.com/media/photo-o/0e/'
    'bc/aa/de/meeker-slough-at-high.jpg?w=2000&h=-1&s=1',
)

s3 = Stop(
    name='Good Hot Sauna',
    description='Saunas for private rental and a beach for cold plunging at'
    ' Point San Pablo ',
    address='1950 Stenmark Dr',
    hood_code='pablo',
    url='https://www.kalw.org/arts-culture/2023-02-08/deconstructed-bathhouse'
    '-good-hot-brings-saunas-to-richmonds-coastline',
    image_url='https://s.hdnux.com/photos/01/31/31/35/23435084/3/rawImage.jpg'
)

db.session.add_all([s1, s2, s3])
db.session.commit()


#######################################
# add users

ua = User.register(
    username="admin",
    first_name="Addie",
    last_name="MacAdmin",
    description="I am the very model of the modern model administrator.",
    email="admin@test.com",
    password="secret",
    admin=True,
)

u1 = User.register(
    username="test",
    first_name="Testy",
    last_name="MacTest",
    description="I am the ultimate representative user.",
    email="test@test.com",
    password="secret",
)

db.session.add_all([u1])
db.session.commit()


#######################################
# add likes

u1.liked_stops.append(s1)
u1.liked_stops.append(s2)
ua.liked_stops.append(s1)
db.session.commit()


#######################################
# stop maps

s1.save_map()
s2.save_map()
s3.save_map()

db.session.commit()
