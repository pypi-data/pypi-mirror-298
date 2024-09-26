# Define the events and their probabilities
from datetime import datetime
from datetime import date, timedelta
import json
import random
from collections import deque
import threading
import time
from faker import Faker
from tqdm import tqdm

from fake.console import print_with_cursor_control
from fake.dates import add_secs, get_working_past_date
from fake.users import generate_user_id_normal

class CasesRows:
    _instance = None
    buffer = deque()
    batch_size = 0
    buffer_size = 0
    goal = 0
    count_generated = 0
    count_sent = 0
    buffer_pbar = None
    last_read_row = None       # Track the last read row or the beggining of the limit range
    last_delivered_row = None  # Track the last delivered row
    last_processed_row = None  # Track the last processed row
    reading_a_batch = False     # a semaphore to allow only one thread to read from database
    goal_row = 0

    # Define a set of common stop words
    stop_words = {
        "i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself", "yourselves",
        "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself", "they", "them",
        "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "these", "those", "am",
        "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do", "does", "did",
        "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while", "of", "at", "by",
        "for", "with", "about", "against", "between", "into", "through", "during", "before", "after", "above",
        "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", "again", "further", "then",
        "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each", "few", "more", "most",
        "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than", "too", "very", "s", "t",
        "can", "will", "just", "don", "should", "now"
    }
    
    stones = [
        "Agate", "Amber", "Amazonite", "Amethyst", "Apatite",
        "Aquamarine", "Aragonite", "Aventurine", "Bloodstone", "Citrine",
        "Diamond", "Emerald", "Fluorite", "Garnet", "Howlite",
        "Jasper", "Kyanite", "Labradorite", "Lapis Lazuli", "Malachite",
        "Moonstone", "Obsidian", "Onyx", "Opal", "Peridot",
        "Petrified Wood", "Pyrite", "Quartz", "Rhodochrosite", "Rhodonite",
        "Sapphire", "Sodalite", "Sunstone", "Tiger's Eye", "Topaz",
        "Tourmaline", "Turquoise", "Variscite", "Wax", "Zircon"
    ]
             
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(CasesRows, cls).__new__(cls)
        return cls._instance


    def init(self, goal, batch_size: int, buffer_size: int, pbar: tqdm):
        self.goal = goal
        self.batch_size = batch_size
        self.buffer_size = buffer_size
        self.buffer_pbar = pbar

    
    def init_fake_rows(self, goal, batch_size: int, buffer_size: int, pbar: tqdm):
        self.init(goal, batch_size, buffer_size, pbar)

        # Create a Faker instance
        self.fake = Faker()

        # set buffer
        self.buffer = deque(maxlen=self.buffer_size)
        for _ in range( int (self.buffer_size )):
            self.generate_a_batch()
           
    def set_last_case_number(self, last_case_number):
        self.last_case_number = last_case_number

    def get_next_case_number(self):
        self.last_case_number = self.last_case_number + 1
        return self.last_case_number

    def set_last_token_id(self, last_case_number):
        self.last_token_id = last_case_number

    def get_next_token_id(self):
        self.last_token_id = self.last_token_id + 1
        return self.last_token_id

    def set_last_request_id(self, last_request_id):
        self.last_request_id = last_request_id

    def get_next_request_id(self):
        self.last_request_id = self.last_request_id + 1
        return self.last_request_id

    def get_last_delivered_row(self):
        return self.last_delivered_row

    def get_last_processed_row(self):
        return self.last_processed_row

    def set_last_delivered_row(self, row):
        self.last_delivered_row = row

    def set_last_processed_row(self, row):
        self.last_processed_row = row

                
    def generate_a_batch(self):
        # generate one batch of fake rows and push into the queue
        # update the counters to make it available
        
        if self.count_generated >= self.goal: 
            return None
        
        this_batch_size = self.batch_size

        if self.count_generated + self.batch_size > self.goal:
            this_batch_size = max(0, self.goal - self.count_generated)
            
        batch = [self.generate_simple_case() for _ in range(this_batch_size)]
        
        self.count_generated += this_batch_size
        self.buffer.append(batch)
        self.buffer_pbar.n = len(self.buffer)
        self.buffer_pbar.refresh() 
        
        #dump_object_to_file(batch, True)
        print_with_cursor_control (f"cases generated: {self.count_generated:9,} ", 50, 11, 30)


    def get_batch_of_rows(self):
        # get the next available batch from the queue, 
        # if not available batch, waits until it is generated
        # do not wait, if no more batches to generate and return None
        # and then update the counters. 

        if not self.buffer and self.count_generated < self.goal :
            iterations = 0
            while self.count_generated < self.goal and len(self.buffer) == 0:
                #print_with_cursor_control (f"len self.buffer: {len(self.buffer):3,} iterations: {iterations}  ", 50, 13, 30)
                #print_with_cursor_control (f"self.count_generated {self.count_generated} < self.goal {self.goal}  ", 50, 14, 30)
                time.sleep(1.1) # wait 0.1 second until the the buffer refills
                iterations = iterations + 1

        # get a batch and update counters
        if self.buffer:
            batch = self.buffer.popleft()
        else:
            return None
 
        self.buffer_pbar.n = len(self.buffer)
        self.buffer_pbar.refresh() 
        self.count_sent += 1

        return batch

    def generate_batches_thread(self):
        # generate a batches in a separate thread
        
        # if all batchs were sent, just return
        if self.count_generated >= self.goal:
            return 
        
        continue_thread = True
        index = 0 
        while continue_thread:
            # wait until the buffer needs to be generated
            while len(self.buffer) >= self.buffer_size:
                time.sleep(0.5) # wait 0.5 second until previous batch is generated

            if self.count_generated + self.batch_size <= self.goal:
                self.generate_a_batch()

            continue_thread = self.count_generated + self.batch_size <= self.goal
            # print_with_cursor_control (f" continue_thread: {continue_thread}  {index} ", 50, 12, 30)
            index =+ 1


    def get_batch_of_read_rows(self):
        # get the next available batch from the queue of read rows, 
        # if not available batch, waits until it is readed
        # do not wait, if reach the goal and return None
        # and then update the counters. 
        if not self.buffer and self.last_read_row < self.goal_row :
            while not self.buffer :
                time.sleep(0.1) # wait 0.1 second until the the buffer refills
                #print ("wait\n")
                    
        # return None if no more batches
        if not self.buffer:
            self.buffer_pbar.n = 0
            self.buffer_pbar.refresh() 
            return None 
            
        # get a batch and update counters
        batch = self.buffer.popleft()

        # read the next batch in a separate thread
        if self.last_read_row < self.goal_row and self.reading_a_batch == False:
            len_buffer = 0 if self.buffer is None else len(self.buffer)
            # start the thread when buffer is less of 50% of capacity
            if len_buffer < self.buffer_size:
                thread = threading.Thread(target=self.read_a_batch)
                thread.start()

        self.buffer_pbar.n = len(self.buffer)
        self.buffer_pbar.refresh() 
        self.last_delivered_row += len(batch)

        #print (f"\033[1A         {self.last_delivered_row} {self.goal}     \033[1B", end='') 
        #tqdm.write (f"   {self.last_delivered_row} {self.goal}  ", end='') 
        return batch
    

    def read_a_batch(self):
        # read a batch from database, executes only one tread, no parallelism
        self.reading_a_batch = True
        
        # Logic to read the next batch of rows from the table
        time.sleep(0.5)
        this_buffer_size = self.buffer_size
        pending_rows = self.goal_row - self.last_read_row 
        if  pending_rows < self.buffer_size * self.batch_size:
            this_buffer_size, last_batch_size = divmod (pending_rows, self.batch_size)

        for i in range(this_buffer_size):
            batch = []
            for i in range(self.batch_size):
                batch.append ( {"n":i*100, "data": "ABC"} )
            
            self.buffer.append(batch)                
        
        self.last_read_row += this_buffer_size * self.batch_size
        
        if this_buffer_size != self.buffer_size:
            last_batch = []
            for i in range(last_batch_size):
                last_batch.append ( {"n":i*100, "data": "last"} )
            
            self.buffer.append(last_batch)                
            self.last_read_row += 1 * last_batch_size

        self.buffer_pbar.n = len(self.buffer)
        self.buffer_pbar.refresh() 
        self.reading_a_batch = False
        
        
    def get_random_status(self):
        return random.choice(["in_progress", "completed"])

    def get_random_process_id(self):
        return random.choice([23, 51])

   
    def get_random_travel_processes(self):
        processes = random.choice([
            [
                {'id': 23, 'name': 'Business Travel'}
            ], 
            [
                {'id': 23, 'name': 'Business Travel'},
                {'id': 25, 'name': 'Subprocess Business Travel'}
            ], 
            [
                {'id': 23, 'name': 'Business Travel'},
                {'id': 24, 'name': 'Parallel of Travel'},
                {'id': 25, 'name': 'Subprocess of Business Travel'}
            ]
        ])
        return processes

    # process_requests   `status` enum('DRAFT','ACTIVE','COMPLETED','ERROR','CANCELED') COLLATE utf8mb4_unicode_ci NOT NULL,
    # process_request_tokens  `status` enum('ACTIVE','FAILING','COMPLETED','CLOSED','EVENT_CATCH','TRIGGERED','INCOMING') COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'ACTIVE',
 
    def get_random_travel_tokens(self, processes: any, case_title: str, case_number: int, case_created_at: datetime, case_status: str):

        # assign id for the requests of this case
        requests = []
        for process in processes:
            requests.append({
                'id' : self.get_next_request_id(),
                'process_id': process['id'],
                'parent_request_id': 0 if process['id'] == processes[0]['id'] else processes[0]['id'], # todo: improve 
                'status': 'ACTIVE', #DRAFT','ACTIVE','COMPLETED','ERROR','CANCELED'
                'name': f"{ process['name'] } {self.last_request_id}", 
                'case_title' : case_title,
                'case_number' : case_number
            })
            
        
        bpmn_tasks = [
            { "task_id": "node_12345", "task_name": "Request Travel Approval" },
            { "task_id": "node_67890", "task_name": "Book Flights" },
            { "task_id": "node_23456", "task_name": "Reserve Accommodation" },
            { "task_id": "node_78901", "task_name": "Arrange Ground Transportation" },
            { "task_id": "node_34567", "task_name": "Prepare Travel Itinerary" },
            { "task_id": "node_89012", "task_name": "Submit Expense Report" },
            { "task_id": "node_45678", "task_name": "Review Travel Policies" },
            { "task_id": "node_90123", "task_name": "Notify Team of Travel Plans" },
            { "task_id": "node_56789", "task_name": "Conduct Pre-Travel Briefing" },
            { "task_id": "node_11223", "task_name": "Collect Feedback Post-Travel" }
        ]
        
        # assign default user for these tasks for this case
        for bpmn_task in bpmn_tasks:
            bpmn_task['user_id'] = generate_user_id_normal(5000) 

        # create an array of tokens  (process_request_tokens)  
        tokens = []    
        current_request = requests[0]
        
        tokens_len = random.randint(1, len(processes) * 10)
        current_case_date = case_created_at  # use this variable to maintain some logic in dates, every task is after this one.
            
        for i in range(0, tokens_len):
            task = random.choice(bpmn_tasks)
            
            # all tokens are completed by default except the last one
            is_active = i == tokens_len -1
            # But if the case is completed, the last token also completed
            if is_active and case_status == 'completed':
                is_active = False
            status = 'ACTIVE' if is_active else 'COMPLETED'
            created_at = current_case_date
            initiated_at = add_secs( current_case_date, 1, 100) 
            completed_at = None if is_active else add_secs( current_case_date, 100, 5*86_400) # 1 day = 86_400
            updated_at = initiated_at if is_active else completed_at
            current_case_date = add_secs(updated_at, 1000, 10000)
            tokens.append({
                'id': self.get_next_token_id(), 
                'user_id' : random.choice( [task['user_id'], generate_user_id_normal(5000) ]),
                'process_id': current_request['process_id'],     
                'process_request_id': current_request['id'],     
                'element_id' : task['task_id'],
                'element_name' : task['task_name'],
                'status' : status, # 'ACTIVE','FAILING','COMPLETED','CLOSED','EVENT_CATCH','TRIGGERED','INCOMING'
                'created_at' : created_at,
                'initiated_at' : initiated_at,
                'updated_at' : updated_at,
                'completed_at' : completed_at,
            })
            
        
            # algorithm to select in which process/subprocess will be next request
            # the algoritm started with the main process
            is_main_process = current_request['process_id'] == requests[0]['process_id']
        
            if not is_main_process or random.random() > 0.3:
                random_index = random.randint(0, len(requests) - 1)
                current_request = requests[random_index]
                
        #for t in tokens:
        #    print("---")    
        #    print (t)
        custom_data = self.generate_travel_custom_data(case_title, case_number, case_created_at, tokens)
        return requests, tokens, custom_data 

    def generate_travel_custom_data(self, case_title: str, case_number: int, case_created_at: datetime, tokens: any):
        travel_fields = {
            "Request Travel Approval": ["destination", "travel_dates", "cost_item1", "cost_item3"],
            "Book Flights": ["flight_number", "ticket_price", "departure_date"],
            "Reserve Accommodation": ["hotel_name", "room_type", "check_in_date"],
            "Arrange Ground Transportation": ["transportation_type", "travel_mode", "ride_distance"],
            "Prepare Travel Itinerary": ["destination", "itinerary", "travel_dates"],
            "Submit Expense Report": ["expense_report", "invoice_number", "vendor_name"],
            "Review Travel Policies": ["travel_policy", "travel_guidelines", "travel_procedures"],
            "Notify Team of Travel Plans": ["travel_policy", "team_members", "travel_dates"],
            "Conduct Pre-Travel Briefing": ["pre-travel_briefing", "team_members", "travel_dates"],
            "Collect Feedback Post-Travel": ["feedback_form", "team_members", "travel_evaluation"]
        }

        random_values = {
            "case_number": case_number,
            "case_title": case_title,
            "destination": self.fake.city(),
            "flight_number": self.fake.numerify(text="#####"),
            "ticket_price": self.fake.numerify(text="!###.##"),
            "cost_item1": self.fake.numerify(text="!###.##"),
            "cost_item3": self.fake.numerify(text="!###.##"),
            "created_at": datetime.strptime(case_created_at, "%Y-%m-%d %H:%M:%S"),
            "departure_date": self.fake.date_time_between(start_date= datetime.strptime(case_created_at, "%Y-%m-%d %H:%M:%S")).strftime("%Y-%m-%d %H:%M:%S"),
            "hotel_name": self.fake.company(),
            "room_type": random.choice(['Single', 'Double', 'Twin', 'Deluxe', 'Suite']),
            "transportation_type": random.choice([ 'Van', 'Bus', 'Train', 'Flight', 'Car', "Motorcycle", "Taxi"]),
            "travel_mode": random.choice([ 'Business', 'Tourism', 'Mixed', 'Enterprise', 'Conference']),
            "ride_distance": self.fake.numerify(text="####"),
            "itinerary": self.fake.sentence(),
            "travel_dates": self.fake.future_datetime(end_date=datetime.strptime("2050-01-01 00:00:00", "%Y-%m-%d %H:%M:%S")).strftime("%Y-%m-%d %H:%M:%S"),
            "check_in_date": self.fake.future_datetime(end_date=datetime.strptime("2050-01-01 00:00:00", "%Y-%m-%d %H:%M:%S")).strftime("%Y-%m-%d %H:%M:%S"),
            "expense_report": self.fake.pyfloat(),
            "invoice_number": self.fake.numerify(text="###########"),
            "vendor_name": self.fake.company(),
            "travel_policy": random.choice([ 'policy 1', 'policy 2', 'policy 3', 'policy 4', 'policy 5']),
            "travel_guidelines": self.fake.sentence(),
            "travel_procedures": self.fake.sentence(),
            "travel_notification": self.fake.sentence(),
            "team_members": self.fake.name(),
            "travel_objectives": self.fake.sentence(),
            "pre-travel_briefing": self.fake.sentence(),
            "feedback_form": self.fake.sentence(),
            "participants": self.fake.name(),
            "travel_evaluation": self.fake.sentence()
        }

        generic_fields = {"generic": ["case_number"]}
  
        fields = []
        fields.extend(generic_fields['generic'])

        #fields['case_title'] = case_title
        for token in tokens:
            element_name = token['element_name']
            if element_name in travel_fields:
                fields.extend(travel_fields[element_name])

        result = {field: random_values[field] for field in fields}
        return result
    
    def get_travel_data(self, case_number: int, case_created_at: datetime, case_status: str):
        city = self.fake.city()
        country = self.fake.country()

        case_title = f'Travel to {city} in {country}'
        case_title_formatted = f'Travel to <b>{city}</b> in <i>{country}</i>'
        processes = self.get_random_travel_processes()
        requests, tokens, custom_data = self.get_random_travel_tokens(processes, case_title, case_number, case_created_at, case_status)

        
        return case_title, case_title_formatted, processes, requests, tokens, custom_data

    # crd data process
    
    def get_random_stone(self):
        return random.choice(self.stones)

    def get_crm_data(self, case_number: int, case_created_at: datetime, case_status: str):
        company = self.fake.company()
        product = f"{self.get_random_stone()} {self.fake.color()}"
        client = self.fake.first_name()
        sub_crm = random.choice(["lead", "nurturing", "opportunity", "retention"])
        if sub_crm == "lead":
            case_title = f'Lead generation from {company} and product {product}'
            case_title_formatted = f'Lead generation from <b>{company}</b> and product <i>{product}</i>'

        if sub_crm == "nurturing":
            case_title = f'Encourage grow of {company} contact {client}'
            case_title_formatted = f'Encourage grow of <b>{company}</b> contact <i>{client}</i>'

        if sub_crm == "opportunity":
            case_title = f'Oppportunity in {company} contact {client}'
            case_title_formatted = f'Opportunity in <b>{company}</b> contact <i>{client}</i>'

        if sub_crm == "retention":
            case_title = f'{company} retention'
            case_title_formatted = f'<b>{company}</b> retention'

        processes = self.get_random_crm_processes()
        requests, tokens, custom_data = self.get_random_crm_tokens(processes, case_title, case_number, case_created_at, case_status)

        
        return case_title, case_title_formatted, processes, requests, tokens, custom_data
        
    def get_random_crm_tokens(self, processes: any, case_title: str, case_number: int, case_created_at: datetime, case_status: str):

        # assign id for the requests of this case
        requests = []
        for process in processes:
            requests.append({
                'id' : self.get_next_request_id(),
                'process_id': process['id'],
                'parent_request_id': 0 if process['id'] == processes[0]['id'] else processes[0]['id'], # todo: improve 
                'status': 'ACTIVE',  #,'ACTIVE','COMPLETED','ERROR','CANCELED'
                'name': f"{ process['name'] } {self.last_request_id}", 
                'case_title' : case_title,
                'case_number' : case_number
            })
            
        
        bpmn_tasks = [
            { "task_id": "node_11345", "task_name": "Capture Lead Information" },
            { "task_id": "node_11890", "task_name": "Verify Lead Data" },
            { "task_id": "node_11456", "task_name": "Assign Lead Owner" },
            { "task_id": "node_11901", "task_name": "Send Welcome Email" },
            { "task_id": "node_11567", "task_name": "Schedule Follow up call" },
            { "task_id": "node_11012", "task_name": "Add Lead to Marketing Campaigns" },
            { "task_id": "node_11678", "task_name": "Quality Opportunities" },
            { "task_id": "node_11123", "task_name": "Assign Opportunity Owner" },
            { "task_id": "node_11789", "task_name": "Create Sales Forecast" },
            { "task_id": "node_11931", "task_name": "Prepare Sales Material" },
            { "task_id": "node_11932", "task_name": "Schedule Meetings and Calls" },
            { "task_id": "node_11933", "task_name": "Conduct Needs Analysis" },
            { "task_id": "node_11934", "task_name": "Onboard New Customers" },
            { "task_id": "node_11935", "task_name": "Schedule Regular Reviews" },
            { "task_id": "node_11936", "task_name": "Manage customer Feedback" },
            { "task_id": "node_11937", "task_name": "Create Sales Order" },
            { "task_id": "node_11938", "task_name": "Process Payment" },
            { "task_id": "node_11939", "task_name": "Generate Invoice" },
            { "task_id": "node_11940", "task_name": "Conduct Post Sale Survey" },
            { "task_id": "node_11941", "task_name": "Close Opportunity" }
        ]
        
        # assign default user for these tasks for this case
        for bpmn_task in bpmn_tasks:
            bpmn_task['user_id'] = generate_user_id_normal(5000) 

        # create an array of tokens  (process_request_tokens)  
        tokens = []    
        current_request = requests[0]
        
        tokens_len = random.randint(1, len(processes) * 10)
        current_case_date = case_created_at  # use this variable to maintain some logic in dates, every task is after this one.
            
        for i in range(0, tokens_len):
            task = random.choice(bpmn_tasks)
            
            # all tokens are completed by default except the last one
            is_active = i == tokens_len -1
            # But if the case is completed, the last token also completed
            if is_active and case_status == 'completed':
                is_active = False
            status = 'ACTIVE' if is_active else 'COMPLETED'
            created_at = current_case_date
            initiated_at = add_secs( current_case_date, 1, 100) 
            completed_at = None if is_active else add_secs( current_case_date, 100, 5*86_400) # 1 day = 86_400
            updated_at = initiated_at if is_active else completed_at
            current_case_date = add_secs(updated_at, 1000, 10000)
            tokens.append({
                'id': self.get_next_token_id(), 
                'user_id' : random.choice( [task['user_id'], generate_user_id_normal(5000) ]),
                'process_id': current_request['process_id'],     
                'process_request_id': current_request['id'],     
                'element_id' : task['task_id'],
                'element_name' : task['task_name'],
                'status' : status, # 'ACTIVE','FAILING','COMPLETED','CLOSED','EVENT_CATCH','TRIGGERED','INCOMING'
                'created_at' : created_at,
                'initiated_at' : initiated_at,
                'updated_at' : updated_at,
                'completed_at' : completed_at,
            })
            
        
            # algorithm to select in which process/subprocess will be next request
            # the algoritm started with the main process
            is_main_process = current_request['process_id'] == requests[0]['process_id']
        
            if not is_main_process or random.random() > 0.3:
                random_index = random.randint(0, len(requests) - 1)
                current_request = requests[random_index]
                
        #for t in tokens:
        #    print("---")    
        #    print (t)
        custom_data = self.generate_crm_custom_data(case_title, case_number, case_created_at, tokens)
        return requests, tokens, custom_data 

    def generate_crm_custom_data(self, case_title: str, case_number: int, case_created_at: datetime, tokens: any):
        crm_fields = {
            "capture": ["first_name", "last_name", "email", "phone", "company"],
            "verify": ["contact_verified", "lead_status"],
            "assign": ["salesperson", "team_name"],
            "nurturing": ["subject_line", "body_text", "date_welcome", "lead_owner"],
            "opportunity": ["budget", "decision_making", "salesperson", "team_name"],
            "sales": ["product", "customer_pain_points", "business_requirements", "customer_name", "onboarding_date"],
            "post": ["satisfaction_rate", "comments", "close_reason", "invoice_number"]
        }

        random_values = {
            "case_number": case_number,
            "case_title": case_title,
            "first_name": self.fake.first_name(),
            "last_name": self.fake.last_name(),
            "email": self.fake.email(),
            "phone": self.fake.numerify(text="!###-###-####"),
            "company": self.fake.company(),
            "contact_verified": random.choice(['Yes', 'No', 'Pending']),
            "lead_status": random.choice(['active', 'inactive', 'paused', 'dead']),
            "salesperson": self.fake.first_name_female(),
            "team_name": random.choice(["Aurora Squad", "Velocity Team", "Pioneers Group", "Apex Club", "Nexus Force", "Storm Chasers", "Spectrum Team",    "Voyager Crew", "Flashpoint Unit", "Horizon Hunters"]),
            "subject_line": self.fake.sentence(),
            "body_text": self.fake.sentence(),
            "date_welcome": self.fake.date_time_between(start_date= datetime.strptime(case_created_at, "%Y-%m-%d %H:%M:%S")).strftime("%Y-%m-%d %H:%M:%S"),
            "lead_owner": self.fake.first_name_female(),
            "budget": self.fake.numerify(text="####00"),
            "decision_making": self.fake.sentence(),
            "product": self.get_random_stone(),
            "customer_pain_points": self.fake.sentence(),
            "business_requirements": self.fake.sentence(),
            "customer_name": self.fake.first_name_male(),
            "onboarding_date": datetime.strptime(case_created_at, "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d %H:%M:%S"),
            "satisfaction_rate": random.choice(['*', '**', '***', '****', '*****']),
            "comments": self.fake.sentence(),
            "close_reason": self.fake.sentence(),
            "invoice_number": self.fake.numerify(text="###########")
        }

        generic_fields = {"generic": ["case_number"]}
  
        fields = []
        fields.extend(generic_fields['generic'])

        for crm_field in crm_fields:
            if random.choice([1,2,3,4])  > 1:
                fields.extend(crm_fields[crm_field])

        result = {field: random_values[field] for field in fields}
        
        return result


    def get_random_crm_processes(self):
        processes = random.choice([
            [
                {'id': 51, 'name': 'CRM Process'}
            ], 
            [
                {'id': 51, 'name': 'CRM Process'},
                {'id': 52, 'name': 'Update CRM system'}
            ]
        ])
        return processes
        
        
    # generate a fake Case
    def generate_simple_case(self):
        case_number = self.get_next_case_number() 
        case_status = self.get_random_status() 
        main_process_id = self.get_random_process_id() 
        case_created_at = get_working_past_date(1000, 1)

        simple_case = {}
        simple_case['case_number']  = case_number 
        simple_case['case_status']  = case_status 

        if main_process_id == 23:
            case_title, case_title_formatted, processes, requests, tokens, custom_data = self.get_travel_data(case_number, case_created_at, case_status) 
        
        if main_process_id == 51:
            case_title, case_title_formatted, processes, requests, tokens, custom_data = self.get_crm_data(case_number, case_created_at, case_status) 
        
        simple_case['case_title']   = case_title
        simple_case['case_title_formatted'] = case_title_formatted
        simple_case['processes']    = processes
        simple_case['requests']     = requests
        simple_case['tokens']       = tokens
            
        case_created_at = None if len(tokens) == 0 else tokens[0]['created_at']            
        case_initiated_at = None if len(tokens) == 0 else tokens[0]['initiated_at']            
        case_updated_at = None if len(tokens) == 0 else tokens[-1]['updated_at']            
        case_completed_at = None if len(tokens) == 0 else tokens[-1]['completed_at']            
      
        simple_case['created_at']   = case_created_at
        simple_case['initiated_at'] = case_initiated_at
        simple_case['updated_at']   = case_completed_at
        simple_case['completed_at'] = case_updated_at
        keywords =  f"{ self.get_subsets_with_prefix(case_number) } {self.remove_stop_words(case_title)} {self.extract_keywords(custom_data)}"
        simple_case['keywords'] = keywords        
        simple_case['custom_data'] = custom_data
        return simple_case


    def get_subsets_with_prefix_old(self, number):
        # Convert the number to a string to easily access its digits
        num_str = str(number)
        
        # Initialize an empty list to store the subsets
        subsets = []
        subsets.append(num_str)
        
        # Loop through the string to get all subsets of length 3
        for i in range(len(num_str) - 2):
            subset = num_str[i:i+3]
            subsets.append(subset)
        
        # Prefix each subset with "cn_"
        prefixed_subsets = [f"cn_{subset}" for subset in subsets]
        
        # Join the prefixed subsets into a single string
        result = ' '.join(prefixed_subsets)
        
        return result
        
    def get_subsets_with_prefix(self, number):
        # Convert the number to a string to easily access its digits
        num_str = str(number)
        
        # Initialize an empty list to store the subsets
        subsets = []
        subsets.append(num_str)
        
        # Loop through the string to get all subsets of decreasing lengths
        for i in range(1, len(num_str)):
            subset = num_str[i:]  # Get the substring starting from index i to the end
            if len(subset) > 2:
                subsets.append(subset)
        
        # Prefix each subset with "cn_"
        prefixed_subsets = [f"cn_{subset}" for subset in subsets]
        
        # Join the prefixed subsets into a single string
        result = ' '.join(prefixed_subsets)
        
        return result    
    
    def remove_stop_words(self, text: str) -> str:


        # Split the text into words
        words = text.split()

        # Filter out the stop words
        filtered_words = [word for word in words if word.lower() not in self.stop_words]

        # Join the remaining words back into a string
        return ' '.join(filtered_words)    
    
    def extract_keywords(self, json_data: any):
        try:
            # Initialize an empty list to hold the keywords
            keywords = []
            
            # Iterate through the key-value pairs in the JSON data
            for key, value in json_data.items():
                # Check if the value is a string and has more than 3 letters
                if isinstance(value, str) and len(value) > 3:
                    if value not in self.stop_words:
                        # Append the lowercase version of the value to the keywords list
                        keywords.append(value.lower())
            
            # Filter keywords to include only those less than 15 characters long
            filtered_keywords = [kw for kw in keywords if len(kw) <= 15]

            # Get the top 15 unique keywords
            top_keywords = list(set(filtered_keywords))[:15]
            
            # Join the keywords into a single string separated by spaces
            keywords_string = ' '.join(top_keywords)
            return keywords_string    
        except (json.JSONDecodeError, TypeError) as e:
            # Handle specific exceptions related to JSON parsing
            print (str(e))
            exit(1)
            return ""
        except Exception as e:
            # Handle any other exceptions
            print (str(e))
            exit(1)
            return ""
                
    
    
    