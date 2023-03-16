import openai
import os

a1 = "sk-BGnlSu6qwg"
a2 = "SFD1CHiTc9T3Blbk"
a3 = "FJScqmD4tX1lmeo0hG9IAh"
openai.api_key = a1+a2+a3

def start_conversation():
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt="User: Hello\nAI:",
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )
    return response.choices[0].text

def get_ai_response(conversation_history, user_input):
    prompt = f"User: {user_input}\nAI: {conversation_history}"
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )
    return response.choices[0].text

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
                       ]
    is_health_related = any(keyword in user_input.lower() for keyword in health_keywords)
    if is_health_related:
        return True
    else:
        return False
