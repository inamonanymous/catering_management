from app.models import db

class BlockedDates(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.Date, unique=True, nullable=False)

    @classmethod
    def block_date(cls, date):
        try:
            blocked_date = cls(date=date)
            db.session.add(blocked_date)
            db.session.commit()
            return blocked_date
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Error blocking date: {e}")

    @classmethod
    def get_blocked_dates(cls):
        return [blocked.date.strftime('%Y-%m-%d') for blocked in cls.query.all()]
