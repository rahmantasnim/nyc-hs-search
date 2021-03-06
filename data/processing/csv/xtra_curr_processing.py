import numpy as np #from numpy package
import sklearn.cluster  # from sklearn package
import distance #from distance package
import simple_import
from fuzzywuzzy import fuzz



"""
REDUCED LIST OF EXTRACURRICULARS

01. Student Government
02. Yearbook
03. Dance (salsa
04. Chess
05. Drama (Theater)
06. Academic Societies (honor society, arista)
07. Art (visual Arts, studio art, mural painting)
08. Robotics
09. Tutoring (SAT prep, homework help, regents prep)
10. Photography (Digitial)
11. Music ??? (Glee)
12. Cheerleading
13. Model UN
14. Peer Mediation (conflict resolution)
15. Chorus, Choir
16. Jounalism
17. Anime
18. Mock Trial
19. Step Team
20. Debate Team
21. Community Service (Key, red cross)
22. Math Team
23. Literary Magazine
24. Fitness (Yoga, Soccer, Basketball, Swimming)
25. Book
26. Film (filmmaking)
27. Science, science olympiad
28. Band (Guitar)
29. Poetry, Creative Writing, Spoken Word
30. Tech (Computer, computer programming, MOUSE squad)
31. Gay Straight Alliance
32. Mentoring
33. Cooking (Culinary Arts)
34. Fashion (fashion design
35. Video Game
36. Environmental Club
37. MSA
"""

xtra_curr_keywords = { "government": "Student Government/Council",
                       "council": "Student Government/Council",
                       "leadership": "Leadership Orgs",
                       "yearbook": "Yearbook",
                       "dance": "Dance",
                       "chess": "Chess",
                       "drama": "Drama/Theater",
                       "theater": "Drama/Theater",
                       "theatre": "Drama/Theater",
                       "honor": "Academic Society",
                       "honors": "Academic Society",
                       "arista": "Academic Society",
                       "art": "Art",
                       "visual": "Art",
                       "painting": "Art",
                       "robotics": "Robotics",
                       "tutoring": "Tutoring/Prep",
                       "prep": "Tutoring/Prep",
                       "preparation": "Tutoring/Prep",
                       "homework": "Tutoring/Prep",
                       "photography": "Photography",
                       "photo": "Photography",
                       "music": "Music",
                       "cheerleading": "Cheerleading",
                       # "model un": "Model UN",    # this is a problem,
                       "mediation": "Conflict Resolution",
                       "conflict": "Conflict Resolution",
                       "mediation/conflict": "Conflict Resolution",
                       "chorus": "Chorus",
                       "choir": "Chorus",
                       "glee": "Chorus",
                       "newspaper": "Journalism",
                       "journalism": "Journalism",
                       "anime": "Anime",
                       "trial": "Mock Trial",
                       "step": "Step Team",
                       "debate": "Debate Team",
                       "key": "Community Service",
                       "service": "Community Service",
                       # "red cross" "Community Service",   #this is a problem
                       "math": "Math Team",
                       "magazine": "Magazine",
                       "fitness": "Fitness",
                       # "", include all other sports here?
                       "book": "Book Club",
                       "science": "Science",
                       "film": "Film",
                       "filmmaking": "Film",
                       "band": "Band",
                       # other instruments?
                       # poetry?, spoken word? creative writing?
                       "writing": "Writing Clubs",
                       "tech": "Technology",
                       "mouse": "Coding",
                       "code": "Coding",
                       "computer": "Coding",
                       "coders": "Coding",
                       "programming": "Coding",
                       "coding": "Coding",
                       "gay": "Gay Straight Alliance",
                       "gay/straight": "Gay Straight Alliance",
                       "gay-straight": "Gay Straight Alliance",
                       "mentoring": "Mentoring",
                       "cooking": "Cooking",
                       "culinary": "Cooking",
                       "fashion": "Fashion",
                       # "video game": ""
                       "environmental": "Environmental Club",
                       "muslim": "Muslim Student Association"
                       }


def collect_xtra_curr(src_file):
    schema = simple_import.peek_field_indices(src_file)
    res = []
    with open(src_file) as f:
        f.readline()
        for line in f:
            line = line.replace("'", "''").split('|')
            xtras = line[schema["extracurricular_activities"]].split(',')
            for xtra in xtras:
                xs = xtra.split(';')
                for x in xs:
                    x = x.strip().lower()
                    if len(x) <= 40:
                        res.append(x)

    return res


def cluster_xtra_curr(xtras, out_file):
    with open(out_file, "w") as f:
        words = set(xtras)
        lev_similarity = -1*np.array([[distance.levenshtein(w1,w2) for w1 in words] for w2 in words])

        affprop = sklearn.cluster.AffinityPropagation(affinity="precomputed", damping=0.5)
        affprop.fit(lev_similarity)
        for cluster_id in np.unique(affprop.labels_):
            exemplar = words[affprop.cluster_centers_indices_[cluster_id]]
            idxs = np.nonzero(affprop.labels_ == cluster_id)[0]
            ws = []
            for idx in idxs:
                ws.append(words[idx])
            cluster = np.unique(ws)
            cluster_str = ", ".join(cluster)
            f.write(" - *%s:* %s\n" % (exemplar, cluster_str))


def count_remove_duplicates(xtras):
    xs = {}
    for x in xtras:
        if x in xs:
            xs[x] += 1
        else:
            xs[x] = 1
    return sorted(xs, key=xs.get, reverse=True)


def minimize_duplicates(xtras, out_file):
    xtras = count_remove_duplicates(xtras)
    res = []

    with open(out_file, 'w') as f:
        for idx, xtra in enumerate(xtras):
            matches = 0
            for canon_xtra in enumerate(res):
                if fuzz.token_set_ratio(canon_xtra, xtra) >= 80:
                    matches += 1
            if matches:
                f.write(xtra + '\n')
                xtras[idx] = ""
            else:
                res.append(xtra)

    return res


def main():
    xtras = collect_xtra_curr("../../src/DOE_High_School_Directory_2016.csv")
    # cluster_xtra_curr(xtras, "xtra_curr_analysis/clustered_xtra_curr_05_all.txt")
    # count_remove_duplicates(xtras)
    print len(minimize_duplicates(xtras, "xtra_curr_analysis/fuzzy_xtra_curr.txt"))


if __name__ == '__main__':
    main()