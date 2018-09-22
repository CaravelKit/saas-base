from flask import render_template, redirect, request, url_for, flash, jsonify, current_app

from . import main_component

@main_component.route('/main', methods=['GET']) # Change to root '/' or anything you want. Currently root '/' is for dashboard.
def main_page():
    return render_template('index.html', company_name=current_app.config.get('COMPANY_NAME'))