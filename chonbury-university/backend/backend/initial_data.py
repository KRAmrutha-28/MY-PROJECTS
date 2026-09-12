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
        # UG Courses
        ("Bachelor of Technology", "BTECH001", "UG", "Computer Science", campus1, 4, 
         "Bachelor of Technology in Computer Science with specialization in AI/ML, Cloud Computing, Cybersecurity, and Data Science at Chanakya University", 175000),
        
        ("Bachelor of Technology", "BTECH002", "UG", "Electronics & Communication", campus1, 4,
         "Bachelor of Technology in Electronics and Communication with focus on VLSI, Embedded Systems, IoT, and Robotics at Chanakya University", 175000),
        
        ("Bachelor of Technology", "BTECH003", "UG", "Mechanical Engineering", campus2, 4,
         "Bachelor of Technology in Mechanical Engineering specializing in Robotics, Automation, and CAD/CAM at Chanakya University", 175000),
        
        ("Bachelor of Computer Applications", "BCA001", "UG", "Computer Applications", campus1, 3,
         "Bachelor of Computer Applications with focus on Web Development, Mobile Apps, and Cloud Computing at Chanakya University", 120000),
        
        ("Bachelor of Business Administration", "BBA001", "UG", "Business Management", campus2, 3,
         "Bachelor of Business Administration with specialization in Marketing, Finance, and HR at Chanakya University", 100000),
        
        # PG Courses
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
        if created:
            print(f"   Created course: {name} - {spec}")
    
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
        
        ("Dr. Neha Gupta", "neha.gupta@chanakya.edu", "9876543213", "APROF",
         "Ph.D. in Robotics (MIT)", "Robotics", 8, False,
         date(2016, 9, 5), "Young Scientist Award recipient"),
        
        ("Prof. Suresh Patel", "suresh.patel@chanakya.edu", "9876543214", "ASPROF",
         "M.Tech from IIT Kanpur", "Cloud Computing", 6, False,
         date(2018, 1, 15), "AWS Certified Solutions Architect"),
        
        ("Dr. Kavita Reddy", "kavita.reddy@chanakya.edu", "9876543215", "PROF",
         "Ph.D. in Management (IIM Ahmedabad)", "Strategic Management", 20, True,
         date(2008, 7, 20), "Former Dean, Author of 5 Management Books"),
    ]
    
    # Get courses for assignment
    btech_cs = Course.objects.filter(specialization="Computer Science").first()
    btech_ec = Course.objects.filter(specialization="Electronics & Communication").first()
    mba_course = Course.objects.filter(specialization="Business Administration").first()
    btech_me = Course.objects.filter(specialization="Mechanical Engineering").first()
    
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
        
        # Assign courses based on specialization
        if "Computer" in spec or "AI" in spec or "Data" in spec or "Machine" in spec:
            if btech_cs:
                faculty.courses.add(btech_cs)
        if "Electronics" in spec or "VLSI" in spec:
            if btech_ec:
                faculty.courses.add(btech_ec)
        if "Management" in spec or "Strategic" in spec:
            if mba_course:
                faculty.courses.add(mba_course)
        if "Robotics" in spec or "Mechanical" in spec:
            if btech_me:
                faculty.courses.add(btech_me)
    
    print(f"✅ Created {Faculty.objects.count()} Faculty Members")
    
    # Create Rooms and Facilities
    rooms_data = [
        ("A-101", "LECTURE", 80, btech_cs, "Smart board, 4K Projector, AC, Wi-Fi, Comfortable seating", True, True),
        ("CS-LAB-01", "LAB", 50, btech_cs, "80 High-end Computers, GPU Workstations, High-speed Internet, Projector, AC", True, True),
        ("CS-LAB-02", "LAB", 40, btech_cs, "50 Computers, AI/ML Software Suite, Linux/Windows, AC", True, True),
        ("EC-LAB-01", "LAB", 45, btech_ec, "VLSI Design Tools, Oscilloscopes, Signal Generators, AC", True, True),
        ("SEMINAR-01", "SEMINAR", 150, btech_cs, "Auditorium style, Advanced AV System, Recording Facility, AC", True, True),
        ("WORKSHOP-01", "WORKSHOP", 60, btech_ec, "Workbenches, Tools, 3D Printers, Soldering Stations, AC", True, True),
        ("AUDI-01", "AUDI", 500, btech_cs, "Full auditorium with stage, Advanced sound system, Projector", True, True),
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
    
    print(f"✅ Created {Room.objects.count()} Rooms/Facilities")
    
    # Create Transport Routes
    routes_data = [
        ("R-101", "City Center Express", "Central Station", "Main Campus - Vidya Vihar",
         "Central Station → City Mall → Railway Station → Bus Depot → Tech Park → Main Campus", 18.5),
        
        ("R-102", "North Suburb Shuttle", "North City Bus Stand", "South Campus - Kautilya Nagar",
         "North City Bus Stand → Sector 15 → Sector 22 → Kautilya Nagar → South Campus", 15.0),
        
        ("R-103", "East Corridor", "East Metro Station", "Tech Park Campus",
         "East Metro Station → IT Park → Industrial Area → Tech Park Campus", 12.5),
        
        ("R-104", "West Connect", "West End Terminal", "Main Campus - Vidya Vihar",
         "West End Terminal → Shopping Mall → Residential Area → Main Campus", 20.0),
    ]
    
    for route_num, name, start, end, stops, distance in routes_data:
        route, created = BusRoute.objects.get_or_create(
            route_number=route_num,
            defaults={
                "route_name": name,
                "start_point": start,
                "end_point": end,
                "stops": stops,
                "distance_km": distance
            }
        )
        
        # Add buses for each route
        if route_num == "R-101":
            Bus.objects.get_or_create(
                bus_number="CH-01-AB-1234",
                defaults={
                    "route": route,
                    "capacity": 60,
                    "driver_name": "Suresh Singh",
                    "driver_contact": "9988776655",
                    "morning_departure": time(6, 30),
                    "evening_departure": time(18, 0),
                    "status": "ACTIVE",
                    "registration_number": "UP12AB1234"
                }
            )
            Bus.objects.get_or_create(
                bus_number="CH-02-CD-5678",
                defaults={
                    "route": route,
                    "capacity": 55,
                    "driver_name": "Ramesh Patel",
                    "driver_contact": "9988776656",
                    "morning_departure": time(6, 45),
                    "evening_departure": time(18, 15),
                    "status": "ACTIVE",
                    "registration_number": "UP12CD5678"
                }
            )
            Bus.objects.get_or_create(
                bus_number="CH-03-EF-9012",
                defaults={
                    "route": route,
                    "capacity": 50,
                    "driver_name": "Mahesh Kumar",
                    "driver_contact": "9988776657",
                    "morning_departure": time(7, 0),
                    "evening_departure": time(18, 30),
                    "status": "ACTIVE",
                    "registration_number": "UP12EF9012"
                }
            )
        elif route_num == "R-102":
            Bus.objects.get_or_create(
                bus_number="CH-04-GH-3456",
                defaults={
                    "route": route,
                    "capacity": 50,
                    "driver_name": "Dinesh Yadav",
                    "driver_contact": "9988776658",
                    "morning_departure": time(7, 0),
                    "evening_departure": time(17, 45),
                    "status": "ACTIVE",
                    "registration_number": "UP12GH3456"
                }
            )
        else:
            Bus.objects.get_or_create(
                bus_number=f"CH-{route_num[-3:]}-XX-0001",
                defaults={
                    "route": route,
                    "capacity": 45,
                    "driver_name": f"Driver {route_num}",
                    "driver_contact": "9988776600",
                    "morning_departure": time(7, 15),
                    "evening_departure": time(17, 30),
                    "status": "ACTIVE",
                    "registration_number": f"UP12{route_num[-3:]}0001"
                }
            )
    
    print(f"✅ Created {BusRoute.objects.count()} Bus Routes with {Bus.objects.count()} Buses")
    
    # Create Admissions
    for course in Course.objects.all():
        if course.course_type == "UG":
            Admission.objects.get_or_create(
                course=course,
                defaults={
                    "status": "OPEN",
                    "last_date": date(2026, 6, 30),
                    "eligibility_criteria": "10+2 with minimum 60% marks in relevant subjects from recognized board",
                    "application_fee": 1500.00,
                    "required_documents": "10th Marksheet, 12th Marksheet, Transfer Certificate, Passport Photos, Character Certificate",
                    "admission_process": "Online application → Document verification → Counseling → Fee payment → Enrollment"
                }
            )
        else:
            Admission.objects.get_or_create(
                course=course,
                defaults={
                    "status": "OPEN",
                    "last_date": date(2026, 7, 15),
                    "eligibility_criteria": "Bachelor's degree with minimum 55% marks from recognized university",
                    "application_fee": 2000.00,
                    "required_documents": "10th, 12th, Graduation Marksheets, Transfer Certificate, Work Experience (if any)",
                    "admission_process": "Online application → Entrance test → Interview → Selection → Enrollment"
                }
            )
    
    print(f"✅ Created {Admission.objects.count()} Admission Records")
    
    print("\n" + "="*60)
    print("🏛️  CHANAKYA UNIVERSITY Database Setup Complete!")
    print("="*60)
    print(f"\n📊 Summary:")
    print(f"   • Campuses: {Campus.objects.count()}")
    print(f"   • Courses: {Course.objects.count()}")
    print(f"   • Faculty: {Faculty.objects.count()}")
    print(f"   • Rooms: {Room.objects.count()}")
    print(f"   • Bus Routes: {BusRoute.objects.count()}")
    print(f"   • Buses: {Bus.objects.count()}")
    print(f"   • Admissions Open: {Admission.objects.filter(status='OPEN').count()}")
    print("\n✅ You can now access the Chanakya University System!")
    print("   • Frontend: http://localhost:3000")
    print("   • Admin Panel: http://localhost:8000/admin")
    print("   • API: http://localhost:8000/api/")

if __name__ == "__main__":
    populate_data()