"""
Czech Grammar Learning App - Backend
Aplikacja do nauki gramatyki czeskiej (zdania SVO)
"""

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import os

app = Flask(__name__, static_folder='static')
CORS(app)

# =============================================================================
# DANE GRAMATYCZNE - CZESKI
# =============================================================================

# Rzeczowniki (nominativ sg, rodzaj, wzór odmiany)
# Rodzaje: m_zyw (męski żywotny), m_nzyw (męski nieżywotny), f (żeński), n (nijaki)
NOUNS = {
    # Męskie żywotne
    "muž": {"gender": "m_zyw", "translation": "mężczyzna", "pattern": "muž"},
    "student": {"gender": "m_zyw", "translation": "student", "pattern": "student"},
    "učitel": {"gender": "m_zyw", "translation": "nauczyciel", "pattern": "muž"},
    "otec": {"gender": "m_zyw", "translation": "ojciec", "pattern": "muž"},
    "bratr": {"gender": "m_zyw", "translation": "brat", "pattern": "muž"},
    "syn": {"gender": "m_zyw", "translation": "syn", "pattern": "muž"},
    "přítel": {"gender": "m_zyw", "translation": "przyjaciel", "pattern": "muž"},
    "kolega": {"gender": "m_zyw", "translation": "kolega", "pattern": "kolega"},
    "soused": {"gender": "m_zyw", "translation": "sąsiad", "pattern": "muž"},
    "lékař": {"gender": "m_zyw", "translation": "lekarz", "pattern": "muž"},
    "pes": {"gender": "m_zyw", "translation": "pies", "pattern": "muž"},
    "kůň": {"gender": "m_zyw", "translation": "koń", "pattern": "muž"},
    
    # Męskie nieżywotne
    "hrad": {"gender": "m_nzyw", "translation": "zamek", "pattern": "hrad"},
    "dům": {"gender": "m_nzyw", "translation": "dom", "pattern": "hrad"},
    "stůl": {"gender": "m_nzyw", "translation": "stół", "pattern": "hrad"},
    "počítač": {"gender": "m_nzyw", "translation": "komputer", "pattern": "stroj"},
    "telefon": {"gender": "m_nzyw", "translation": "telefon", "pattern": "hrad"},
    "auto": {"gender": "n", "translation": "samochód", "pattern": "město"},
    "vlak": {"gender": "m_nzyw", "translation": "pociąg", "pattern": "hrad"},
    "autobus": {"gender": "m_nzyw", "translation": "autobus", "pattern": "hrad"},
    "obchod": {"gender": "m_nzyw", "translation": "sklep", "pattern": "hrad"},
    "film": {"gender": "m_nzyw", "translation": "film", "pattern": "hrad"},
    
    # Żeńskie
    "žena": {"gender": "f", "translation": "kobieta", "pattern": "žena"},
    "matka": {"gender": "f", "translation": "matka", "pattern": "žena"},
    "sestra": {"gender": "f", "translation": "siostra", "pattern": "žena"},
    "dcera": {"gender": "f", "translation": "córka", "pattern": "žena"},
    "přítelkyně": {"gender": "f", "translation": "przyjaciółka", "pattern": "růže"},
    "učitelka": {"gender": "f", "translation": "nauczycielka", "pattern": "žena"},
    "studentka": {"gender": "f", "translation": "studentka", "pattern": "žena"},
    "kniha": {"gender": "f", "translation": "książka", "pattern": "žena"},
    "škola": {"gender": "f", "translation": "szkoła", "pattern": "žena"},
    "práce": {"gender": "f", "translation": "praca", "pattern": "růže"},
    "káva": {"gender": "f", "translation": "kawa", "pattern": "žena"},
    "voda": {"gender": "f", "translation": "woda", "pattern": "žena"},
    "hudba": {"gender": "f", "translation": "muzyka", "pattern": "žena"},
    "kočka": {"gender": "f", "translation": "kot", "pattern": "žena"},
    
    # Nijakie
    "město": {"gender": "n", "translation": "miasto", "pattern": "město"},
    "okno": {"gender": "n", "translation": "okno", "pattern": "město"},
    "jídlo": {"gender": "n", "translation": "jedzenie", "pattern": "město"},
    "pivo": {"gender": "n", "translation": "piwo", "pattern": "město"},
    "víno": {"gender": "n", "translation": "wino", "pattern": "město"},
    "dítě": {"gender": "n", "translation": "dziecko", "pattern": "kuře"},
    "moře": {"gender": "n", "translation": "morze", "pattern": "moře"},
    "slunce": {"gender": "n", "translation": "słońce", "pattern": "moře"},
}

# Przymiotniki (forma męska sg)
ADJECTIVES = {
    "dobrý": {"translation": "dobry"},
    "špatný": {"translation": "zły"},
    "velký": {"translation": "duży"},
    "malý": {"translation": "mały"},
    "nový": {"translation": "nowy"},
    "starý": {"translation": "stary"},
    "mladý": {"translation": "młody"},
    "krásný": {"translation": "piękny"},
    "hezký": {"translation": "ładny"},
    "ošklivý": {"translation": "brzydki"},
    "chytrý": {"translation": "mądry"},
    "hloupý": {"translation": "głupi"},
    "rychlý": {"translation": "szybki"},
    "pomalý": {"translation": "wolny"},
    "silný": {"translation": "silny"},
    "slabý": {"translation": "słaby"},
    "vysoký": {"translation": "wysoki"},
    "nízký": {"translation": "niski"},
    "dlouhý": {"translation": "długi"},
    "krátký": {"translation": "krótki"},
    "těžký": {"translation": "ciężki"},
    "lehký": {"translation": "lekki"},
    "drahý": {"translation": "drogi"},
    "levný": {"translation": "tani"},
    "bohatý": {"translation": "bogaty"},
    "chudý": {"translation": "biedny"},
    "čistý": {"translation": "czysty"},
    "špinavý": {"translation": "brudny"},
    "teplý": {"translation": "ciepły"},
    "studený": {"translation": "zimny"},
    "suchý": {"translation": "suchy"},
    "mokrý": {"translation": "mokry"},
    "tvrdý": {"translation": "twardy"},
    "měkký": {"translation": "miękki"},
    "český": {"translation": "czeski"},
    "polský": {"translation": "polski"},
    "zajímavý": {"translation": "interesujący"},
    "nudný": {"translation": "nudny"},
    "veselý": {"translation": "wesoły"},
    "smutný": {"translation": "smutny"},
}

# Czasowniki (infinitiv, koniugacja)
VERBS = {
    "být": {"translation": "być", "conj_class": "irregular_byt"},
    "mít": {"translation": "mieć", "conj_class": "irregular_mit"},
    "dělat": {"translation": "robić", "conj_class": "a"},
    "pracovat": {"translation": "pracować", "conj_class": "ovat"},
    "studovat": {"translation": "studiować", "conj_class": "ovat"},
    "mluvit": {"translation": "mówić", "conj_class": "i"},
    "psát": {"translation": "pisać", "conj_class": "a"},
    "číst": {"translation": "czytać", "conj_class": "irregular_cist"},
    "vidět": {"translation": "widzieć", "conj_class": "e"},
    "slyšet": {"translation": "słyszeć", "conj_class": "e"},
    "jíst": {"translation": "jeść", "conj_class": "irregular_jist"},
    "pít": {"translation": "pić", "conj_class": "irregular_pit"},
    "spát": {"translation": "spać", "conj_class": "irregular_spat"},
    "chtít": {"translation": "chcieć", "conj_class": "irregular_chtit"},
    "muset": {"translation": "musieć", "conj_class": "irregular_muset"},
    "moct": {"translation": "móc", "conj_class": "irregular_moct"},
    "vědět": {"translation": "wiedzieć", "conj_class": "irregular_vedet"},
    "znát": {"translation": "znać", "conj_class": "a"},
    "rozumět": {"translation": "rozumieć", "conj_class": "e"},
    "milovat": {"translation": "kochać", "conj_class": "ovat"},
    "kupovat": {"translation": "kupować", "conj_class": "ovat"},
    "prodávat": {"translation": "sprzedawać", "conj_class": "a"},
    "hrát": {"translation": "grać", "conj_class": "a"},
    "zpívat": {"translation": "śpiewać", "conj_class": "a"},
    "tančit": {"translation": "tańczyć", "conj_class": "i"},
    "běžet": {"translation": "biec", "conj_class": "e"},
    "chodit": {"translation": "chodzić", "conj_class": "i"},
    "jezdit": {"translation": "jeździć", "conj_class": "i"},
    "cestovat": {"translation": "podróżować", "conj_class": "ovat"},
    "telefonovat": {"translation": "telefonować", "conj_class": "ovat"},
    "pomáhat": {"translation": "pomagać", "conj_class": "a"},
    "potřebovat": {"translation": "potrzebować", "conj_class": "ovat"},
    "myslet": {"translation": "myśleć", "conj_class": "e"},
    "učit": {"translation": "uczyć", "conj_class": "i"},
    "učit se": {"translation": "uczyć się", "conj_class": "i"},
    "bydlet": {"translation": "mieszkać", "conj_class": "e"},
    "žít": {"translation": "żyć", "conj_class": "irregular_zit"},
    "vařit": {"translation": "gotować", "conj_class": "i"},
    "jmenovat se": {"translation": "nazywać się", "conj_class": "ovat"},
}

# Zaimki dzierżawcze
POSSESSIVE_PRONOUNS = {
    "můj": {"translation": "mój", "gender_forms": {"m": "můj", "f": "moje/má", "n": "moje/mé"}},
    "tvůj": {"translation": "twój", "gender_forms": {"m": "tvůj", "f": "tvoje/tvá", "n": "tvoje/tvé"}},
    "jeho": {"translation": "jego", "gender_forms": {"m": "jeho", "f": "jeho", "n": "jeho"}},
    "její": {"translation": "jej", "gender_forms": {"m": "její", "f": "její", "n": "její"}},
    "náš": {"translation": "nasz", "gender_forms": {"m": "náš", "f": "naše", "n": "naše"}},
    "váš": {"translation": "wasz", "gender_forms": {"m": "váš", "f": "vaše", "n": "vaše"}},
    "jejich": {"translation": "ich", "gender_forms": {"m": "jejich", "f": "jejich", "n": "jejich"}},
}

# Zaimki wskazujące
DEMONSTRATIVE_PRONOUNS = {
    "ten": {"translation": "ten", "gender_forms": {"m": "ten", "f": "ta", "n": "to"}},
    "tento": {"translation": "ten (bliski)", "gender_forms": {"m": "tento", "f": "tato", "n": "toto"}},
    "tamten": {"translation": "tamten", "gender_forms": {"m": "tamten", "f": "tamta", "n": "tamto"}},
}

# =============================================================================
# FUNKCJE ODMIANY
# =============================================================================

def decline_adjective(adj_base, gender, number, case="nom"):
    """Odmiana przymiotnika według rodzaju, liczby i przypadku."""
    # Uproszczona odmiana dla nominativu i akuzativu
    if adj_base.endswith("ý"):
        stem = adj_base[:-1]
        if number == "sg":
            if gender == "m_zyw":
                return stem + "ý" if case == "nom" else stem + "ého"
            elif gender == "m_nzyw":
                return stem + "ý"
            elif gender == "f":
                return stem + "á" if case == "nom" else stem + "ou"
            elif gender == "n":
                return stem + "é"
        else:  # plural
            if gender in ["m_zyw"]:
                return stem + "í" if case == "nom" else stem + "é"
            elif gender == "m_nzyw":
                return stem + "é"
            elif gender == "f":
                return stem + "é"
            elif gender == "n":
                return stem + "á"
    return adj_base


def decline_noun(noun, number, case="nom"):
    """Odmiana rzeczownika według liczby i przypadku."""
    if noun not in NOUNS:
        return noun
    
    info = NOUNS[noun]
    gender = info["gender"]
    pattern = info["pattern"]
    
    # Uproszczone reguły odmiany dla podstawowych przypadków
    # Nominativ i Akuzativ
    
    if number == "sg":
        if case == "nom":
            return noun
        elif case == "acc":
            # Akuzativ sg
            if gender == "m_zyw":
                # Męskie żywotne - końcówka -a
                if noun.endswith("a"):
                    return noun[:-1] + "u"
                return noun + "a"
            elif gender == "m_nzyw":
                return noun  # = nominativ
            elif gender == "f":
                if noun.endswith("a"):
                    return noun[:-1] + "u"
                elif noun.endswith("e"):
                    return noun[:-1] + "i"
                return noun
            elif gender == "n":
                return noun  # = nominativ
    else:  # plural
        if case == "nom" or case == "acc":
            if gender == "m_zyw":
                if noun.endswith("a"):
                    return noun[:-1] + "ové"
                return noun + "i" if noun[-1] not in "kgch" else noun + "ové"
            elif gender == "m_nzyw":
                return noun + "y"
            elif gender == "f":
                if noun.endswith("a"):
                    return noun[:-1] + "y"
                elif noun.endswith("e"):
                    return noun[:-1] + "e"
                return noun + "e"
            elif gender == "n":
                if noun.endswith("o"):
                    return noun[:-1] + "a"
                elif noun.endswith("e"):
                    return noun[:-1] + "e"
                elif noun.endswith("í"):
                    return noun
                return noun + "a"
    
    return noun


def conjugate_verb(verb, person, number, tense="present", mood="indicative", negative=False):
    """Koniugacja czasownika."""
    if verb not in VERBS:
        return verb
    
    info = VERBS[verb]
    conj_class = info["conj_class"]
    
    # Prefix negacji
    neg_prefix = "ne" if negative else ""
    
    # Czas teraźniejszy - tryb oznajmujący
    if tense == "present" and mood == "indicative":
        forms = get_present_forms(verb, conj_class)
        idx = (person - 1) + (0 if number == "sg" else 3)
        form = forms[idx]
        if negative:
            # "ne" przed czasownikiem, ale "není" dla "je"
            if form == "je":
                return "není"
            elif form == "jsem":
                return "nejsem"
            elif form == "jsi":
                return "nejsi"
            elif form == "jsou":
                return "nejsou"
            elif form == "jsme":
                return "nejsme"
            elif form == "jste":
                return "nejste"
            return neg_prefix + form
        return form
    
    # Czas przeszły
    elif tense == "past":
        l_form = get_past_participle(verb, conj_class)
        aux = get_present_forms("být", "irregular_byt")
        
        if number == "sg":
            if person == 1:
                return f"{neg_prefix}{l_form} {'jsem' if not negative else 'nejsem'}"
            elif person == 2:
                return f"{neg_prefix}{l_form} {'jsi' if not negative else 'nejsi'}"
            else:
                return f"{neg_prefix}{l_form}"
        else:
            if person == 1:
                return f"{neg_prefix}{l_form}i {'jsme' if not negative else 'nejsme'}"
            elif person == 2:
                return f"{neg_prefix}{l_form}i {'jste' if not negative else 'nejste'}"
            else:
                return f"{neg_prefix}{l_form}i"
    
    # Czas przyszły
    elif tense == "future":
        if verb == "být":
            future_forms = ["budu", "budeš", "bude", "budeme", "budete", "budou"]
            idx = (person - 1) + (0 if number == "sg" else 3)
            form = future_forms[idx]
            return neg_prefix + form if not negative else "ne" + form
        else:
            # budu + infinitiv
            future_aux = ["budu", "budeš", "bude", "budeme", "budete", "budou"]
            idx = (person - 1) + (0 if number == "sg" else 3)
            aux = future_aux[idx]
            return f"{'ne' if negative else ''}{aux} {verb}"
    
    # Tryb rozkazujący
    elif mood == "imperative":
        imp_form = get_imperative(verb, conj_class, person, number)
        return neg_prefix + imp_form if imp_form else verb
    
    # Tryb przypuszczający
    elif mood == "conditional":
        l_form = get_past_participle(verb, conj_class)
        cond_aux = ["bych", "bys", "by", "bychom", "byste", "by"]
        idx = (person - 1) + (0 if number == "sg" else 3)
        aux = cond_aux[idx]
        return f"{neg_prefix}{l_form} {aux}"
    
    return verb


def get_present_forms(verb, conj_class):
    """Zwraca formy czasu teraźniejszego [1sg, 2sg, 3sg, 1pl, 2pl, 3pl]."""
    
    irregular = {
        "irregular_byt": ["jsem", "jsi", "je", "jsme", "jste", "jsou"],
        "irregular_mit": ["mám", "máš", "má", "máme", "máte", "mají"],
        "irregular_chtit": ["chci", "chceš", "chce", "chceme", "chcete", "chtějí"],
        "irregular_muset": ["musím", "musíš", "musí", "musíme", "musíte", "musí"],
        "irregular_moct": ["mohu/můžu", "můžeš", "může", "můžeme", "můžete", "mohou/můžou"],
        "irregular_vedet": ["vím", "víš", "ví", "víme", "víte", "vědí"],
        "irregular_jist": ["jím", "jíš", "jí", "jíme", "jíte", "jedí"],
        "irregular_pit": ["piju", "piješ", "pije", "pijeme", "pijete", "pijou"],
        "irregular_spat": ["spím", "spíš", "spí", "spíme", "spíte", "spí"],
        "irregular_cist": ["čtu", "čteš", "čte", "čteme", "čtete", "čtou"],
        "irregular_zit": ["žiju", "žiješ", "žije", "žijeme", "žijete", "žijou"],
    }
    
    if conj_class in irregular:
        return irregular[conj_class]
    
    # Regularne klasy
    if verb.endswith("at"):
        stem = verb[:-2]
        if conj_class == "a":
            return [stem+"ám", stem+"áš", stem+"á", stem+"áme", stem+"áte", stem+"ají"]
    
    if verb.endswith("ovat"):
        stem = verb[:-4]
        return [stem+"uji/uju", stem+"uješ", stem+"uje", stem+"ujeme", stem+"ujete", stem+"ují/ujou"]
    
    if verb.endswith("it"):
        stem = verb[:-2]
        return [stem+"ím", stem+"íš", stem+"í", stem+"íme", stem+"íte", stem+"í"]
    
    if verb.endswith("et") or verb.endswith("ět"):
        stem = verb[:-2]
        return [stem+"ím", stem+"íš", stem+"í", stem+"íme", stem+"íte", stem+"í"]
    
    # Domyślnie
    stem = verb[:-1] if verb[-1] in "taei" else verb
    return [stem+"u", stem+"eš", stem+"e", stem+"eme", stem+"ete", stem+"ou"]


def get_past_participle(verb, conj_class):
    """Zwraca imiesłów przeszły (l-participle) w formie męskiej sg."""
    
    irregular = {
        "irregular_byt": "byl",
        "irregular_mit": "měl",
        "irregular_chtit": "chtěl",
        "irregular_muset": "musel",
        "irregular_moct": "mohl",
        "irregular_vedet": "věděl",
        "irregular_jist": "jedl",
        "irregular_pit": "pil",
        "irregular_spat": "spal",
        "irregular_cist": "četl",
        "irregular_zit": "žil",
    }
    
    if conj_class in irregular:
        return irregular[conj_class]
    
    if verb.endswith("ovat"):
        return verb[:-4] + "oval"
    if verb.endswith("at"):
        return verb[:-1] + "l"
    if verb.endswith("it"):
        return verb[:-1] + "l"
    if verb.endswith("et") or verb.endswith("ět"):
        return verb[:-2] + "ěl"
    
    return verb + "l"


def get_imperative(verb, conj_class, person, number):
    """Zwraca formę trybu rozkazującego."""
    if person == 1 and number == "sg":
        return None  # Brak formy
    
    # Uproszczone formy rozkazujące
    present = get_present_forms(verb, conj_class)
    stem_3sg = present[2]  # 3 osoba sg jako baza
    
    # Usuń końcówkę
    if stem_3sg.endswith("e") or stem_3sg.endswith("á") or stem_3sg.endswith("í"):
        stem = stem_3sg[:-1]
    else:
        stem = stem_3sg
    
    if person == 2 and number == "sg":
        return stem + "!" if not stem.endswith(("j","ň","ť","ď")) else stem + "!"
    elif person == 1 and number == "pl":
        return stem + "me!"
    elif person == 2 and number == "pl":
        return stem + "te!"
    
    return None


def build_sentence(subject_data, verb_data, object_data=None):
    """Buduje pełne zdanie SVO."""
    
    # Podmiot
    subj_noun = subject_data.get("noun", "")
    subj_adj = subject_data.get("adjective")
    subj_number = subject_data.get("number", "sg")
    subj_determiner = subject_data.get("determiner")
    subj_possessive = subject_data.get("possessive")
    
    noun_info = NOUNS.get(subj_noun, {})
    gender = noun_info.get("gender", "m_nzyw")
    
    # Odmień rzeczownik (nominativ dla podmiotu)
    declined_noun = decline_noun(subj_noun, subj_number, "nom")
    
    # Podmiot z dodatkami
    subject_parts = []
    
    if subj_determiner and subj_determiner in DEMONSTRATIVE_PRONOUNS:
        dem = DEMONSTRATIVE_PRONOUNS[subj_determiner]
        g_key = "m" if gender.startswith("m") else ("f" if gender == "f" else "n")
        subject_parts.append(dem["gender_forms"][g_key])
    
    if subj_possessive and subj_possessive in POSSESSIVE_PRONOUNS:
        poss = POSSESSIVE_PRONOUNS[subj_possessive]
        g_key = "m" if gender.startswith("m") else ("f" if gender == "f" else "n")
        subject_parts.append(poss["gender_forms"][g_key])
    
    if subj_adj and subj_adj in ADJECTIVES:
        declined_adj = decline_adjective(subj_adj, gender, subj_number, "nom")
        subject_parts.append(declined_adj)
    
    subject_parts.append(declined_noun)
    subject_str = " ".join(subject_parts)
    
    # Czasownik
    verb_inf = verb_data.get("verb", "být")
    person = verb_data.get("person", 3)
    v_number = verb_data.get("number", "sg")
    tense = verb_data.get("tense", "present")
    mood = verb_data.get("mood", "indicative")
    negative = verb_data.get("negative", False)
    question = verb_data.get("question", False)
    
    conjugated = conjugate_verb(verb_inf, person, v_number, tense, mood, negative)
    
    # Dopełnienie
    object_str = ""
    if object_data and object_data.get("noun"):
        obj_noun = object_data["noun"]
        obj_adj = object_data.get("adjective")
        obj_number = object_data.get("number", "sg")
        obj_determiner = object_data.get("determiner")
        obj_possessive = object_data.get("possessive")
        
        obj_info = NOUNS.get(obj_noun, {})
        obj_gender = obj_info.get("gender", "m_nzyw")
        
        # Odmień (akuzativ dla dopełnienia)
        declined_obj = decline_noun(obj_noun, obj_number, "acc")
        
        object_parts = []
        
        if obj_determiner and obj_determiner in DEMONSTRATIVE_PRONOUNS:
            dem = DEMONSTRATIVE_PRONOUNS[obj_determiner]
            g_key = "m" if obj_gender.startswith("m") else ("f" if obj_gender == "f" else "n")
            # Akuzativ dla zaimków wskazujących
            if obj_gender == "m_zyw":
                object_parts.append("toho" if obj_determiner == "ten" else obj_determiner)
            else:
                object_parts.append(dem["gender_forms"][g_key])
        
        if obj_possessive and obj_possessive in POSSESSIVE_PRONOUNS:
            poss = POSSESSIVE_PRONOUNS[obj_possessive]
            g_key = "m" if obj_gender.startswith("m") else ("f" if obj_gender == "f" else "n")
            object_parts.append(poss["gender_forms"][g_key])
        
        if obj_adj and obj_adj in ADJECTIVES:
            declined_obj_adj = decline_adjective(obj_adj, obj_gender, obj_number, "acc")
            object_parts.append(declined_obj_adj)
        
        object_parts.append(declined_obj)
        object_str = " ".join(object_parts)
    
    # Złóż zdanie
    if mood == "imperative":
        sentence = f"{conjugated}"
        if object_str:
            sentence = f"{conjugated[:-1]} {object_str}!"
    else:
        parts = [subject_str, conjugated]
        if object_str:
            parts.append(object_str)
        sentence = " ".join(parts)
        
        if question:
            sentence = sentence + "?"
        else:
            sentence = sentence + "."
    
    return sentence.capitalize()


# =============================================================================
# API ENDPOINTS
# =============================================================================

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/api/nouns')
def get_nouns():
    result = []
    for noun, info in NOUNS.items():
        result.append({
            "word": noun,
            "gender": info["gender"],
            "translation": info["translation"]
        })
    return jsonify(sorted(result, key=lambda x: x["word"]))

@app.route('/api/adjectives')
def get_adjectives():
    result = []
    for adj, info in ADJECTIVES.items():
        result.append({
            "word": adj,
            "translation": info["translation"]
        })
    return jsonify(sorted(result, key=lambda x: x["word"]))

@app.route('/api/verbs')
def get_verbs():
    result = []
    for verb, info in VERBS.items():
        result.append({
            "word": verb,
            "translation": info["translation"]
        })
    return jsonify(sorted(result, key=lambda x: x["word"]))

@app.route('/api/pronouns/possessive')
def get_possessive_pronouns():
    result = []
    for pron, info in POSSESSIVE_PRONOUNS.items():
        result.append({
            "word": pron,
            "translation": info["translation"]
        })
    return jsonify(result)

@app.route('/api/pronouns/demonstrative')
def get_demonstrative_pronouns():
    result = []
    for pron, info in DEMONSTRATIVE_PRONOUNS.items():
        result.append({
            "word": pron,
            "translation": info["translation"]
        })
    return jsonify(result)

@app.route('/api/decline/noun', methods=['POST'])
def api_decline_noun():
    data = request.json
    noun = data.get("noun", "")
    number = data.get("number", "sg")
    case = data.get("case", "nom")
    
    result = decline_noun(noun, number, case)
    return jsonify({"declined": result})

@app.route('/api/decline/adjective', methods=['POST'])
def api_decline_adjective():
    data = request.json
    adj = data.get("adjective", "")
    gender = data.get("gender", "m_nzyw")
    number = data.get("number", "sg")
    case = data.get("case", "nom")
    
    result = decline_adjective(adj, gender, number, case)
    return jsonify({"declined": result})

@app.route('/api/conjugate', methods=['POST'])
def api_conjugate():
    data = request.json
    verb = data.get("verb", "")
    person = data.get("person", 3)
    number = data.get("number", "sg")
    tense = data.get("tense", "present")
    mood = data.get("mood", "indicative")
    negative = data.get("negative", False)
    
    result = conjugate_verb(verb, person, number, tense, mood, negative)
    return jsonify({"conjugated": result})

@app.route('/api/build', methods=['POST'])
def api_build_sentence():
    data = request.json
    subject = data.get("subject", {})
    verb = data.get("verb", {})
    obj = data.get("object")
    
    result = build_sentence(subject, verb, obj)
    return jsonify({"sentence": result})


if __name__ == '__main__':
    app.run(debug=True, port=5000)
