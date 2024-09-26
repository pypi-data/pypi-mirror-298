import random
import numpy as np

def generate_user_id_pareto(max_users: int):
    """
    Generates a user_id based on a Pareto distribution.
    80% of the rows will be assigned to 20% of the users.

    Returns:
    int: A user_id.
    """
    # Pareto distribution parameters
    shape, mode = 10, 1


    while True: 
        # Generate a random number from the Pareto distribution
        pareto_num = (np.random.pareto(shape) + 1) * max_users

        # Scale the number to the range of user_ids
        #user_id = int(pareto_num * max_users / (mode + shape))
        user_id = int(pareto_num )
        print (f"{user_id:7} {pareto_num}")   
        if 1 <= user_id <= max_users:
            return user_id  


def generate_user_id_normal(max_users: int):
    """
    Generates a user_id based on a normal distribution.
    The majority of the user_ids will be around the mean.

    Returns:
    int: A user_id.
    """
    # Normal distribution parameters
    #mean, std_dev = 0, 0.1
    #mean, std_dev = 0, 0.15
    mean, std_dev = 0, 0.1

    while True: 
        # Generate a random number from the normal distribution
        normal_num = np.random.normal(mean, std_dev) + 0.5

        # Ensure the user_id is within the valid range
        user_id = int(normal_num * max_users * 2.1)  # halt of the bell and little shift to the right

        if max_users < user_id < max_users * 1.1 :
            user_id = int(max_users - (user_id - max_users) * (1+random.random())*1.8)
            
        if 1 <= user_id <= max_users:
            return user_id        


def get_user_name(user_id: int):
    # return the same name for a user_id
    
    popular_names = [
        "Liam",
        "Noah",
        "Oliver",
        "Elijah",
        "James",
        "William",
        "Benjamin",
        "Lucas",
        "Henry",
        "Alexander",
        "Mason",
        "Michael",
        "Ethan",
        "Daniel",
        "Jacob",
        "Logan",
        "Jackson",
        "Sebastian",
        "Aiden",
        "Matthew",
        "Samuel",
        "David",
        "Joseph",
        "Carter",
        "Owen",
        "Wyatt",
        "John",
        "Jack",
        "Luke",
        "Jayden",
        "Dylan",
        "Grayson",
        "Levi",
        "Isaac",
        "Gabriel",
        "Julian",
        "Mateo",
        "Anthony",
        "Jaxon",
        "Lincoln",
        "Joshua",
        "Christopher",
        "Andrew",
        "Theodore",
        "Caleb",
        "Ryan",
        "Asher",
        "Nathan",
        "Thomas",
        "Leo",
        "Isaiah",
        "Charles",
        "Josiah",
        "Hudson",
        "Christian",
        "Hunter",
        "Connor",
        "Landon",
        "Eli",
        "Adrian",
        "Jonathan",
        "Nolan",
        "Jeremiah",
        "Easton",
        "Ezekiel",
        "Colton",
        "Silas",
        "Gavin",
        "Chase",
        "Zachary",
        "Ryder",
        "Diego",
        "Jax",
        "Emmett",
        "Kaden",
        "Riley",
        "Robert",
        "Tyler",
        "Austin",
        "Jordan",
        "Cooper",
        "Xavier",
        "Jesse",
        "Luca",
        "Max",
        "Vincent",
        "Zane",
        "Liam",
        "Maverick",
        "Sawyer",
        "Graham",
        "Jude",
        "Karter",
        "Kylan",
        "Ronan",
        "Tobias",
        "Wesley",
        "Kendrick",
        "Dante",
        "Khalil",
        "Kendall",
        "Rafael",
        "Quinn",
        "Santiago",
        "Kairo",
        "Kason",
        "Kellan",
        "Koa",
        "Kye"
    ]

    last_names = [
        "Smith",
        "Johnson",
        "Williams",
        "Jones",
        "Brown",
        "Davis",
        "Miller",
        "Wilson",
        "Moore",
        "Taylor",
        "Anderson",
        "Thomas",
        "Jackson",
        "White",
        "Harris",
        "Martin",
        "Thompson",
        "Garcia",
        "Martinez",
        "Robinson",
        "Clark",
        "Rodriguez",
        "Lewis",
        "Lee",
        "Walker",
        "Hall",
        "Allen",
        "Young",
        "Hernandez",
        "King",
        "Wright",
        "Lopez",
        "Hill",
        "Scott",
        "Green",
        "Adams",
        "Baker",
        "Gonzalez",
        "Nelson",
        "Carter",
        "Mitchell",
        "Perez",
        "Roberts",
        "Turner",
        "Phillips",
        "Campbell",
        "Parker",
        "Evans",
        "Edwards",
        "Collins",
        "Stewart",
        "Sanchez",
        "Morris",
        "Rogers",
        "Reed",
        "Cook",
        "Morgan",
        "Bell",
        "Murphy",
        "Bailey",
        "Rivera",
        "Cooper",
        "Richardson",
        "Cox",
        "Howard",
        "Ward",
        "Torres",
        "Peterson",
        "Gray",
        "Ramirez",
        "James",
        "Watson",
        "Brooks",
        "Kelly",
        "Sanders",
        "Price",
        "Bennett",
        "Wood",
        "Barnes",
        "Ross",
        "Henderson",
        "Coleman",
        "Jenkins",
        "Perry",
        "Powell",
        "Long",
        "Patterson",
        "Hughes",
        "Flores",
        "Washington",
        "Butler",
        "Simmons",
        "Foster",
        "Gonzales",
        "Bryant",
        "Alexander",
        "Russell",
        "Griffin",
        "Diaz",
        "Hayes"
    ]
    
    first_name = popular_names[ user_id % len(popular_names)]
    last_name = last_names[ user_id % len(last_names)]
    name_set = int(user_id / (len(popular_names) * len(last_names))) 
    
    if name_set == 0:
        return f"{first_name} {last_name}"
    else:
        return f"{first_name} {chr(name_set+64)}. {last_name}"
    
    
def  get_user_job_title(user_id: int):
    job_titles = [
        "CEO", 
        "CTO", 
        "CFO", 
        "Marketing Manager", 
        "Sales Director", 
        "IT Manager", 
        "HR Manager", 
        "Accountant", 
        "Financial Analyst", 
        "Data Scientist", 
        "Software Engineer", 
        "Product Manager", 
        "DevOps Engineer", 
        "Network Administrator", 
        "Customer Service Representative", 
        "Operations Manager", 
        "Supply Chain Manager", 
        "Procurement Specialist", 
        "Inventory Manager", 
        "Logistics Coordinator", 
        "Project Manager", 
        "Business Analyst", 
        "Systems Administrator", 
        "Database Administrator", 
        "Web Developer", 
        "UX Designer", 
        "Marketing Coordinator", 
        "Public Relations Manager", 
        "Graphic Designer", 
        "Social Media Manager", 
        "Event Planner", 
        "Executive Assistant", 
        "Personal Assistant", 
        "Receptionist", 
        "Office Manager", 
        "Administrative Assistant", 
        "Data Entry Clerk", 
        "Customer Support Specialist", 
        "Help Desk Technician", 
        "Network Engineer", 
        "Cyber Security Specialist", 
        "Cloud Architect", 
        "Artificial Intelligence Engineer", 
        "Machine Learning Engineer", 
        "Full Stack Developer", 
        "Front End Developer", 
        "Back End Developer", 
        "Quality Assurance Tester", 
        "Test Automation Engineer", 
        "Digital Marketing Manager", 
        "SEO Specialist", 
        "Content Writer", 
        "Technical Writer", 
        "UX Researcher", 
        "User Experience Designer", 
        "Product Designer", 
        "Business Development Manager", 
        "Sales Representative", 
        "Account Manager", 
        "Customer Success Manager", 
        "Recruiter", 
        "Talent Acquisition Specialist", 
        "Hiring Manager", 
        "Executive Recruiter"
        ]
    job_title = job_titles[ user_id % len(job_titles)]
    return job_title
        
def get_user_avatar(user_id: int):
    return f"https://cdn.processmaker.com/users/000{user_id}"
        