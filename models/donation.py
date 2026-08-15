from . import db


class Donation(db.Model):

    __tablename__ = "donation"

    # =========================
    # PRIMARY KEY
    # =========================
    id = db.Column(
        db.Integer,
        primary_key=True
    )

    # =========================
    # BASIC DONATION DETAILS
    # =========================
    item_type = db.Column(
        db.String(20),
        nullable=False
    )

    quantity = db.Column(
        db.Integer,
        nullable=False
    )

    condition = db.Column(
        db.String(20),
        nullable=False
    )

    # =========================
    # AUTO ROUTING
    # =========================
    route_type = db.Column(
        db.String(20),
        nullable=False,
        default="ngo"
    )

    # =========================
    # FOOD SAFETY
    # =========================
    expiry_hours = db.Column(
        db.Integer,
        nullable=True
    )

    # =========================
    # LOCATION DETAILS
    # =========================
    location = db.Column(
        db.String(255),
        nullable=True
    )

    latitude = db.Column(
        db.Float,
        nullable=True
    )

    longitude = db.Column(
        db.Float,
        nullable=True
    )

    # =========================
    # CONTACT
    # =========================
    name = db.Column(
        db.String(100),
        nullable=False
    )

    phone = db.Column(
        db.String(15),
        nullable=False
    )

    email = db.Column(
        db.String(100),
        nullable=True
    )

    # =========================
    # STATUS TRACKING
    # =========================
    status = db.Column(
        db.String(20),
        default="available",
        nullable=False
    )

    # NGO chosen by user
    assigned_ngo = db.Column(
        db.String(100),
        nullable=True
    )

    # =========================
    # PICKUP TIME
    # =========================
    pickup_time = db.Column(
        db.String(100),
        nullable=True
    )

    # =========================
    # CREATED TIME
    # =========================
    created_at = db.Column(
        db.DateTime,
        server_default=db.func.current_timestamp()
    )



