from config import pakets

from Models import db

class Preise(db.Model):
    __tablename__ = 'preise'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    price = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)

    def __init__(self, name, price, description):
        self.name = name
        self.price = price
        self.description = description

    @classmethod
    def check_db(cls, app):
        with app.app_context():
            for name, price, description in pakets:
                exist_paket = Preise.query.filter_by(name=name).first()

                if exist_paket:
                    change = False
                    if exist_paket.price != price:
                        change = True
                        exist_paket.price = price
                    if exist_paket.description != description:
                        change = True
                        exist_paket.description = description

                    if change:
                        db.session.commit()
                else:
                    # Создаем новый пакет
                    new_paket = Preise(name=name, price=price, description=description)
                    Preise.new_paket(new_paket, app)

    @classmethod
    def new_paket(cls, new_paket, app):
        with app.app_context():
            try:
                db.session.add(new_paket)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                print(f"Ошибка при добавлении нового пакета: {e}")