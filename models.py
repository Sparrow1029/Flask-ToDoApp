from datetime import datetime
from app import db

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(528))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    due_date = db.Column(db.DateTime, index=True)
    completed = db.Column(db.Boolean, default=False)
    completed_date = db.Column(db.DateTime, index=True)

    # def is_recently_deleted():
    #     return self.recently_deleted

    @classmethod
    def clear_completed(cls):
        cls.query.filter_by(completed = True or 1).delete()
        db.session.commit()

    def __repr__(self):
        return '<Task: {}, created: {}, due: {}>'.format(self.body,
                                                         self.timestamp,
                                                         self.due_date)
