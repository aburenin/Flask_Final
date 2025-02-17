from Models import db
from config import qa_list

class Question(db.Model):
    __tablename__ = 'question'

    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(100), nullable=False, unique=True)
    answer = db.Column(db.Text(1000), nullable=False)

    def __init__(self, id, question, answer):
        self.id = id
        self.question = question
        self.answer = answer

def CHECK_QUESTION_DB(app):
    with app.app_context():
        for id, question, answer in qa_list:
            exist_qa = Question.query.filter_by(id=id).first()

            if exist_qa:
                change = False
                if exist_qa.question != question:
                    change = True
                    exist_qa.question = question
                if exist_qa.answer != answer:
                    change = True
                    exist_qa.answer = answer

                if change:
                    db.session.commit()
            else:
                question = Question(id=id, question=question, answer=answer)
                try:
                    db.session.add(question)
                    db.session.commit()
                except Exception as e:
                    db.session.rollback()
                    print(f"Ошибка при добавлении нового пакета: {e}")