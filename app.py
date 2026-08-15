from flask import Flask, render_template, request, redirect, abort, session, jsonify
from models import db
from models.user import User
from models.donation import Donation
from models.collection import Collection
from sqlalchemy import func, desc
import re
import random
import smtplib
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# 🔐 SECRET KEY
app.secret_key = os.getenv("SECRET_KEY")

# -------------------------------------------------
# DATABASE CONFIG
# -------------------------------------------------

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# -------------------------------------------------
# INITIAL SETUP
# -------------------------------------------------
with app.app_context():
    db.create_all()

    if not User.query.filter_by(role="ngo").first():
        ngo = User(
            name="Helping Hands NGO",
            role="ngo",
            location="Mumbai",
            verified=True
        )
        db.session.add(ngo)
        db.session.commit()





# -------------------------------------------------
# HOME
# -------------------------------------------------
@app.route('/')
def index():

    food = Donation.query.filter_by(
        item_type="food",
        status="accepted"
    ).count()

    clothes = Donation.query.filter_by(
        item_type="clothes",
        status="accepted"
    ).count()

    return render_template(
        "index.html",
        meals=food * 5,
        clothes=clothes,
        total=food + clothes
    )

# -------------------------------------------------
# CONTACT PAGE
# -------------------------------------------------
@app.route('/contact', methods=['GET', 'POST'])
def contact():

    if request.method == 'POST':
        name = request.form.get("name")
        email = request.form.get("email")
        subject = request.form.get("subject")
        message = request.form.get("message")

        print("CONTACT FORM:")
        print(name, email, subject, message)

        return redirect('/contact')

    return render_template("contact.html")

# -------------------------------------------------
# DONATE
# -------------------------------------------------
@app.route('/donate', methods=['GET', 'POST'])
def donate():

  

    if request.method == 'POST':

        # 🔥 Reset verification after one successful submit
        session["user_verified"] = False

        if not request.form.get("terms"):
            abort(400, "Terms must be accepted")

        name = request.form.get("name")
        phone = request.form.get("phone")
        location = request.form.get("location")
        latitude = request.form.get("latitude")
        longitude = request.form.get("longitude")
        assigned_ngo = request.form.get("assigned_ngo")

        if not name or len(name) < 3:
            abort(400, "Invalid name")

        if not re.fullmatch(r"[6-9][0-9]{9}", phone):
            abort(400, "Invalid phone number")

        if not location:
            abort(400, "Location is required")

        item_type = request.form['item_type']
        condition = request.form['condition']

        expiry_map = {
            "fresh": 10,
            "medium": 5,
            "low": 2,
            "contaminated": 0
        }

        expiry_hours = expiry_map.get(condition)

        if item_type == "food":
            route_type = "recycle" if condition == "contaminated" else "ngo"
        elif item_type == "clothes":
            if condition == "wearable":
                route_type = "ngo"
            elif condition == "repairable":
                route_type = "tailor"
            else:
                route_type = "recycle"

        try:
            latitude = float(latitude) if latitude else None
            longitude = float(longitude) if longitude else None
        except:
            latitude = None
            longitude = None

        donation = Donation(
            name=name,
            item_type=item_type,
            quantity=int(request.form['quantity']),
            condition=condition,
            route_type=route_type,
            expiry_hours=expiry_hours,
            location=location,
            latitude=latitude,
            longitude=longitude,
            phone=phone,
            status="available",
            assigned_ngo=assigned_ngo
        )

        db.session.add(donation)
        db.session.commit()

        return redirect("/")

    return render_template("donate.html")

# -------------------------------------------------
# NGO DASHBOARD
# -------------------------------------------------
@app.route('/ngo')
def ngo():

    donations = Donation.query.filter(
        Donation.status.in_(["available"])
    ).order_by(
        Donation.expiry_hours.asc().nullslast()
    ).all()

    return render_template("ngo.html", donations=donations)

# -------------------------------------------------
# ACCEPT / REJECT / FLOW
# -------------------------------------------------
@app.route('/accept/<int:id>')
def accept(id):
    d = Donation.query.get_or_404(id)

    if d.status != "available":
        return redirect('/ngo')

    d.status = "accepted"

    c = Collection(
        donation_id=id,
        ngo_name=d.assigned_ngo,
        status="assigned"
    )

    db.session.add(c)
    db.session.commit()

    return redirect('/ngo')


@app.route('/reject/<int:id>')
def reject(id):
    d = Donation.query.get_or_404(id)

    if d.status != "available":
        return redirect('/ngo')

    d.status = "rejected"
    db.session.commit()

    return redirect('/ngo')


@app.route('/pickup/<int:id>')
def pickup(id):
    d = Donation.query.get_or_404(id)

    if d.status != "accepted":
        return redirect('/ngo')

    d.status = "picked_up"
    db.session.commit()

    return redirect('/ngo')


@app.route('/delivered/<int:id>')
def delivered(id):
    d = Donation.query.get_or_404(id)

    if d.status != "picked_up":
        return redirect('/ngo')

    d.status = "delivered"
    db.session.commit()

    return redirect('/ngo')

# -------------------------------------------------
# TRACK
# -------------------------------------------------
@app.route("/track/<int:id>")
def track(id):
    donation = Donation.query.get_or_404(id)
    return render_template("track.html", donation=donation)

# -------------------------------------------------
# ANALYTICS
# -------------------------------------------------
@app.route('/analytics')
def analytics():

    food = Donation.query.filter_by(item_type="food", status="accepted").count()
    clothes = Donation.query.filter_by(item_type="clothes", status="accepted").count()

    total = Donation.query.count()
    meals = food * 5

    ngos = db.session.query(Collection.ngo_name).distinct().count()
    quantity = db.session.query(func.sum(Donation.quantity)).scalar() or 0

    top_ngos_query = db.session.query(
        Collection.ngo_name,
        func.count(Collection.id)
    ).group_by(Collection.ngo_name).order_by(desc(func.count(Collection.id))).limit(5).all()

    top_ngos = [{"name": n, "count": c} for n, c in top_ngos_query]

    status_data = db.session.query(Donation.status, func.count()).group_by(Donation.status).all()
    type_data = db.session.query(Donation.item_type, func.count()).group_by(Donation.item_type).all()
    condition_data = db.session.query(Donation.condition, func.count()).group_by(Donation.condition).all()

    return render_template(
        "analytics.html",
        food=food,
        clothes=clothes,
        total=total,
        meals=meals,
        ngos=ngos,
        quantity=quantity,
        top_ngos=top_ngos,
        status_labels=[s[0] for s in status_data],
        status_counts=[s[1] for s in status_data],
        type_labels=[t[0] for t in type_data],
        type_counts=[t[1] for t in type_data],
        condition_labels=[c[0] for c in condition_data],
        condition_counts=[c[1] for c in condition_data]
    )

# -------------------------------------------------
# ADMIN
# -------------------------------------------------
@app.route('/admin')
def admin():

    donations = Donation.query.order_by(Donation.id.desc()).all()

    total = Donation.query.count()
    pending = Donation.query.filter_by(status="available").count()
    delivered = Donation.query.filter_by(status="delivered").count()
    rejected = Donation.query.filter_by(status="rejected").count()

    food = Donation.query.filter_by(item_type="food").count()
    clothes = Donation.query.filter_by(item_type="clothes").count()

    meals = food * 5
    ngos = db.session.query(Collection.ngo_name).distinct().count()
    quantity = db.session.query(func.sum(Donation.quantity)).scalar() or 0

    top_ngos_query = db.session.query(
        Collection.ngo_name,
        func.count(Collection.id)
    ).group_by(Collection.ngo_name).order_by(desc(func.count(Collection.id))).limit(5).all()

    top_ngos = [{"name": n, "count": c} for n, c in top_ngos_query]

    users = User.query.all()

    status_data = db.session.query(Donation.status, func.count()).group_by(Donation.status).all()
    type_data = db.session.query(Donation.item_type, func.count()).group_by(Donation.item_type).all()
    condition_data = db.session.query(Donation.condition, func.count()).group_by(Donation.condition).all()

    return render_template(
        "admin.html",
        donations=donations,
        total=total,
        pending=pending,
        delivered=delivered,
        rejected=rejected,
        ngos=ngos,
        food=food,
        clothes=clothes,
        meals=meals,
        quantity=quantity,
        top_ngos=top_ngos,
        users=users,
        status_labels=[s[0] for s in status_data],
        status_counts=[s[1] for s in status_data],
        type_labels=[t[0] for t in type_data],
        type_counts=[t[1] for t in type_data],
        condition_labels=[c[0] for c in condition_data],
        condition_counts=[c[1] for c in condition_data]
    )

# -------------------------------------------------
# RUN
# -------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)