
class Content(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    form = db.Column(db.String(50))
    date = db.Column(db.Date)
    rating = db.Column(db.Integer)
    notes = db.Column(db.String(200))
    link = db.Column(db.String(200))