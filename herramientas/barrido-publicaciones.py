# -*- coding: utf-8 -*-
"""Genera _data/publications.yml del sitio general:
   - trae las de aguas (2023+) con areas: [aguas] (+ las áreas de otros PI que firmen)
   - agrega el barrido 2020–2026 de Vergara, Scott, Guerrero, Moreno (Google Scholar → Crossref)
   - agrega las de Huiliñir 2020–2022 (Crossref), en bloque aparte y comentado
   Dedupe por DOI. Se corre en el Mac/VM con las dos carpetas montadas.
"""
import io, re, sys, yaml

AGUAS = sys.argv[1]      # .../pagina_web_gtech/github/_data/publications.yml
DEST  = sys.argv[2]      # .../pagina_web_gtech_general/github/_data/publications.yml

PI = {  # apellido tal como aparece en la lista de autores → área
    "Vergara-Fern": "vergara", "Vergara‐Fern": "vergara",
    "Scott, F": "scott",
    "Guerrero, S": "guerrero",
    "Moreno-Casas": "moreno", "Moreno‐Casas": "moreno",
    "Huiliñir": "aguas", "Carreño-López": "aguas", "Carreno-Lopez": "aguas", "Carreño‐López": "aguas",
}
ORDEN = ["vergara", "aguas", "scott", "guerrero", "moreno"]

def areas_de(autores):
    a = {v for k, v in PI.items() if k in autores}
    return [x for x in ORDEN if x in a]

def limpia(s):
    s = re.sub(r"<[^>]+>", "", s)
    s = s.replace("‐", "-").replace("‑", "-").replace("&amp;", "&")
    return re.sub(r"\s+", " ", s).strip()

def det(vol, issue, page):
    v = vol + (f"({issue})" if issue else "")
    return ", ".join(x for x in (v, page) if x)

# ---- barrido Vergara / Scott / Guerrero / Moreno (Crossref por título) ----
# (year, authors "A, B.; C, D.", title, journal, vol, issue, page, doi, featured)
NUEVAS = [
 (2026, "Martín-Dávison, J. S.; Vergara-Fernández, A.; Guerrero, S.; Pulido, N. A.", "Catalytic oxidation of biomass combustion emissions over K-M/MgO (M = Cu, Mn, Fe) mixed oxide catalysts", "Reaction Kinetics, Mechanisms and Catalysis", "139", "3", "1789-1813", "10.1007/s11144-026-03104-1", True),
 (2026, "Araya, B.; Torres-Praderio, P.; Conejeros, R.; Vergara-Fernández, A.; Scott, F.", "Triacylglycerol accumulation in Rhodococcus opacus DSM 43205 from Knallgas and Knallgas-derived soluble intermediates", "Journal of Environmental Chemical Engineering", "14", "1", "120959", "10.1016/j.jece.2025.120959", False),
 (2026, "Bobillier, P.; Scott, F.; Bolivar, J. M.; Illanes, A.; Wilson, L.; Conejeros, R.", "Modeling-based optimal control policies for a multienzymatic system with distinct thermal stabilities in packed-bed reactors", "Chemical Engineering Science", "334", "", "124275", "10.1016/j.ces.2026.124275", False),
 (2026, "Silva, O.; Maxwell, L.; Guerrero, S.; Creaser, D.; Cornejo, I.", "Techno-economic evaluation and carbon balance of multiple process routes for light olefin production from green hydrogen and captured CO2", "Chemical Engineering Research and Design", "230", "", "111-127", "10.1016/j.cherd.2026.04.037", True),
 (2026, "Díaz-Ulloa, P.; Garrido-Figueroa, B.; Guerrero, S.; Cornejo, I.", "Nusselt number correlation for convective heat transfer in dual core-ring packed beds", "Chemical Engineering Science", "322", "", "123067", "10.1016/j.ces.2025.123067", False),
 (2025, "Cruz, P.; Lebrero, R.; Vergara-Fernández, A.; Muñoz, R.", "Airlift Taylor Flow bioreactors as a novel platform to enhance H2-assisted CO2 bioconversion processes", "Chemical Engineering Journal", "522", "", "167871", "10.1016/j.cej.2025.167871", True),
 (2025, "Silva, P.; Scott, F.; Adloor, S. D.; Vassiliadis, V. S.; Illanes, A.; Wilson, L.; Conejeros, R.", "Optimal control of scheduling and production for a multienzymatic system in continuous reactors", "Computers & Chemical Engineering", "201", "", "109209", "10.1016/j.compchemeng.2025.109209", False),
 (2025, "Toro, J. P.; Sepúlveda, S.; Bombardelli, F. A.; Moreno-Casas, P. A.; Meireles, I.; Matos, J.; Blanc, A.", "Influence of step height on turbulence statistics in the non-aerated skimming flow in steep-stepped spillways", "Water", "17", "22", "3256", "10.3390/w17223256", True),
 (2024, "Lueckel, F. B.; Scott, F.; Aroca, G.", "Comparative techno-economic and carbon footprint analysis of 2,3-butanediol production through aerobic and anaerobic bioconversion of carbon dioxide with green hydrogen", "Chemical Engineering Journal Advances", "20", "", "100659", "10.1016/j.ceja.2024.100659", False),
 (2024, "González, E.; Vera, F.; Scott, F.; Guerrero, C.; Bolívar, J. M.; Aroca, G.; Muñoz, J. Á.; Ladero, M.; Santos, V. E.", "Acidophilic heterotrophs: basic aspects and technological applications", "Frontiers in Microbiology", "15", "", "1374800", "10.3389/fmicb.2024.1374800", False),
 (2024, "Abell, J. A.; Moreno-Casas, P. A.; Recabarren, M.", "Integrating advanced computational skills into engineering education: a discipline-based approach", "Computer Applications in Engineering Education", "32", "6", "e22784", "10.1002/cae.22784", False),
 (2023, "González, E.; Zuleta, C.; Zamora, G.; Maturana, N.; Ponce, B.; Rivero, M. V.; Rodríguez, A.; Soto, J. P.; Scott, F.; Díaz-Barrera, Á.", "Production of poly(3-hydroxybutyrate) and extracellular polymeric substances from glycerol by the acidophile Acidiphilium cryptum", "Extremophiles", "27", "3", "30", "10.1007/s00792-023-01313-3", False),
 (2023, "López, N.; Monte, M.; Iglesias-Juez, A.; Portela, R.; Xuyun, G.; Ye, Z.; Aguila, G.; Araya, P.; Guerrero, S.", "Effect of alkali addition on a Cu/SmCeO2@TiO2 catalyst for NO reduction with CO under oxidizing conditions", "Catalysis Today", "423", "", "114247", "10.1016/j.cattod.2023.114247", False),
 (2022, "Yáñez, L.; Rodríguez, Y.; Scott, F.; Vergara-Fernández, A.; Muñoz, R.", "Production of (R)-3-hydroxybutyric acid from methane by in vivo depolymerization of polyhydroxybutyrate in Methylocystis parvus OBBP", "Bioresource Technology", "353", "", "127141", "10.1016/j.biortech.2022.127141", False),
 (2022, "Araya, B.; Diaz, C.; Martín, J. S.; Vergara-Fernández, A.; Aroca, G.; Scott, F.", "Biodegradation of 2,5-dimethylpyrazine in gas and liquid phase by the fungus Fusarium solani", "Journal of Chemical Technology & Biotechnology", "97", "6", "1408-1415", "10.1002/jctb.6903", False),
 (2022, "Morales-Vera, R.; Vásquez-Ibarra, L.; Scott, F.; Puettmann, M.; Gustafson, R.", "Life cycle assessment of bioethanol production: a case study from poplar biomass growth in the U.S. Pacific Northwest", "Fermentation", "8", "12", "734", "10.3390/fermentation8120734", False),
 (2022, "Moreno-Casas, P. A.; Toro, J. P.; Sepúlveda, S.; Abell, J. A.; González, E.; Paik, J.", "The effect of particle concentration on bed particle diffusion in dilute flows", "Water", "14", "19", "3105", "10.3390/w14193105", False),
 (2021, "Scott, F.; Yañez, L.; Conejeros, R.; Araya, B.; Vergara-Fernández, A.", "Two internal bottlenecks cause the overflow metabolism leading to poly(3-hydroxybutyrate) production in Azohydromonas lata DSM1123", "Journal of Environmental Chemical Engineering", "9", "4", "105665", "10.1016/j.jece.2021.105665", False),
 (2021, "Aguirre, A.; Gentina, J. C.; Malhautier, L.; Fanlo, J.; Vergara-Fernandez, A.; Scott, F.; Aroca, G.", "Characterization of the microbial community in a biotrickling filter treating a complex mixture of gaseous compounds causing odor nuisance", "Journal of Chemical Technology & Biotechnology", "96", "6", "1720-1731", "10.1002/jctb.6697", False),
 (2021, "Nolasco, E.; Vassiliadis, V. S.; Kähm, W.; Adloor, S. D.; Ismaili, R. A.; Conejeros, R.; Espaas, T.; Gangadharan, N.; Mappas, V.; Scott, F.; Zhang, Q.", "Optimal control in chemical engineering: past, present and future", "Computers & Chemical Engineering", "155", "", "107528", "10.1016/j.compchemeng.2021.107528", True),
 (2021, "Núñez-Montero, K.; Salazar, R.; Santos, A.; Gómez-Espinoza, O.; Farah, S.; Troncoso, C.; Hoffmann, C.; Melivilu, D.; Scott, F.; Barrientos Díaz, L.", "Antarctic Rahnella inusitata: a producer of cold-stable β-galactosidase enzymes", "International Journal of Molecular Sciences", "22", "8", "4144", "10.3390/ijms22084144", False),
 (2021, "Sánchez, L.; Aguila, G.; Araya, P.; Quijada, S.; Guerrero, S.", "A highly active Ca/Cu/YCeO2–TiO2 catalyst for the transient reduction of NO with CO and naphthalene under oxidizing conditions", "RSC Advances", "11", "63", "39896-39906", "10.1039/d1ra08412g", False),
 (2021, "Aguila, G.; Calle, R.; Guerrero, S.; Baeza, P.; Araya, P.", "Improvement of thermal stability of highly active species on SiO2 supported copper-ceria catalysts", "RSC Advances", "11", "53", "33271-33275", "10.1039/d1ra06204b", False),
 (2021, "Galano, N.; Moreno-Casas, P. A.; Abell, J. A.", "Extending the Particle Finite Element Method for sediment transport simulation", "Computer Methods in Applied Mechanics and Engineering", "380", "", "113772", "10.1016/j.cma.2021.113772", True),
 (2021, "Paul, A.; Murgadas, S.; Delpiano, J.; Moreno-Casas, P. A.; Walczak, M.; Lopez, M.", "The role of moisture transport mechanisms on the performance of lightweight aggregates in internal curing", "Construction and Building Materials", "268", "", "121191", "10.1016/j.conbuildmat.2020.121191", False),
 (2020, "Vergara-Fernandez, A.; Scott, F.; Carreno-Lopez, F.; Aroca, G.; Moreno-Casas, P.; Gonzalez-Sanchez, A.; Munoz, R.", "A comparative assessment of the performance of fungal-bacterial and fungal biofilters for methane abatement", "Journal of Environmental Chemical Engineering", "8", "5", "104421", "10.1016/j.jece.2020.104421", False),
 (2020, "Yañez, L.; Conejeros, R.; Vergara-Fernández, A.; Scott, F.", "Beyond intracellular accumulation of polyhydroxyalkanoates: chiral hydroxyalkanoic acids and polymer secretion", "Frontiers in Bioengineering and Biotechnology", "8", "", "248", "10.3389/fbioe.2020.00248", False),
 (2020, "Moreno-Casas, P. A.; Scott, F.; Delpiano, J.; Vergara-Fernández, A.", "Computational tomography and CFD simulation of a biofilter treating a toluene, formaldehyde and benzo[α]pyrene vapor mixture", "Chemosphere", "240", "", "124924", "10.1016/j.chemosphere.2019.124924", False),
 (2020, "Moreno-Casas, P. A.; Scott, F.; Delpiano, J.; Abell, J. A.; Caicedo, F.; Muñoz, R.; Vergara-Fernández, A.", "Mechanistic description of convective gas–liquid mass transfer in biotrickling filters using CFD modeling", "Environmental Science & Technology", "54", "1", "419-426", "10.1021/acs.est.9b02662", True),
 (2020, "Carrasco, S.; Silva, J.; Pino-Cortés, E.; Gómez, J.; Vallejo, F.; Díaz-Robles, L.; Campos, V.; Cubillos, F.; Pelz, S.; Paczkowski, S.; Cereceda-Balic, F.; Vergara-Fernández, A.; Lapuerta, M.; Pazo, A.; Monedero, E.; Hoekman, K.", "Experimental study on hydrothermal carbonization of lignocellulosic biomass with magnesium chloride for solid fuel production", "Processes", "8", "4", "444", "10.3390/pr8040444", False),
 (2020, "Salinas, D.; Guerrero, S.; Campos, C. H.; Bustamante, T. M.; Pecchi, G.", "The effect of the ZrO2 loading in SiO2@ZrO2-CaO catalysts for transesterification reaction", "Materials", "13", "1", "221", "10.3390/ma13010221", False),
]

# ---- Huiliñir 2020–2022 (Crossref, query.author) ----
HUILINIR_2020_2022 = [
 (2022, "Castillo, A.; Ortega-Martínez, E.; Pagés-Díaz, J.; Montalvo, S.; Huiliñir, C.", "Micro-aerobic pre-treatment vs. thermal pre-treatment of waste activated sludge for its subsequent anaerobic digestion in semi-continuous digesters: a comparative study", "Fermentation", "8", "10", "565", "10.3390/fermentation8100565", False),
 (2022, "Barahona, A.; Rubio, J.; Gómez, R.; Huiliñir, C.; Borja, R.; Guerrero, L.", "Sequential nitrification–autotrophic denitrification using sulfur as an electron donor and Chilean zeolite as microbial support", "Water", "15", "1", "95", "10.3390/w15010095", False),
 (2022, "Murillo, H. A.; Pagés-Díaz, J.; Díaz-Robles, L. A.; Vallejo, F.; Huiliñir, C.", "Valorization of oat husk by hydrothermal carbonization: optimization of process parameters and anaerobic digestion of spent liquors", "Bioresource Technology", "343", "", "126112", "10.1016/j.biortech.2021.126112", False),
 (2022, "Lauzurique, Y.; Fermoso, F. G.; Sánchez, N.; Castillo, A.; Salazar, R.; García, V.; Huiliñir, C.", "Biogas production from winery wastewater: effect of the substrate-inoculum ratio on fly ash addition and iron availability", "Journal of Water Process Engineering", "47", "", "102826", "10.1016/j.jwpe.2022.102826", False),
 (2022, "Lauzurique, Y.; Espinoza, L. C.; Huiliñir, C.; García, V.; Salazar, R.", "Anodic oxidation of industrial winery wastewater using different anodes", "Water", "14", "1", "95", "10.3390/w14010095", False),
 (2021, "Yánez, D.; Guerrero, L.; Borja, R.; Huiliñir, C.", "Sulfur-based mixotrophic denitrification with the stoichiometric S0/N ratio and methanol supplementation: effect of the C/N ratio on the process", "Journal of Environmental Science and Health, Part A", "56", "13", "1420-1427", "10.1080/10934529.2021.2004839", False),
 (2021, "Lauzurique, Y.; Montalvo, S.; Salazar, R.; García, V.; Huiliñir, C.", "Fly ash from coal combustion as improver of anaerobic digestion: a review", "Journal of Environmental Chemical Engineering", "9", "6", "106422", "10.1016/j.jece.2021.106422", False),
 (2021, "Palominos, N.; Castillo, A.; Guerrero, L.; Borja, R.; Huiliñir, C.", "Coupling of anaerobic digestion and struvite precipitation in the same reactor: effect of zeolite and bischofite as Mg2+ source", "Frontiers in Environmental Science", "9", "", "706730", "10.3389/fenvs.2021.706730", False),
 (2021, "Huiliñir, C.; Fuentes, V.; Estuardo, C.; Antileo, C.; Pino-Cortés, E.", "Partial nitrification in a sequencing moving bed biofilm reactor (SMBBR) with zeolite as biomass carrier: effect of sulfide pulses and organic matter presence", "Water", "13", "18", "2484", "10.3390/w13182484", False),
 (2021, "Lauzurique, Y.; Fermoso, F. G.; Sánchez, N.; Castillo, A.; Valdés, N.; Tello, M.; Salazar, R.; García, V.; Huiliñir, C.", "Effect of the addition of fly ash on the specific methane production and microbial communities in the anaerobic digestion of real winery wastewater", "Journal of Chemical Technology & Biotechnology", "96", "10", "2882-2890", "10.1002/jctb.6840", False),
 (2021, "Pérez-Pérez, T.; Pereda-Reyes, I.; Correia, G. T.; Pozzi, E.; Kwong, W. H.; Oliva-Merencio, D.; Zaiat, M.; Montalvo, S.; Huiliñir, C.", "Performance of EGSB reactor using natural zeolite as support for treatment of synthetic swine wastewater", "Journal of Environmental Chemical Engineering", "9", "1", "104922", "10.1016/j.jece.2020.104922", False),
 (2020, "Pagés-Díaz, J.; Huiliñir, C.", "Valorization of the liquid fraction of co-hydrothermal carbonization of mixed biomass by anaerobic digestion: effect of the substrate to inoculum ratio and hydrochar addition", "Bioresource Technology", "317", "", "123989", "10.1016/j.biortech.2020.123989", False),
 (2020, "Huiliñir, C.; Fuentes, V.; Esposito, G.; Montalvo, S.; Guerrero, L.", "Nitrification in the presence of sulfide and organic matter in a sequencing moving bed biofilm reactor (SMBBR) with zeolite as biomass carrier", "Journal of Chemical Technology & Biotechnology", "95", "5", "1614", "10.1002/jctb.6346", False),
 (2020, "Montalvo, S.; Huiliñir, C.; Castillo, A.; Pagés-Díaz, J.; Guerrero, L.", "Carbon, nitrogen and phosphorus recovery from liquid swine wastes: a review", "Journal of Chemical Technology & Biotechnology", "95", "9", "2335-2347", "10.1002/jctb.6336", False),
 (2020, "Montalvo, S.; Huiliñir, C.; Borja, R.; Sánchez, E.; Herrmann, C.", "Application of zeolites for biological treatment processes of solid wastes and wastewaters – a review", "Bioresource Technology", "301", "", "122808", "10.1016/j.biortech.2020.122808", True),
 (2020, "Pino-Cortés, E.; Montalvo, S.; Huiliñir, C.; Cubillos, F.; Gacitúa, J.", "Characteristics and treatment of wastewater from the mercaptan oxidation process: a comprehensive review", "Processes", "8", "4", "425", "10.3390/pr8040425", False),
 (2020, "Montalvo, S.; Martinez, J.; Castillo, A.; Huiliñir, C.; Borja, R.; García, V.; Salazar, R.", "Sustainable energy for a winery through biogas production and its utilization: a Chilean case study", "Sustainable Energy Technologies and Assessments", "37", "", "100640", "10.1016/j.seta.2020.100640", False),
 (2020, "Acosta-Cordero, L.; Carrera-Chapela, F.; Montalvo, S.; Guerrero, L.; Palominos, N.; Borja, R.; Huiliñir, C.", "Modeling of the effect of zeolite concentration on the biological nitrification process in the presence of sulfide and organic matter", "Journal of Environmental Science and Health, Part A", "56", "1", "1-12", "10.1080/10934529.2020.1852011", False),
 (2020, "Huiliñir, C.; Acosta, L.; Yanez, D.; Montalvo, S.; Esposito, G.; Retamales, G.; Levicán, G.; Guerrero, L.", "Elemental sulfur-based autotrophic denitrification in stoichiometric S0/N ratio: calibration and validation of a kinetic model", "Bioresource Technology", "307", "", "123229", "10.1016/j.biortech.2020.123229", True),
]

def entrada(t):
    year, authors, title, journal, vol, issue, page, doi, featured = t
    authors = limpia(authors).replace("; ", ", ")
    return {"areas": areas_de(authors), "year": year, "authors": authors, "title": limpia(title),
            "journal": journal, "details": det(vol, issue, page), "doi": doi, "featured": featured}

def yml(e):
    q = lambda s: '"' + str(s).replace('\\', '\\\\').replace('"', '\\"') + '"'
    return ("  - areas: [%s]\n    year: %d\n    authors: %s\n    title: %s\n    journal: %s\n    details: %s\n    doi: %s\n    featured: %s\n"
            % (", ".join(e["areas"]), e["year"], q(e["authors"]), q(e["title"]), q(e["journal"]), q(e.get("details", "")), q(e.get("doi", "")), "true" if e.get("featured") else "false"))

aguas = yaml.safe_load(io.open(AGUAS, encoding="utf-8"))
vistos = set()
bloque_aguas, bloque_nuevas, bloque_cesar = [], [], []
for e in aguas["indexed"]:
    e = dict(e); e["authors"] = limpia(e["authors"]); e["title"] = limpia(e["title"])
    e["areas"] = sorted(set(["aguas"] + areas_de(e["authors"])), key=ORDEN.index)
    vistos.add((e.get("doi") or e["title"]).lower()); bloque_aguas.append(e)
for t in NUEVAS:
    e = entrada(t)
    if e["doi"].lower() in vistos: continue
    vistos.add(e["doi"].lower()); bloque_nuevas.append(e)
for t in HUILINIR_2020_2022:
    e = entrada(t)
    if e["doi"].lower() in vistos: continue
    vistos.add(e["doi"].lower()); bloque_cesar.append(e)

orden = lambda L: sorted(L, key=lambda e: (-e["year"], e["authors"]))
group = ["Carreño-López", "Carreno-Lopez", "Huiliñir", "Quezada-Cáceres", "Roa",
         "Vergara-Fernández", "Vergara-Fernandez", "Scott, F.", "Guerrero, S.", "Moreno-Casas"]

out = io.StringIO()
out.write(u"""# Artículos indexados, 2020 a la fecha, de las cinco áreas.
#
# Cada entrada:
#   - areas: [ids]        un paper con dos PI lleva las dos áreas y aparece en ambas
#     year, authors, title, journal, details, doi, featured
#
# Origen (barrido del 14-09-2026):
#   · bloque 1: las del sitio de aguas (2023+), con `aguas` más el área de cualquier
#     otro PI que firme; se mantienen sincronizadas con herramientas/migrar-aguas.rb
#   · bloque 2: Vergara, Scott, Guerrero y Moreno, 2020–2026, desde sus perfiles de
#     Google Scholar contrastados con Crossref (DOI, autores completos, revista)
#   · bloque 3: Huiliñir 2020–2022 (Crossref). OJO: el sitio de aguas las excluye a
#     propósito porque son de su etapa anterior a G-Tech. Si se decide lo mismo acá,
#     basta borrar el bloque 3 completo.
#
# Se dejaron fuera patentes, capítulos de libro, preprints (SSRN), actas y corrigenda.
# group_authors marca en negrita los apellidos del grupo en la lista de autores.
# Al sumar un PI nuevo hay que agregar su apellido acá.

group_authors:
""")
for g in group: out.write(u'  - "%s"\n' % g)
out.write(u"\nindexed:\n")
out.write(u"  # ---- bloque 1: publicaciones del sitio de aguas (2023+) ----\n")
for e in orden(bloque_aguas): out.write(yml(e) + "\n")
out.write(u"  # ---- bloque 2: Vergara / Scott / Guerrero / Moreno, 2020–2026 ----\n")
for e in orden(bloque_nuevas): out.write(yml(e) + "\n")
out.write(u"  # ---- bloque 3: Huiliñir 2020–2022 (etapa previa a G-Tech; ver nota arriba) ----\n")
for e in orden(bloque_cesar): out.write(yml(e) + "\n")
io.open(DEST, "w", encoding="utf-8").write(out.getvalue())

d = yaml.safe_load(io.open(DEST, encoding="utf-8"))
from collections import Counter
c = Counter(a for e in d["indexed"] for a in e["areas"])
print("total:", len(d["indexed"]), "| aguas:", len(bloque_aguas), "nuevas:", len(bloque_nuevas), "césar 20-22:", len(bloque_cesar))
print("por área:", dict(c))
print("sin área:", [e["title"][:50] for e in d["indexed"] if not e["areas"]])
print("por año:", dict(sorted(Counter(e["year"] for e in d["indexed"]).items(), reverse=True)))
