import openai
from openai import error
import os

a1 = "sk-QMI14RMwDxqHuBQq"
a2 = "3qb1T3BlbkFJ4Jww1"
a3 = "9xS5FKI1wcxjkIi"
openai.api_key = a1+a2+a3

def start_conversation():
    try:
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt="User: Hello\nAI:",
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.5,
        )
        return response.choices[0].text
    except error.APIConnectionError as e:
        # Handle the APIConnectionError exception here
        print("Error communicating with OpenAI:", e)
        return None

def get_ai_response(conversation_history, user_input):
    prompt = f"User: {user_input}\nAI: {conversation_history}"
    try:
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.5,
        )
        return response.choices[0].text
    except error.APIConnectionError as e:
        # Handle the APIConnectionError exception here
        print("Error communicating with OpenAI:", e)
        return None

def call_until_return_response(func, history, input):
    result = func(history,input)
    while not result:
        result = func(history,input)
    return result

def check_user_input(user_input):
    health_keywords = ['covid','coronavirus','health', 'medicine', 'doctor', 'hospital', 'sickness', 'symptom', 'treatment', 'disease', 'injury', 'illness',"abdomen",
                       "abdominal","acupuncture","ADD","addiction","ADHD","adolescent","epilepsy","eye","family","feet","bipolar","blood","bone","brain","breast",
                       "adult","alcohol","allergies","alternative","Alzheimers","anatomy","anemia","anesthesia","anxiety","arthritis","asthma","autism","back","bacteria",
                       "cancer","cardiac","cardiology","caregiver","cataract","cell","child","chiropractic","chronic","clinic","colon","community","concussion","cosmetic",
                       "counseling","dementia","dental","depression","thrombosis","thyroid","treatment","urology","vaccine","veterinary","vision","weight","wellness","women","yoga"
                       "dermatology","diabetes","diagnosis","diet","digestion","disability","doctor","drug","ear","eating","emergency","endocrine","endocrinology","ENT",
                       "fitness","flu","food","gastrointestinal","genetic","geriatric","gynecology","health","heart","herpes","hip","HIV","homeopathy","hospice",
                       "hospital","hypertension","immunology","infectious","infertility","injury","insurance","internal","knee","laser","lung","lymphoma",
                       "medical","medicine","menopause","mental","migraine","mobility","MRI","neonatal","neurology","nutrition","obesity","obstetrics","oncology",
                       "ophthalmology","optometry","oral","orthodontics","orthopedic","osteoporosis","ovarian","pain","palliative","pediatric","pharmacy",
                       "physical","plastic","podiatry","pregnancy","psychiatry","psychology","radiation","radiology","rehabilitation","reproductive","respiratory",
                       "rheumatoid","rheumatology","safety","senior","sexual","sickle","skin","sleep","speech","spinal","sports","stroke","surgery","therapist","therapy",
                       "water","compound","chemical","diseases","cure","COVID-19", "Vaccination", "Coronavirus", "Flu", "Cancer", "Diabetes", "Heart disease", "HIV/AIDS", 
                       "Alzheimer's disease", "Asthma", "Arthritis", "Depression", "Obesity", "Migraine", "High blood pressure", "Stroke", "Pregnancy", "Menopause", "Erectile dysfunction", 
                       "Cholesterol", "Acne", "Allergies", "Anemia", "Anxiety", "Back pain", "Bipolar disorder", "Blood pressure", "Bronchitis", "Celiac disease", "Chickenpox", "Chlamydia", 
                       "Chronic fatigue syndrome", "Cold sores", "Colitis", "Conjunctivitis", "Constipation", "COPD", "Crohn's disease", "Cystic fibrosis", "Dementia", "Dental health", "Dermatitis", 
                       "Diarrhea", "Digestive system", "Eating disorders", "Eczema", "Endometriosis", "Epilepsy", "Fibromyalgia", "Gallstones", "Gout", "Headaches", "Hemorrhoids", "Hepatitis", "Herpes", 
                       "Hyperthyroidism", "Hypothyroidism", "Incontinence", "Influenza", "Insomnia", "Irritable bowel syndrome","IBS","Jaundice", "Kidney disease", "Lactose intolerance", "Leukemia", 
                       "Lupus", "Lyme disease", "Macular degeneration", "Malaria", "Melanoma", "Menstrual cycle", "Mesothelioma", "Mumps", "Multiple sclerosis","MS", "Myasthenia gravis", "Nasal congestion",
                       "Neck pain", "Nephrotic syndrome", "Neuropathy", "Osteoporosis", "Ovarian cancer", "Overactive bladder", "Pancreatic cancer", "Panic attacks", "Parkinson's disease", "Pneumonia", "Polio", 
                       "Polycystic ovary syndrome","PCOS","Psoriasis", "Raynaud's disease", "Restless leg syndrome", "Rheumatoid arthritis", "Rosacea", "Sarcoidosis", "Scabies", "Schizophrenia", "Sciatica", 
                       "Scleroderma", "Shingles", "Sinusitis", "Sleep apnea", "Sore throat", "Stomach ulcers", "Stress", "Sunburn", "Swine flu", "Syphilis", "Tinnitus", "Tonsillitis", "Tuberculosis","TB", "Ulcerative colitis", 
                       "Urinary tract infection","UTI", "Varicose veins", "Vertigo", "Vitamin deficiency", "Warts", "West Nile virus", "Whooping cough", "Yeast infection", "Zika virus", "Abdominal pain", 
                       "Acute respiratory distress syndrome","ARDS", "Adenoids", "ADHD", "Adrenal gland disorders", "Alcoholism", "Allergic","pain","syndrome","ache","infection"
                       ]
    is_health_related = any(keyword in user_input.lower() for keyword in health_keywords)
    if is_health_related:
        return True
    else:
        return False
