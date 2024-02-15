import spacy
from nltk.corpus import wordnet as wn
import random
from llama_cpp import Llama

# Load the Spacy English model
nlp = spacy.load("en_core_web_lg")

# List of body parts
body_parts = [
    "tail", "penis", "armpits", "paws", "snout", "legs", "arms",
    "chest", "forearms", "hands", "testicles", "anus","butt","abs","nipples",
    "piercings","muscles","lips","tongue","mouth","ear","underside",
    "fur", "dick", "crotch", "bulge", "crotch bulge","balls","visible penis line",
    "uncircumcised penis", "uncut penis", "food","face","back","feet",
    "fingers", "pierced nipples", "pierced penis", "pierced uncut penis",
    "long foreskin", "foreskin", "foreskin folds", "frenulum"
]

base_verbs = [
    "sweat","musk","stink","do", "move", "touch", "feel", "hold", "shake", "masturbate", "piss",
    "urinate", "fuck", "suck", "lift", "grab", "grip", "tug", "pull", "rub",
    "present", "scratch",
]

# Function to expand verbs based on synonyms from WordNet
import nltk
from nltk.corpus import brown
nltk.download("brown")
# Get the frequency distribution of words in the Brown corpus
freq_dist = nltk.FreqDist(w.lower() for w in brown.words())

def expand_verbs(verb):
    expanded_verbs = {verb}  # Include the original verb
    for syn in wn.synsets(verb, pos=wn.VERB):
        for lemma in syn.lemmas():
            expanded_verbs.add(lemma.name().replace("_", " "))
    
    # Sort the expanded verbs by their frequency in the Brown corpus
    expanded_verbs = sorted(expanded_verbs, key=lambda x: freq_dist[x], reverse=True)
    
    # Return the 5 most common expanded verbs
    return expanded_verbs[:5]

# Initialize Llama model with optimized configurations
llm = Llama(
    model_path="C:\\Users\\toxic\\neuralbeagle14-7b.Q4_K_M.gguf",
    n_ctx=848, n_batch=128, n_gpu_layers=32, n_batch_threads=16,
    chat_format="llama-2"
)

def find_compatible_phrase(verb, body_part):
    prompt = "You are a gay creative erotica sentence writing assistant."
    content = (
        f"Write a short sentence about a male anthro doing normal, everyday things,"
        f" interacting with himself or another anthro or an object in a explicit, vulgar, innovative, or creative way, these are"
        f" good examples with enough detail: ``male anthro husky started to masturbate his friends penis in a playful manner, his eyes look like spirals as he sniffs his friends musky testicles``,"
        f" or ``male anthro husky lifts weights with his large pecs, his penis displayed sweating aggressively, sweat dripping down onto the gym floor``,"
        f" Please match this sort of sentence, be highly descriptive to select the best sentence that matches exclusively with both {verb} and {body_part} to create a complex scene in a sentence."
        f" Finish this sentence: ``male anthro husky {verb} with his {body_part}``"
    )

    # Simulated API call structure
    output = llm.create_chat_completion(messages=[
        {"role": "system", "content": prompt},
        {"role": "user", "content": content}
    ], max_tokens=255, stop=[".","/*"],temperature=.9, top_k=50, top_p=0.95)

    # Process output assuming a correct JSON structure is returned
    if 'choices' in output and output['choices']:
        generated_text = output['choices'][0]['message']['content']
        print(generated_text) 
        return generated_text

# Generate phrases ensuring the body part is included
phrases = []
for body_part in body_parts:
    for _ in range(5):
        base_verb = random.choice(base_verbs)
        expanded_verbs = expand_verbs(base_verb)
        for verb in expanded_verbs:
            chosen_phrase = find_compatible_phrase(verb, body_part)
            phrases.append(f"{chosen_phrase}")

# Save phrases to a file
with open("general_phraselist.txt", "w") as file:
    file.writelines([f"{phrase}\n" for phrase in phrases])

print("Phraselists generated and saved successfully.")
