import flask
import os
from flask import request
from flask.views import MethodView
from sqlalchemy import Column, DateTime, Integer, String, create_engine, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker

app = flask.Flask('app')
PG_DSN = os.getenv('PG_DSN')
engine = create_engine(PG_DSN)
Base = declarative_base()
Session = sessionmaker(bind=engine)


class UserModel(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True)
    user_name = Column(String(100), nullable=False, unique=True)


Base.metadata.create_all(engine)


class UserView(MethodView):
    def get(self):
        pass

    def post(self):
        new_user_data = request.json
        with Session() as session:
            new_user = UserModel(user_name=new_user_data['user_name'])
            session.add(new_user)
            return flask.jsonify({
                'id': new_user.user_id
            })


class AdModel(Base):
    __tablename__ = 'ads'
    ad_id = Column(Integer, primary_key=True)
    ad_title = Column(String(100), nullable=False, unique=True)
    ad_description = Column(String(500), nullable=False, unique=True)
    ad_date = Column(DateTime(timezone=True), server_default=func.now())

    ad_owner = Column(Integer, ForeignKey('users.user_id'))
    user = relationship('UserModel')


class AdView(MethodView):

    def get(self):
        pass

    def post(self):
        new_ad_data = request.json
        with Session() as session:
            new_ad = UserModel(user_name=new_ad_data['title'])
            session.add(new_ad)
            return flask.jsonify({
                'ad_id': new_ad.ad_id
            })

    def delete(self):
        ad = AdModel.query.get(AdModel.ad_id)
        with Session() as session:
            session.delete(ad)


user_view = UserView.as_view('user_api')
ad_view = AdView.as_view('ad_api')


app.add_url_rule(
    '/user/',
    view_func=UserView.as_view('create_user'),
    methods=['GET', 'POST'])

app.add_url_rule(
    '/ads/',
    view_func=ad_view,
    methods=['GET', 'POST', 'DELETE'])

