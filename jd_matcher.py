
from sentence_transformers import SentenceTransformer, util
model = SentenceTransformer('all-MiniLM-L6-v2')
def get_similarity(resume_text, jd_text):
    v1 = model.encode(resume_text, convert_to_tensor=True)
    v2 = model.encode(jd_text, convert_to_tensor=True)
    return util.cos_sim(v1, v2).item()
