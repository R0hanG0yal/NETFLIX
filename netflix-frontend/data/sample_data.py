"""
Sample data module for the Netflix OTT Platform.
Contains all entities from the ER diagram with realistic sample data.
"""

import datetime
import random

# ============================================================
# ENTITY: SUBS_PLAN
# Attributes: PLAN_ID, PLAN_NAME, PRICE, DURATION_MON, MAX_SCREEN, VIDEO_QUAL
# ============================================================
SUBS_PLANS = [
    {"plan_id": 1, "plan_name": "Mobile", "price": 149, "duration_mon": 1, "max_screen": 1, "video_qual": "480p"},
    {"plan_id": 2, "plan_name": "Basic", "price": 199, "duration_mon": 1, "max_screen": 1, "video_qual": "720p"},
    {"plan_id": 3, "plan_name": "Standard", "price": 499, "duration_mon": 1, "max_screen": 2, "video_qual": "1080p"},
    {"plan_id": 4, "plan_name": "Premium", "price": 649, "duration_mon": 1, "max_screen": 4, "video_qual": "4K+HDR"},
    {"plan_id": 5, "plan_name": "Student", "price": 149, "duration_mon": 6, "max_screen": 1, "video_qual": "1080p"},
    {"plan_id": 6, "plan_name": "Family Annual", "price": 4999, "duration_mon": 12, "max_screen": 5, "video_qual": "4K+HDR"},
]

# ============================================================
# ENTITY: USER
# Attributes: USER_ID, NAME, EMAIL, PASSWORD, PHONE, REG_DATE
# ============================================================
USERS = [
    {"user_id": 1, "name": "Aarav Sharma", "email": "aarav.sharma@email.com", "password": "hashed_pw1", "phone": "9876543210", "reg_date": "2023-01-15"},
    {"user_id": 2, "name": "Priya Patel", "email": "priya.patel@email.com", "password": "hashed_pw2", "phone": "9876543211", "reg_date": "2023-02-20"},
    {"user_id": 3, "name": "Rohan Mehta", "email": "rohan.mehta@email.com", "password": "hashed_pw3", "phone": "9876543212", "reg_date": "2023-03-10"},
    {"user_id": 4, "name": "Sneha Gupta", "email": "sneha.gupta@email.com", "password": "hashed_pw4", "phone": "9876543213", "reg_date": "2023-04-05"},
    {"user_id": 5, "name": "Vikram Singh", "email": "vikram.singh@email.com", "password": "hashed_pw5", "phone": "9876543214", "reg_date": "2023-05-18"},
    {"user_id": 6, "name": "Ananya Reddy", "email": "ananya.reddy@email.com", "password": "hashed_pw6", "phone": "9876543215", "reg_date": "2023-06-22"},
    {"user_id": 7, "name": "Karan Joshi", "email": "karan.joshi@email.com", "password": "hashed_pw7", "phone": "9876543216", "reg_date": "2023-07-30"},
    {"user_id": 8, "name": "Divya Nair", "email": "divya.nair@email.com", "password": "hashed_pw8", "phone": "9876543217", "reg_date": "2023-08-14"},
    {"user_id": 9, "name": "Arjun Kapoor", "email": "arjun.kapoor@email.com", "password": "hashed_pw9", "phone": "9876543218", "reg_date": "2024-01-05"},
    {"user_id": 10, "name": "Meera Iyer", "email": "meera.iyer@email.com", "password": "hashed_pw10", "phone": "9876543219", "reg_date": "2024-02-28"},
]

# ============================================================
# ENTITY: PROFILES
# Attributes: PROFILE_ID, USER_ID, PROFILE_NAME, PROFILE_TYPE
# ============================================================
PROFILES = [
    {"profile_id": 1, "user_id": 1, "profile_name": "Aarav", "profile_type": "Adult"},
    {"profile_id": 2, "user_id": 1, "profile_name": "Kids Zone", "profile_type": "Kids"},
    {"profile_id": 3, "user_id": 2, "profile_name": "Priya", "profile_type": "Adult"},
    {"profile_id": 4, "user_id": 2, "profile_name": "Mom", "profile_type": "Adult"},
    {"profile_id": 5, "user_id": 3, "profile_name": "Rohan", "profile_type": "Adult"},
    {"profile_id": 6, "user_id": 4, "profile_name": "Sneha", "profile_type": "Adult"},
    {"profile_id": 7, "user_id": 4, "profile_name": "Little Star", "profile_type": "Kids"},
    {"profile_id": 8, "user_id": 5, "profile_name": "Vikram", "profile_type": "Adult"},
    {"profile_id": 9, "user_id": 6, "profile_name": "Ananya", "profile_type": "Adult"},
    {"profile_id": 10, "user_id": 7, "profile_name": "Karan", "profile_type": "Adult"},
    {"profile_id": 11, "user_id": 8, "profile_name": "Divya", "profile_type": "Adult"},
    {"profile_id": 12, "user_id": 9, "profile_name": "Arjun", "profile_type": "Adult"},
    {"profile_id": 13, "user_id": 10, "profile_name": "Meera", "profile_type": "Adult"},
    {"profile_id": 14, "user_id": 10, "profile_name": "Family", "profile_type": "Kids"},
]

# ============================================================
# ENTITY: SUBSCRIPTION
# Attributes: SUBS_ID, USER_ID, PLAN_ID, START_DATE, END_DATE, STATUS
# ============================================================
SUBSCRIPTIONS = [
    {"subs_id": 1, "user_id": 1, "plan_id": 4, "start_date": "2024-01-15", "end_date": "2024-02-15", "status": "Active"},
    {"subs_id": 2, "user_id": 2, "plan_id": 3, "start_date": "2024-02-20", "end_date": "2024-03-20", "status": "Active"},
    {"subs_id": 3, "user_id": 3, "plan_id": 2, "start_date": "2024-01-10", "end_date": "2024-02-10", "status": "Expired"},
    {"subs_id": 4, "user_id": 4, "plan_id": 4, "start_date": "2024-03-05", "end_date": "2024-04-05", "status": "Active"},
    {"subs_id": 5, "user_id": 5, "plan_id": 1, "start_date": "2024-04-18", "end_date": "2024-05-18", "status": "Active"},
    {"subs_id": 6, "user_id": 6, "plan_id": 6, "start_date": "2024-01-22", "end_date": "2025-01-22", "status": "Active"},
    {"subs_id": 7, "user_id": 7, "plan_id": 3, "start_date": "2024-05-30", "end_date": "2024-06-30", "status": "Active"},
    {"subs_id": 8, "user_id": 8, "plan_id": 5, "start_date": "2024-02-14", "end_date": "2024-08-14", "status": "Active"},
    {"subs_id": 9, "user_id": 9, "plan_id": 2, "start_date": "2024-06-05", "end_date": "2024-07-05", "status": "Cancelled"},
    {"subs_id": 10, "user_id": 10, "plan_id": 4, "start_date": "2024-07-28", "end_date": "2024-08-28", "status": "Active"},
    {"subs_id": 11, "user_id": 3, "plan_id": 3, "start_date": "2024-03-10", "end_date": "2024-04-10", "status": "Active"},
]

# ============================================================
# ENTITY: PAYMENTS
# Attributes: PAYMENT_ID, USER_ID, SUBS_ID, AMOUNT, PAY_DATE, PAY_METHOD, STATUS
# ============================================================
PAYMENTS = [
    {"payment_id": 1, "user_id": 1, "subs_id": 1, "amount": 649, "pay_date": "2024-01-15", "pay_method": "Credit Card", "status": "Success"},
    {"payment_id": 2, "user_id": 2, "subs_id": 2, "amount": 499, "pay_date": "2024-02-20", "pay_method": "UPI", "status": "Success"},
    {"payment_id": 3, "user_id": 3, "subs_id": 3, "amount": 199, "pay_date": "2024-01-10", "pay_method": "Debit Card", "status": "Success"},
    {"payment_id": 4, "user_id": 4, "subs_id": 4, "amount": 649, "pay_date": "2024-03-05", "pay_method": "Net Banking", "status": "Success"},
    {"payment_id": 5, "user_id": 5, "subs_id": 5, "amount": 149, "pay_date": "2024-04-18", "pay_method": "UPI", "status": "Success"},
    {"payment_id": 6, "user_id": 6, "subs_id": 6, "amount": 4999, "pay_date": "2024-01-22", "pay_method": "Credit Card", "status": "Success"},
    {"payment_id": 7, "user_id": 7, "subs_id": 7, "amount": 499, "pay_date": "2024-05-30", "pay_method": "UPI", "status": "Success"},
    {"payment_id": 8, "user_id": 8, "subs_id": 8, "amount": 149, "pay_date": "2024-02-14", "pay_method": "Wallet", "status": "Success"},
    {"payment_id": 9, "user_id": 9, "subs_id": 9, "amount": 199, "pay_date": "2024-06-05", "pay_method": "UPI", "status": "Failed"},
    {"payment_id": 10, "user_id": 9, "subs_id": 9, "amount": 199, "pay_date": "2024-06-05", "pay_method": "Credit Card", "status": "Success"},
    {"payment_id": 11, "user_id": 10, "subs_id": 10, "amount": 649, "pay_date": "2024-07-28", "pay_method": "Net Banking", "status": "Success"},
    {"payment_id": 12, "user_id": 3, "subs_id": 11, "amount": 499, "pay_date": "2024-03-10", "pay_method": "UPI", "status": "Success"},
]

# ============================================================
# ENTITY: GENRES
# Attributes: GENRE_ID, GENRE_NAME
# ============================================================
GENRES = [
    {"genre_id": 1, "genre_name": "Action"},
    {"genre_id": 2, "genre_name": "Comedy"},
    {"genre_id": 3, "genre_name": "Drama"},
    {"genre_id": 4, "genre_name": "Horror"},
    {"genre_id": 5, "genre_name": "Sci-Fi"},
    {"genre_id": 6, "genre_name": "Romance"},
    {"genre_id": 7, "genre_name": "Thriller"},
    {"genre_id": 8, "genre_name": "Documentary"},
    {"genre_id": 9, "genre_name": "Animation"},
    {"genre_id": 10, "genre_name": "Fantasy"},
]

# ============================================================
# ENTITY: DIRECTORS
# Attributes: DIRECTOR_ID, DIRECTOR_NAME
# ============================================================
DIRECTORS = [
    {"director_id": 1, "director_name": "Rajkumar Hirani"},
    {"director_id": 2, "director_name": "S.S. Rajamouli"},
    {"director_id": 3, "director_name": "Zoya Akhtar"},
    {"director_id": 4, "director_name": "Anurag Kashyap"},
    {"director_id": 5, "director_name": "Shoojit Sircar"},
    {"director_id": 6, "director_name": "Vetrimaaran"},
    {"director_id": 7, "director_name": "Neeraj Pandey"},
    {"director_id": 8, "director_name": "Imtiaz Ali"},
    {"director_id": 9, "director_name": "Sanjay Leela Bhansali"},
    {"director_id": 10, "director_name": "Mani Ratnam"},
]

# ============================================================
# ENTITY: ACTORS
# Attributes: ACTOR_ID, ACTOR_NAME
# ============================================================
ACTORS = [
    {"actor_id": 1, "actor_name": "Shah Rukh Khan"},
    {"actor_id": 2, "actor_name": "Aamir Khan"},
    {"actor_id": 3, "actor_name": "Deepika Padukone"},
    {"actor_id": 4, "actor_name": "Ranveer Singh"},
    {"actor_id": 5, "actor_name": "Alia Bhatt"},
    {"actor_id": 6, "actor_name": "Prabhas"},
    {"actor_id": 7, "actor_name": "Vijay Sethupathi"},
    {"actor_id": 8, "actor_name": "Tabu"},
    {"actor_id": 9, "actor_name": "Rajkummar Rao"},
    {"actor_id": 10, "actor_name": "Samantha Ruth Prabhu"},
    {"actor_id": 11, "actor_name": "Dhanush"},
    {"actor_id": 12, "actor_name": "Konkona Sen Sharma"},
]

# ============================================================
# ENTITY: CONTENT
# Attributes: CONTENT_ID, TITLE, DESCRIPTION, DURATION, LANGUAGE, TYPE, RELEASE_YEAR, MATURITY, RATING
# ============================================================
CONTENT = [
    {
        "content_id": 1, "title": "Dark Horizon",
        "description": "An expedition near Jupiter encounters unexpected gravitational anomalies. The flight crew works to maintain telemetry contact while analyzing anomalous atmospheric data.",
        "duration": 142, "language": "Hindi", "type": "Movie", "release_year": 2024, "maturity": "U/A 16+", "rating": 8.5,
        "poster_url": "https://images.unsplash.com/photo-1534996858221-380b92700493?w=400&h=600&fit=crop",
        "backdrop_url": "https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=1200&h=500&fit=crop"
    },
    {
        "content_id": 2, "title": "Autumn in Paris",
        "description": "An architect on sabbatical in Paris crosses paths with an archivist documenting historical neighborhood renovations. Their conversations explore preservation, urban memory, and personal choices.",
        "duration": 118, "language": "English", "type": "Movie", "release_year": 2023, "maturity": "U/A 13+", "rating": 7.8,
        "poster_url": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400&h=600&fit=crop",
        "backdrop_url": "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?w=1200&h=500&fit=crop"
    },
    {
        "content_id": 3, "title": "Shadow Agent",
        "description": "An undercover intelligence officer tracks financial irregularities tied to maritime shipping corridors in Bangkok. When communications are disrupted, he must coordinate an extraction.",
        "duration": 156, "language": "Hindi", "type": "Movie", "release_year": 2024, "maturity": "A", "rating": 8.9,
        "poster_url": "https://images.unsplash.com/photo-1536440136628-849c177e76a1?w=400&h=600&fit=crop",
        "backdrop_url": "https://images.unsplash.com/photo-1519608487953-e999c86e7455?w=1200&h=500&fit=crop"
    },
    {
        "content_id": 4, "title": "The Enchanted Kingdom",
        "description": "A rural community in northern Wales discovers historical boundary stones linked to early medieval folklore. A local scholar documents archaeological findings amidst regional land development.",
        "duration": 165, "language": "English", "type": "Movie", "release_year": 2024, "maturity": "U", "rating": 8.2,
        "poster_url": "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?w=400&h=600&fit=crop",
        "backdrop_url": "https://images.unsplash.com/photo-1440342359743-84fcb8c21c7f?w=1200&h=500&fit=crop"
    },
    {
        "content_id": 5, "title": "The Haunting of Raven Manor",
        "description": "An estate evaluation team inspects a secluded manor in Yorkshire prior to public auction. Unexplained structural noises and historical tenancy records prompt an inquiry into the building's past.",
        "duration": 128, "language": "English", "type": "Movie", "release_year": 2023, "maturity": "A", "rating": 7.4,
        "poster_url": "https://images.unsplash.com/photo-1509248961085-879e3e5b624c?w=400&h=600&fit=crop",
        "backdrop_url": "https://images.unsplash.com/photo-1520034475321-cbe63696469a?w=1200&h=500&fit=crop"
    },
    {
        "content_id": 6, "title": "Ocean Depths",
        "description": "Marine researchers record biological activity along the Mariana Trench using specialized submersibles, capturing benthic ecosystem adaptations and deep-sea current patterns.",
        "duration": 95, "language": "English", "type": "Movie", "release_year": 2024, "maturity": "U", "rating": 9.1,
        "poster_url": "https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=400&h=600&fit=crop",
        "backdrop_url": "https://images.unsplash.com/photo-1518837695005-2083093ee35b?w=1200&h=500&fit=crop"
    },
    {
        "content_id": 7, "title": "Mumbai Nights",
        "description": "A drama series tracing five transit workers across Mumbai during the monsoon season as they navigate municipal rail schedules, personal obligations, and neighborhood community events.",
        "duration": 45, "language": "Hindi", "type": "Series", "release_year": 2024, "maturity": "U/A 16+", "rating": 8.7,
        "poster_url": "https://images.unsplash.com/photo-1570168007204-dfb528c6958f?w=400&h=600&fit=crop",
        "backdrop_url": "https://images.unsplash.com/photo-1566552881560-0be862a7c445?w=1200&h=500&fit=crop"
    },
    {
        "content_id": 8, "title": "Code Breakers",
        "description": "Historical drama recounting cryptographic efforts at Bletchley Park during the Battle of the Atlantic, detailing rotor mechanical calculations and intelligence verification protocols.",
        "duration": 55, "language": "English", "type": "Series", "release_year": 2023, "maturity": "U/A 13+", "rating": 8.3,
        "poster_url": "https://images.unsplash.com/photo-1550751827-4bd374c3f58b?w=400&h=600&fit=crop",
        "backdrop_url": "https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=1200&h=500&fit=crop"
    },
    {
        "content_id": 9, "title": "The Last Garden",
        "description": "An animated film following an agricultural scientist managing an experimental seed vault beneath an expanding industrial district, examining conservation and urban ecology.",
        "duration": 110, "language": "Hindi", "type": "Movie", "release_year": 2024, "maturity": "U", "rating": 8.8,
        "poster_url": "https://images.unsplash.com/photo-1585320806297-9794b3e4eeae?w=400&h=600&fit=crop",
        "backdrop_url": "https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=1200&h=500&fit=crop"
    },
    {
        "content_id": 10, "title": "Gangster's Paradise",
        "description": "A crime drama documenting port customs enforcement and smuggling syndicates in 1980s Bombay, chronicling legal investigations and court proceedings.",
        "duration": 170, "language": "Hindi", "type": "Movie", "release_year": 2023, "maturity": "A", "rating": 8.0,
        "poster_url": "https://images.unsplash.com/photo-1478720568477-152d9b164e26?w=400&h=600&fit=crop",
        "backdrop_url": "https://images.unsplash.com/photo-1494976388531-d1058494cdd8?w=1200&h=500&fit=crop"
    },
    {
        "content_id": 11, "title": "Laugh Factory",
        "description": "A comedy series following the operational staff and touring comedians at a metropolitan performance venue preparing for weekend show lineups.",
        "duration": 30, "language": "Hindi", "type": "Series", "release_year": 2024, "maturity": "U/A 13+", "rating": 7.6,
        "poster_url": "https://images.unsplash.com/photo-1527224857830-43a7acc85260?w=400&h=600&fit=crop",
        "backdrop_url": "https://images.unsplash.com/photo-1516280440614-37939bbacd81?w=1200&h=500&fit=crop"
    },
    {
        "content_id": 12, "title": "Mountain Spirits",
        "description": "A documentary capturing high-altitude meteorological research stations and traditional farming communities across the Spiti and Ladakh valleys.",
        "duration": 88, "language": "Hindi", "type": "Movie", "release_year": 2024, "maturity": "U", "rating": 9.0,
        "poster_url": "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=400&h=600&fit=crop",
        "backdrop_url": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=1200&h=500&fit=crop"
    },
    {
        "content_id": 13, "title": "Cyber Hunt",
        "description": "A technical procedural series depicting forensic investigators responding to ransomware intrusions affecting regional utility networks.",
        "duration": 50, "language": "English", "type": "Series", "release_year": 2024, "maturity": "U/A 16+", "rating": 8.4,
        "poster_url": "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?w=400&h=600&fit=crop",
        "backdrop_url": "https://images.unsplash.com/photo-1550745165-9bc0b252726f?w=1200&h=500&fit=crop"
    },
    {
        "content_id": 14, "title": "Wedding Season",
        "description": "A social comedy centering on two event planning partners coordinating logistics for a multi-day family wedding celebration in Jaipur.",
        "duration": 135, "language": "Hindi", "type": "Movie", "release_year": 2023, "maturity": "U", "rating": 7.5,
        "poster_url": "https://images.unsplash.com/photo-1519741497674-611481863552?w=400&h=600&fit=crop",
        "backdrop_url": "https://images.unsplash.com/photo-1511285560929-80b456fea0bc?w=1200&h=500&fit=crop"
    },
    {
        "content_id": 15, "title": "Tiger's Eye",
        "description": "A wildlife documentary documenting habitat conservation efforts and radio-collar tracking data in Bandhavgarh National Park.",
        "duration": 102, "language": "Hindi", "type": "Movie", "release_year": 2024, "maturity": "U/A 13+", "rating": 8.6,
        "poster_url": "https://images.unsplash.com/photo-1549366021-9f761d450615?w=400&h=600&fit=crop",
        "backdrop_url": "https://images.unsplash.com/photo-1474511320723-9a56873571b7?w=1200&h=500&fit=crop"
    },
]

# ============================================================
# JUNCTION TABLE: CONTENT_GENRES (M:M between CONTENT and GENRES)
# ============================================================
CONTENT_GENRES = [
    {"content_id": 1, "genre_id": 5}, {"content_id": 1, "genre_id": 7},
    {"content_id": 2, "genre_id": 6}, {"content_id": 2, "genre_id": 3},
    {"content_id": 3, "genre_id": 1}, {"content_id": 3, "genre_id": 7},
    {"content_id": 4, "genre_id": 10}, {"content_id": 4, "genre_id": 1},
    {"content_id": 5, "genre_id": 4}, {"content_id": 5, "genre_id": 7},
    {"content_id": 6, "genre_id": 8},
    {"content_id": 7, "genre_id": 3}, {"content_id": 7, "genre_id": 2},
    {"content_id": 8, "genre_id": 3}, {"content_id": 8, "genre_id": 7},
    {"content_id": 9, "genre_id": 9}, {"content_id": 9, "genre_id": 5},
    {"content_id": 10, "genre_id": 1}, {"content_id": 10, "genre_id": 3},
    {"content_id": 11, "genre_id": 2},
    {"content_id": 12, "genre_id": 8}, {"content_id": 12, "genre_id": 3},
    {"content_id": 13, "genre_id": 5}, {"content_id": 13, "genre_id": 7},
    {"content_id": 14, "genre_id": 6}, {"content_id": 14, "genre_id": 2},
    {"content_id": 15, "genre_id": 8}, {"content_id": 15, "genre_id": 7},
]

# ============================================================
# JUNCTION TABLE: CONTENT_DIRECTORS (M:M between CONTENT and DIRECTORS)
# ============================================================
CONTENT_DIRECTORS = [
    {"content_id": 1, "director_id": 2},
    {"content_id": 2, "director_id": 8},
    {"content_id": 3, "director_id": 7},
    {"content_id": 4, "director_id": 2},
    {"content_id": 5, "director_id": 4},
    {"content_id": 6, "director_id": 5},
    {"content_id": 7, "director_id": 3},
    {"content_id": 8, "director_id": 7},
    {"content_id": 9, "director_id": 1},
    {"content_id": 10, "director_id": 4},
    {"content_id": 11, "director_id": 3},
    {"content_id": 12, "director_id": 5},
    {"content_id": 13, "director_id": 7},
    {"content_id": 14, "director_id": 8},
    {"content_id": 15, "director_id": 6},
]

# ============================================================
# JUNCTION TABLE: CONTENT_ACTORS / ACTED_BY (M:M between CONTENT and ACTORS)
# ============================================================
CONTENT_ACTORS = [
    {"content_id": 1, "actor_id": 6}, {"content_id": 1, "actor_id": 3},
    {"content_id": 2, "actor_id": 5}, {"content_id": 2, "actor_id": 4},
    {"content_id": 3, "actor_id": 1}, {"content_id": 3, "actor_id": 8},
    {"content_id": 4, "actor_id": 3}, {"content_id": 4, "actor_id": 9},
    {"content_id": 5, "actor_id": 8}, {"content_id": 5, "actor_id": 12},
    {"content_id": 6, "actor_id": 11},
    {"content_id": 7, "actor_id": 7}, {"content_id": 7, "actor_id": 10},
    {"content_id": 8, "actor_id": 2}, {"content_id": 8, "actor_id": 12},
    {"content_id": 9, "actor_id": 5}, {"content_id": 9, "actor_id": 9},
    {"content_id": 10, "actor_id": 4}, {"content_id": 10, "actor_id": 1},
    {"content_id": 11, "actor_id": 7}, {"content_id": 11, "actor_id": 9},
    {"content_id": 12, "actor_id": 11},
    {"content_id": 13, "actor_id": 1}, {"content_id": 13, "actor_id": 10},
    {"content_id": 14, "actor_id": 5}, {"content_id": 14, "actor_id": 4},
    {"content_id": 15, "actor_id": 6}, {"content_id": 15, "actor_id": 8},
]

REVIEW_RATINGS = [
    {"review_id": 1, "content_id": 1, "user_id": 1, "review_text": "Strong sound mixing and visual effects throughout. The mid-film pacing slows down slightly, but the climax ties the plot together well.", "review_date": "2024-03-15", "rating": 8},
    {"review_id": 2, "content_id": 1, "user_id": 3, "review_text": "The orbital physics and technical dialogue feel credible. Good choice for hard science fiction fans.", "review_date": "2024-03-20", "rating": 7},
    {"review_id": 3, "content_id": 2, "user_id": 2, "review_text": "Subtle cinematography and thoughtful location work in Paris. Well-acted without melodramatic tropes.", "review_date": "2024-02-28", "rating": 8},
    {"review_id": 4, "content_id": 3, "user_id": 4, "review_text": "Solid action set pieces in the port sequences. Editing keeps the procedural tension consistent.", "review_date": "2024-04-10", "rating": 8},
    {"review_id": 5, "content_id": 3, "user_id": 5, "review_text": "Neeraj Pandey maintains his familiar gritty investigation rhythm. Lead acting by Shah Rukh Khan carries the operational scenes.", "review_date": "2024-04-12", "rating": 9},
    {"review_id": 6, "content_id": 4, "user_id": 6, "review_text": "Careful attention to regional landscape and production design. The plot progresses at a deliberate pace.", "review_date": "2024-05-01", "rating": 8},
    {"review_id": 7, "content_id": 5, "user_id": 1, "review_text": "Good sound design and lighting. Avoids cheap jump scares in favor of building architectural dread.", "review_date": "2024-05-15", "rating": 7},
    {"review_id": 8, "content_id": 6, "user_id": 7, "review_text": "Very clean 4K underwater photography and informative scientific narration regarding trench biology.", "review_date": "2024-06-01", "rating": 9},
    {"review_id": 9, "content_id": 7, "user_id": 8, "review_text": "Effective ensemble drama focusing on suburban rail workers. Captures realistic Mumbai transit routines.", "review_date": "2024-06-20", "rating": 9},
    {"review_id": 10, "content_id": 7, "user_id": 2, "review_text": "Well-written character arcs and strong dialogue work from the secondary cast members.", "review_date": "2024-06-25", "rating": 8},
    {"review_id": 11, "content_id": 9, "user_id": 10, "review_text": "Art style is distinct and cohesive. Explores urban conservation themes with emotional restraint.", "review_date": "2024-07-10", "rating": 8},
    {"review_id": 12, "content_id": 10, "user_id": 9, "review_text": "Convincing period production design of 1980s docklands. The court case sequences are well researched.", "review_date": "2024-07-20", "rating": 8},
    {"review_id": 13, "content_id": 12, "user_id": 6, "review_text": "Respectful and unobtrusive documentary approach to high-altitude agrarian life.", "review_date": "2024-08-01", "rating": 9},
    {"review_id": 14, "content_id": 13, "user_id": 3, "review_text": "Depicts actual network monitoring commands and packet analysis without exaggerated movie hacking clichés.", "review_date": "2024-08-15", "rating": 8},
    {"review_id": 15, "content_id": 15, "user_id": 4, "review_text": "Balanced exploration of wildlife reserve challenges and anti-poaching patrol duties.", "review_date": "2024-09-01", "rating": 9},
]

# ============================================================
# ENTITY: WATCH_HISTORY
# Attributes: HISTORY_ID, CONTENT_ID, USER_ID, WATCH_DATE, COMPLETED, PROGRESS_MIN
# ============================================================
WATCH_HISTORY = [
    {"history_id": 1, "content_id": 1, "user_id": 1, "watch_date": "2024-03-14", "completed": True, "progress_min": 142},
    {"history_id": 2, "content_id": 3, "user_id": 1, "watch_date": "2024-03-16", "completed": True, "progress_min": 156},
    {"history_id": 3, "content_id": 7, "user_id": 1, "watch_date": "2024-04-01", "completed": False, "progress_min": 30},
    {"history_id": 4, "content_id": 2, "user_id": 2, "watch_date": "2024-02-25", "completed": True, "progress_min": 118},
    {"history_id": 5, "content_id": 7, "user_id": 2, "watch_date": "2024-06-20", "completed": True, "progress_min": 45},
    {"history_id": 6, "content_id": 1, "user_id": 3, "watch_date": "2024-03-18", "completed": True, "progress_min": 142},
    {"history_id": 7, "content_id": 13, "user_id": 3, "watch_date": "2024-08-10", "completed": False, "progress_min": 35},
    {"history_id": 8, "content_id": 3, "user_id": 4, "watch_date": "2024-04-08", "completed": True, "progress_min": 156},
    {"history_id": 9, "content_id": 15, "user_id": 4, "watch_date": "2024-08-30", "completed": True, "progress_min": 102},
    {"history_id": 10, "content_id": 3, "user_id": 5, "watch_date": "2024-04-20", "completed": True, "progress_min": 156},
    {"history_id": 11, "content_id": 5, "user_id": 5, "watch_date": "2024-05-10", "completed": False, "progress_min": 60},
    {"history_id": 12, "content_id": 4, "user_id": 6, "watch_date": "2024-04-28", "completed": True, "progress_min": 165},
    {"history_id": 13, "content_id": 12, "user_id": 6, "watch_date": "2024-07-28", "completed": True, "progress_min": 88},
    {"history_id": 14, "content_id": 6, "user_id": 7, "watch_date": "2024-05-28", "completed": True, "progress_min": 95},
    {"history_id": 15, "content_id": 9, "user_id": 7, "watch_date": "2024-06-15", "completed": True, "progress_min": 110},
    {"history_id": 16, "content_id": 7, "user_id": 8, "watch_date": "2024-06-18", "completed": True, "progress_min": 45},
    {"history_id": 17, "content_id": 11, "user_id": 8, "watch_date": "2024-07-01", "completed": True, "progress_min": 30},
    {"history_id": 18, "content_id": 10, "user_id": 9, "watch_date": "2024-07-15", "completed": True, "progress_min": 170},
    {"history_id": 19, "content_id": 9, "user_id": 10, "watch_date": "2024-07-05", "completed": True, "progress_min": 110},
    {"history_id": 20, "content_id": 14, "user_id": 10, "watch_date": "2024-08-20", "completed": False, "progress_min": 70},
    {"history_id": 21, "content_id": 1, "user_id": 4, "watch_date": "2024-03-22", "completed": True, "progress_min": 142},
    {"history_id": 22, "content_id": 2, "user_id": 6, "watch_date": "2024-03-01", "completed": True, "progress_min": 118},
    {"history_id": 23, "content_id": 8, "user_id": 1, "watch_date": "2024-05-20", "completed": True, "progress_min": 55},
    {"history_id": 24, "content_id": 14, "user_id": 2, "watch_date": "2024-04-15", "completed": True, "progress_min": 135},
    {"history_id": 25, "content_id": 11, "user_id": 5, "watch_date": "2024-06-01", "completed": True, "progress_min": 30},
]


# ============================================================
# Helper functions to resolve relationships
# ============================================================
def get_content_genres(content_id):
    """Get genre names for a content item."""
    genre_ids = [cg["genre_id"] for cg in CONTENT_GENRES if cg["content_id"] == content_id]
    return [g["genre_name"] for g in GENRES if g["genre_id"] in genre_ids]

def get_content_actors(content_id):
    """Get actor names for a content item."""
    actor_ids = [ca["actor_id"] for ca in CONTENT_ACTORS if ca["content_id"] == content_id]
    return [a["actor_name"] for a in ACTORS if a["actor_id"] in actor_ids]

def get_content_director(content_id):
    """Get director name for a content item."""
    director_ids = [cd["director_id"] for cd in CONTENT_DIRECTORS if cd["content_id"] == content_id]
    directors = [d["director_name"] for d in DIRECTORS if d["director_id"] in director_ids]
    return directors[0] if directors else "Unknown"

def get_user_profiles(user_id):
    """Get profiles belonging to a user."""
    return [p for p in PROFILES if p["user_id"] == user_id]

def get_user_subscription(user_id):
    """Get active subscription for a user."""
    subs = [s for s in SUBSCRIPTIONS if s["user_id"] == user_id and s["status"] == "Active"]
    return subs[-1] if subs else None

def get_plan_details(plan_id):
    """Get plan details by ID."""
    plans = [p for p in SUBS_PLANS if p["plan_id"] == plan_id]
    return plans[0] if plans else None

def get_content_reviews(content_id):
    """Get reviews for a content item."""
    reviews = [r for r in REVIEW_RATINGS if r["content_id"] == content_id]
    for review in reviews:
        user = next((u for u in USERS if u["user_id"] == review["user_id"]), None)
        review["user_name"] = user["name"] if user else "Anonymous"
    return reviews

def get_user_watch_history(user_id):
    """Get watch history for a user."""
    history = [h for h in WATCH_HISTORY if h["user_id"] == user_id]
    for h in history:
        content = next((c for c in CONTENT if c["content_id"] == h["content_id"]), None)
        if content:
            h["title"] = content["title"]
            h["duration"] = content["duration"]
            h["poster_url"] = content["poster_url"]
            h["type"] = content["type"]
    return history

def get_user_payments(user_id):
    """Get payment history for a user."""
    return [p for p in PAYMENTS if p["user_id"] == user_id]
