from collections import OrderedDict

MEDICINES = [
    ('Abacavir 20 mg/mL solution (240 mL)',),
    ('Adrenaline 1 mg/ml injection (1 mL ampoule)',),
    ('Amoxicillin 125 mg/5ml suspension (75 or 100 mL)', 'amosus'),
    ('Amoxicillin 250 mg or 500 mg capsules (15 capsules)', 'amocap'),
    ('Azithromycin 500mg',),
    ('Beclomethasone 50 mcg or 100 mcg inhaler (200 inhalations)',),
    ('Ceftriaxone injection 250 mg or 500 mg (vial)', 'cex'),
    ('Hexavalent (Vaccine)',),
    ('Hydrochlorothiazide 12.5 or 25 mg tablets (28 tablets)',),
    ('Insulin soluble 100IU/ml injection (10 mL vial)',),
    ('Isoniazid 300 mg tablet (28 tablets)',),
    ('Lamivudine 10 mg/mL solution (240 mL)',),
    ('Medroxyprogesterone injection 150 mg (1 mL vial)',),
    ('Metformin 500 mg or 850 mg tablets (56 or 84 tablets)',),
    ('Paracetamol 500 mg tablets (10 or 20 tablets)', 'partab'),
    ('Paracetamol syrup 120 mg/5mL (50 mL or 100 mL)', 'parsyr'),
    ('Rifampicin 150 mg, isoniazid 75 mg, pyrazinamide 400 mg and ethambutol 275 mg tablets  (28, 56 or 84 tablets)', 'rif150'),
    ('Rifampicin 60mg and isoniazid 60 mg dispersible tablet (28 or 56 tablets)', 'rif60'),
    ('Sodium chloride 0.9% 1L',),
    ('Tenofovir 300 mg, emtricitabine 200 mg, efavirenz 600 mg tablet, 28 tablets  (FDC)',),
    ('Tetanus toxoid vaccine (10 doses)',),
    ('Valproate sodium 50ml or 200mg',),
]

UNUSED_MEDICINES = [
    ('Carbamazepine 200 mg tablets (28, 56 or 84 tablets)',),
    ('Cefixime 400 mg capsules (1 capsule)', 'cef'),
    ('DTaP-IPV/Hib (Pentavalent) Vaccine (EPI)',),
]


def med_code(med):
    if len(med) > 1:
        name, code = med
    else:
        name = med[0]
        code = name.lower()[0:3]

    return name, code


MEDS = OrderedDict()
for med in MEDICINES + UNUSED_MEDICINES:
    name, code = med_code(med)

    MEDS[code] = name


DISTRICT_CODES = dict([
    ("Alfred Nzo District Municipality", "DC44"),
    ("Amajuba District Municipality", "DC25"),
    ("Amathole District Municipality", "DC12"),
    ("Bojanala Platinum District Municipality", "DC37"),
    ("Buffalo City Metropolitan Municipality", "BUF"),
    ("Cacadu District Municipality", "DC10"),
    ("Cape Winelands District Municipality", "DC2"),
    ("Capricorn District Municipality", "DC35"),
    ("Central Karoo District Municipality", "DC5"),
    ("Chris Hani District Municipality", "DC13"),
    ("City of Cape Town Metropolitan Municipality", "CPT"),
    ("City of Johannesburg Metropolitan", "JHB"),
    ("City of Tshwane Metropolitan Municipality", "TSH"),
    ("Dr Kenneth Kaunda District Municipality", "DC40"),
    ("Dr Ruth Segomotsi Mompati District Municipality", "DC39"),
    ("Eden District Municipality", "DC4"),
    ("Ehlanzeni District Municipality", "DC32"),
    ("Ekurhuleni Metropolitan Municipality", "EKU"),
    ("eThekwini Metropolitan Municipality", "ETH"),
    ("Fezile Dabi District Municipality", "DC20"),
    ("Frances Baard District Municipality", "DC9"),
    ("Gert Sibande District Municipality", "DC30"),
    ("iLembe District Municipality", "DC29"),
    ("Joe Gqabi District Municipality", "DC14"),
    ("John Taolo Gaetsewe District Municipality", "DC45"),
    ("Lejweleputswa District Municipality", "DC18"),
    ("Mangaung Metropolitan Municipality", "MAN"),
    ("Mopani District Municipality", "DC33"),
    ("Namakwa District Municipality", "DC6"),
    ("Nelson Mandela Bay Municipality", "NMA"),
    ("Ngaka Modiri Molema District Municipality", "DC38"),
    ("Nkangala District Municipality", "DC31"),
    ("Oliver Tambo District Municipality", "DC15"),
    ("Overberg District Municipality", "DC3"),
    ("Pixley ka Seme District Municipality", "DC7"),
    ("Sedibeng District Municipality", "DC42"),
    ("Sekhukhune District Municipality", "DC47"),
    ("Sisonke District Municipality", "DC43"),
    ("Siyanda District Municipality", "DC8"),
    ("Thabo Mofutsanyana District Municipality", "DC19"),
    ("Ugu District Municipality", "DC21"),
    ("uMgungundlovu District Municipality", "DC22"),
    ("uMkhanyakude District Municipality", "DC27"),
    ("uMzinyathi District Municipality", "DC24"),
    ("uThukela District Municipality", "DC23"),
    ("uThungulu District Municipality", "DC28"),
    ("Vhembe District Municipality", "DC34"),
    ("Waterberg District Municipality", "DC36"),
    ("West Coast District Municipality", "DC1"),
    ("West Rand District Municipality", "DC48"),
    ("Xhariep District Municipality", "DC16"),
    ("Zululand District Municipality", "DC26"),
])
DISTRICTS = {v: k for k, v in DISTRICT_CODES.iteritems()}

PROVINCE_CODES = {
    'Eastern Cape': 'EC',
    'Free State': 'FS',
    'Gauteng': 'GT',
    'KwaZulu-Natal': 'KZN',
    'Limpopo': 'LIM',
    'Mpumalanga': 'MP',
    'North West': 'NW',
    'Northern Cape': 'NC',
    'Western Cape': 'WC',
}
PROVINCES = {v: k for k, v in PROVINCE_CODES.iteritems()}
