from flask import Blueprint, render_template, request, redirect, flash, url_for

from app.extensions import db
from app.models.user import User

class SearchHistory():
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    query = db.Column(db.String(100), nullable=False)
    searched_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())