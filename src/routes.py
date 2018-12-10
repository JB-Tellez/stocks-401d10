from flask import render_template, abort, redirect, url_for, request
from json import JSONDecodeError
from .models import db, Company
import requests as req
from . import app
import json


@app.route('/')
def home():
    """
    """
    return render_template('home.html')


@app.route('/search', methods=['GET', 'POST'])
def company_search():
    """
    """
    if request.method == 'POST':
        res = req.get(f'https://api.iextrading.com/1.0/stock/{ request.form.get("symbol") }/company')

        try:
            data = json.loads(res.text)
            company = Company(
                symbol=data['symbol'],
                companyName=data['companyName'],
                exchange=data['exchange'],
                industry=data['industry'],
                website=data['website'],
                description=data['description'],
                CEO=data['CEO'],
                issueType=data['issueType'],
                sector=data['sector'],
            )

            # NOTE: THIS WILL THROW A DUPE KEY ERROR IF WE ADD THE SAME STOCK AGAIN
            # Handle this with an additional try/except
            db.session.add(company)
            db.session.commit()

            return redirect(url_for('.portfolio_detail'))
        except JSONDecodeError:
            abort(404)

    return render_template('portfolio/search.html')


@app.route('/portfolio')
def portfolio_detail():
    """
    """
    return render_template('portfolio/portfolio.html')
