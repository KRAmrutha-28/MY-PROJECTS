import os
import django
from datetime import date, time
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from courses.models import Campus, Course, BTechSpecialization
from faculty.models import Faculty, Room
from transport.models import BusRoute, Bus
from admissions.models import Admission
from inquiries.models import Inquiry

def populate_data():
    print("="*60)
    print("🏛️  Setting up CHANAKYA UNIVERSITY Database")
    print("="*60)
    
    # Create Campuses
    campus1, created1 = Campus.objects.get_or_create(
        name="Main Campus - Vidya Vihar",
        defaults={
            "location": "123 Knowledge Park, Near City Center",
            "description": "Main campus of Chanakya University with all engineering and management departments"
        }
    )
    
    campus2, created2 = Campus.objects.get_or_create(
        name="South Campus - Kautilya Nagar",
        defaults={
            "location": "456 Education Hub, Southern Suburbs",
            "description": "South campus of Chanakya University for research and postgraduate studies"
        }
    )
    
    campus3, created3 = Campus.objects.get_or_create(
        name="Tech Park Campus",
        defaults={
            "location": "789 Innovation Boulevard, Tech Corridor",
            "description": "Chanakya University's tech park campus with state-of-the-art laboratories"
        }
    )
    
    print(f"✅ Created {Campus.objects.count()} Campuses")
    
    # Create BTech Specializations
    btech_specs = [
        ('CS', 'Computer Science', 180, 75, 175000),
        ('EC', 'Electronics & Communication', 120, 50, 175000),
        ('ME', 'Mechanical Engineering', 120, 45, 175000),
        ('CE', 'Civil Engineering', 90, 35, 175000),
        ('EE', 'Electrical Engineering', 90, 40, 175000),
    ]
    
    for code, name, total, available, fee in btech_specs:
        BTechSpecialization.objects.get_or_create(
            specialization=code,
            defaults={
                "total_seats": total,
                "available_seats": available,
                "fee_per_year": fee
            }
        )
    
    print(f"✅ Created {BTechSpecialization.objects.count()} BTech Specializations")
    
    # Create Courses
    courses_data = [
        ("Bachelor of Technology", "BTECH001", "UG", "Computer Science", campus1, 4, 
         "Bachelor of Technology in Computer Science with specialization in AI/ML, Cloud Computing, Cybersecurity, and Data Science at Chanakya University", 175000),
        ("Bachelor of Technology", "BTECH002", "UG", "Electronics & Communication", campus1, 4,
         "Bachelor of Technology in Electronics and Communication with focus on VLSI, Embedded Systems, IoT, and Robotics at Chanakya University", 175000),
        ("Bachelor of Computer Applications", "BCA001", "UG", "Computer Applications", campus1, 3,
         "Bachelor of Computer Applications with focus on Web Development, Mobile Apps, and Cloud Computing at Chanakya University", 120000),
        ("Bachelor of Business Administration", "BBA001", "UG", "Business Management", campus2, 3,
         "Bachelor of Business Administration with specialization in Marketing, Finance, and HR at Chanakya University", 100000),
        ("Master of Technology", "MTECH001", "PG", "Computer Science", campus1, 2,
         "Master of Technology in Computer Science with research focus on AI, ML, and Big Data Analytics at Chanakya University", 200000),
        ("Master of Computer Applications", "MCA001", "PG", "Computer Applications", campus1, 2,
         "Master of Computer Applications with industry-oriented curriculum at Chanakya University", 150000),
        ("Master of Business Administration", "MBA001", "PG", "Business Administration", campus2, 2,
         "MBA program with dual specialization in Marketing, Finance, HR, or Operations at Chanakya University", 250000),
    ]
    
    for name, code, course_type, spec, campus, duration, desc, fee in courses_data:
        course, created = Course.objects.get_or_create(
            code=code,
            defaults={
                "name": name,
                "course_type": course_type,
                "specialization": spec,
                "campus": campus,
                "duration": duration,
                "description": desc,
                "fee": fee
            }
        )
    
    print(f"✅ Created {Course.objects.count()} Courses")
    
    # Create Faculty
    faculty_data = [
        ("Dr. Rajesh Kumar", "rajesh.kumar@chanakya.edu", "9876543210", "PROF", 
         "Ph.D. in Computer Science (IIT Delhi)", "Artificial Intelligence", 18, True,
         date(2010, 6, 1), "Padma Shri awardee, Author of 50+ research papers in AI"),
        ("Dr. Priya Sharma", "priya.sharma@chanakya.edu", "9876543211", "PROF",
         "Ph.D. in Electronics (IIT Bombay)", "VLSI Design", 15, True,
         date(2012, 7, 15), "Fellow of IEEE, Expert in Chip Design"),
        ("Dr. Amit Singh", "amit.singh@chanakya.edu", "9876543212", "APROF",
         "Ph.D. in Data Science (Stanford University)", "Machine Learning", 10, False,
         date(2015, 8, 10), "Google Faculty Award winner"),
        ("Dr. Kavita Reddy", "kavita.reddy@chanakya.edu", "9876543215", "PROF",
         "Ph.D. in Management (IIM Ahmedabad)", "Strategic Management", 20, True,
         date(2008, 7, 20), "Former Dean, Author of 5 Management Books"),
    ]
    
    btech_cs = Course.objects.filter(specialization="Computer Science").first()
    btech_ec = Course.objects.filter(specialization="Electronics & Communication").first()
    mba_course = Course.objects.filter(specialization="Business Administration").first()
    
    for name, email, phone, desig, qual, spec, exp, is_hod, join_date, bio in faculty_data:
        faculty, created = Faculty.objects.get_or_create(
            email=email,
            defaults={
                "name": name,
                "phone": phone,
                "designation": desig,
                "qualification": qual,
                "specialization": spec,
                "experience_years": exp,
                "is_hod": is_hod,
                "joining_date": join_date,
                "bio": bio
            }
        )
        if btech_cs and ("Computer" in spec or "AI" in spec or "Data" in spec):
            faculty.courses.add(btech_cs)
        if btech_ec and ("Electronics" in spec or "VLSI" in spec):
            faculty.courses.add(btech_ec)
        if mba_course and ("Management" in spec):
            faculty.courses.add(mba_course)
    
    print(f"✅ Created {Faculty.objects.count()} Faculty Members")
    
    # Create Rooms
    rooms_data = [
        ("A-101", "LECTURE", 80, btech_cs, "Smart board, 4K Projector, AC, Wi-Fi", True, True),
        ("CS-LAB-01", "LAB", 50, btech_cs, "80 High-end Computers, GPU Workstations", True, True),
        ("EC-LAB-01", "LAB", 45, btech_ec, "VLSI Design Tools, Oscilloscopes", True, True),
    ]
    
    for room_num, room_type, capacity, course, facilities, ac, proj in rooms_data:
        if course:
            Room.objects.get_or_create(
                room_number=room_num,
                course=course,
                defaults={
                    "room_type": room_type,
                    "capacity": capacity,
                    "facilities": facilities,
                    "is_ac_available": ac,
                    "has_projector": proj
                }
            )
    
    print(f"✅ Created {Room.objects.count()} Rooms")
    
    # Create Transport
    route1, _ = BusRoute.objects.get_or_create(
        route_number="R-101",
        defaults={
            "route_name": "City Center Express",
            "start_point": "Central Station",
            "end_point": "Main Campus",
            "stops": "Central Station → City Mall → Main Campus",
            "distance_km": 15.5
        }
    )
    
    Bus.objects.get_or_create(
        bus_number="CH-01-AB-1234",
        defaults={
            "route": route1,
            "capacity": 50,
            "driver_name": "Suresh Singh",
            "driver_contact": "9988776655",
            "morning_departure": time(7, 0),
            "evening_departure": time(18, 0),
            "status": "ACTIVE",
            "registration_number": "UP12AB1234"
        }
    )
    
    print(f"✅ Created Transport Services")
    
    # Create Admissions
    for course in Course.objects.all()[:3]:
        Admission.objects.get_or_create(
            course=course,
            defaults={
                "status": "OPEN",
                "last_date": date(2026, 6, 30),
                "eligibility_criteria": "10+2 with 60% marks",
                "application_fee": 1500.00,
                "required_documents": "Marksheets, Certificates",
                "admission_process": "Online application"
            }
        )
    
    print(f"✅ Created {Admission.objects.count()} Admissions")
    
    print("\n" + "="*60)
    print("🏛️  CHANAKYA UNIVERSITY Database Setup Complete!")
    print("="*60)

if __name__ == "__main__":
    populate_data()
