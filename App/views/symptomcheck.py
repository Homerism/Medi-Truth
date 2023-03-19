from flask import Blueprint, render_template, request, flash
from flask_login import login_required

symptom_views = Blueprint('symptom_views', __name__, template_folder='../templates')

@symptom_views.route('/symptoms', methods=['GET'])
@login_required
def index():
    return render_template('results.html')

@symptom_views.route('/symptoms', methods=['POST'])
@login_required
def get_symptom_diagnosis():
    symptom_to_condition = {
        "fever": ["flu", "COVID-19", "pneumonia",'Influenza', 'Pneumonia', 'Malaria'],
        "cough": ["common cold", "bronchitis", "COVID-19",'Pneumonia', 'Asthma'],
        "headache": ["migraine", "tension headache", "sinusitis",'Cluster headache'],
        "nausea": ["food poisoning", "gastroenteritis", "migraine"],
        "fatigue": ["anemia", "hypothyroidism", "sleep apnea"],
        'vomiting': ['Gastroenteritis', 'Food poisoning', 'Appendicitis'],
        'diarrhea': ['Gastroenteritis', 'Food poisoning', 'Irritable bowel syndrome'],
        'fatigue': ['Chronic fatigue syndrome', 'Anemia', 'Hypothyroidism'],
        'abdominal pain': ['Gastroenteritis', 'Appendicitis', 'Diverticulitis'],
        'back pain': ['Muscle strain', 'Herniated disc', 'Sciatica'],
        'chest pain': ['Heart attack', 'Angina', 'Pulmonary embolism'],
        'shortness of breath': ['Asthma', 'Chronic obstructive pulmonary disease', 'Pulmonary embolism'],
        'wheezing': ['Asthma', 'Bronchitis', 'COPD'],
        'rash': ['Eczema', 'Psoriasis', 'Contact dermatitis'],
        'joint pain': ['Arthritis', 'Lupus', 'Fibromyalgia'],
        'muscle pain': ['Fibromyalgia', 'Myositis', 'Polymyalgia rheumatica'],
        'swollen lymph nodes': ['Mononucleosis', 'HIV', 'Lymphoma'],
        'red eyes': ['Conjunctivitis', 'Uveitis', 'Keratitis'],
        'blurred vision': ['Myopia', 'Hyperopia', 'Astigmatism'],
        'dizziness': ['Vertigo', 'Labyrinthitis', 'Meniere’s disease'],
        'balance problems': ['Vertigo', 'Labyrinthitis', 'Meniere’s disease'],
        'seizures': ['Epilepsy', 'Brain tumor', 'Stroke'],
        'tremors': ['Parkinson’s disease', 'Essential tremor', 'Multiple sclerosis'],
        'memory loss': ['Alzheimer’s disease', 'Dementia', 'Stroke'],
        'confusion': ['Delirium', 'Alzheimer’s disease', 'Dementia'],
        'anxiety': ['Generalized anxiety disorder', 'Panic disorder', 'Social anxiety disorder'],
        "allergies": ["Hay fever", "Asthma", "Eczema", "Food allergies"],
        "acne": ["Rosacea", "Hormonal acne", "Cystic acne"],
        "bad breath": ["Gum disease", "Cavities", "Dry mouth"],
        "bloating": ["Irritable bowel syndrome", "Celiac disease", "Gastroparesis"],
        "blood in stool": ["Colon cancer", "Ulcerative colitis", "Crohn's disease", "Hemorrhoids"],
        "blood in urine": ["Urinary tract infection", "Kidney stones", "Bladder cancer"],
        "blurry vision": ["Myopia", "Hyperopia", "Astigmatism", "Glaucoma"],
        "chest pain": ["Heart attack", "Angina", "Pulmonary embolism", "Gastroesophageal reflux disease (GERD)"],
        "chills": ["Influenza", "Pneumonia", "Malaria", "Lyme disease"],
        "cold hands and feet": ["Raynaud's disease", "Hypothyroidism", "Peripheral artery disease"],
        "depression": ["Major depressive disorder", "Seasonal affective disorder", "Bipolar disorder"],
        "diarrhea": ["Gastroenteritis", "Inflammatory bowel disease", "Celiac disease", "Lactose intolerance"],
        "difficulty breathing": ["Asthma", "Chronic obstructive pulmonary disease (COPD)", "Pneumonia"],
        "dizziness": ["Vertigo", "Inner ear infection", "Migraine", "Dehydration"],
        "dry skin": ["Eczema", "Psoriasis", "Hypothyroidism", "Diabetes"],
        "earache": ["Ear infection", "Swimmer's ear", "Sinus infection", "Temporomandibular joint (TMJ) disorder"],
        "frequent urination": ["Urinary tract infection", "Prostate problems", "Interstitial cystitis"],
        "gas": ["Irritable bowel syndrome", "Gastroesophageal reflux disease (GERD)", "Lactose intolerance"],
        "hair loss": ["Androgenic alopecia", "Telogen effluvium", "Alopecia areata"],
        "heart palpitations": ["Arrhythmia", "Atrial fibrillation", "Anxiety", "Hyperthyroidism"],
        "high blood pressure": ["Hypertension", "Atherosclerosis", "Heart attack", "Stroke"]
}
    
    symptoms = str(request.form["symptoms"])
    symptoms = symptoms.replace(", ",",")
    symptoms = symptoms.strip().lower().split(",")
    potential_conditions = []
    
    for symptom in symptoms:
         if symptom in symptom_to_condition:
              potential_conditions += symptom_to_condition[symptom]

    potential_conditions = list(set(potential_conditions))
    
    if potential_conditions:
        return render_template('results.html',conditions=potential_conditions)
    else:
        flash("Sorry, we could not find any potential conditions based on your symptoms.")
    return render_template('results.html',conditions=potential_conditions)
