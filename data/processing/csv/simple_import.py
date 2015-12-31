import sqlite3  # xtra_curr_processing


def peek_field_indices(src_file):
    with open(src_file) as f:
        schema = {}
        for idx, field in enumerate(f.readline().split('|')):
            schema[field] = idx
    return schema


def decide_dress_code(inp):
    l_input = inp.lower()
    if "uniform required" in l_input or "dress code required" in l_input:
        return 1
    return 0


def parse_school_info(info, schema):
    parsed_info = []
    parsed_info.append(info[schema["dbn"]])
    parsed_info.append(info[schema["school_name"]])
    parsed_info.append(info[schema["phone_number"]])
    parsed_info.append(info[schema["fax_number"]])
    parsed_info.append(info[schema["school_email"]])
    parsed_info.append(1 if "Yes" == info[schema["shared_space"]] else 0)
    parsed_info.append(info[schema["primary_address_line_1"]])
    parsed_info.append(int(info[schema["zip"]]))
    parsed_info.append(info[schema["website"]])
    parsed_info.append(int(info[schema["total_students"]]))
    parsed_info.append(decide_dress_code(info[schema["addtl_info2"]]))
    parsed_info.append(info[schema["start_time"]])
    parsed_info.append(info[schema["end_time"]])
    parsed_info.append(0 if "Not" in info[schema["school_accessibility_description"]] else 1)
    return tuple(parsed_info)


def general_insert(c, dbn, table, value, join_table):
    c.execute("""SELECT id FROM %s WHERE title = '%s';"""
              % (table, value))
    value_info = c.fetchone()
    if not value_info:
        c.execute("""INSERT INTO %s (title) VALUES
                  ('%s');""" % (table, value))
        c.execute("""SELECT id FROM %s WHERE title = '%s';"""
                  % (table, value))
        value_info = c.fetchone()

    c.execute("""INSERT INTO %s VALUES
               (%d, '%s');""" % (join_table, value_info[0], dbn))


def trains_insert(c, dbn, train, stop):
    if train:
        c.execute("""SELECT id FROM Trains WHERE title = '%s';""" % train)
        train_info = c.fetchone()
        if not train_info:
            c.execute("""INSERT INTO Trains (title) VALUES ('%s');""" % train)
            c.execute("""SELECT id FROM Trains WHERE title = '%s';""" % train)
            train_info = c.fetchone()

        c.execute("""INSERT INTO Train_School VALUES (%d, '%s', '%s');""" % (train_info[0], dbn, stop))


def sports_insert(c, dbn, sports, psal, gender):
    for sport in sports:
        sport = sport.strip()
        if sport:
            c.execute("""SELECT id FROM Sports WHERE title = '%s';""" % sport)
            sport_info = c.fetchone()
            if not sport_info:
                c.execute("""INSERT INTO Sports (title) VALUES ('%s');""" % sport)
                c.execute("""SELECT id FROM Sports WHERE title = '%s';""" % sport)
                sport_info = c.fetchone()

            c.execute("""INSERT INTO School_Sports VALUES
                       (%d, '%s', %d, '%s');""" % (sport_info[0], dbn, psal, gender))


def xtra_curr_insert(c, dbn, xtra):
    words = xtra.split(' ')
    # for w in words:
    #     w = w.lower()
    #     if w in xtra_curr_processing.xtra_curr_keywords:
    #         xtra = xtra_curr_processing.xtra_curr_keywords[w]
    #         break

    general_insert(c, dbn, "Xtra_Curr", xtra, "School_Xtracurr")


def grade_insert(c, dbn, lo, hi):
    for x in range (lo, hi+1):
        c.execute("""INSERT INTO School_Grades VALUES (%d, '%s');""" % (x, dbn))


def simple_import(db_file, src_file):
    conn = sqlite3.connect(db_file)
    c = conn.cursor()

    schema = peek_field_indices(src_file)

    with open(src_file) as f:
        f.readline()    # skipping first line containing fields
        for line in f:
            info = line.replace("'", "''").split("|")
            dbn = info[schema["dbn"]]

            # inserting into schools
            c.execute("""INSERT INTO Schools VALUES
                      ('%s', '%s', '%s', '%s', '%s', %d, '%s',
                      %d, '%s', %d, %d, '%s', '%s', %d);"""
                      % parse_school_info(info, schema))

            # inserting into Buses and Bus_school
            buses = info[schema["bus"]].split(",")
            for bus in buses:
                bus = bus.strip()
                if bus:
                    general_insert(c, dbn, "Buses", bus, "Bus_School")

            # inserting into Trains
            stops = info[schema["subway"]].split(";")
            for stop in stops:
                stop = stop.split("to", 1)
                trains = stop[0].split(",")
                for train in trains:
                    train = train.strip()
                    trains_insert(c, dbn, train, stop[1].strip() if len(stop) == 2 else "NULL")

            # inserting into Grades
            grade_min = info[schema["grade_span_min"]].replace("PK", "-1").replace("K", "0")
            grade_max = info[schema["grade_span_max"]].replace("PK", "-1").replace("K", "0")
            exp_grade_min = info[schema["expgrade_span_min"]].replace("PK", "-1").replace("K", "0")
            exp_grade_max = info[schema["expgrade_span_max"]].replace("PK", "-1").replace("K", "0")

            grade_min = min(int(grade_min), int(exp_grade_min)) if exp_grade_min else int(grade_min)
            grade_max = max(int(grade_max), int(exp_grade_max)) if exp_grade_max else int(grade_max)

            grade_insert(c, dbn, grade_min, grade_max)

            # inserting into School_Types
            school_types = info[schema["school_type"]].split(",")
            for school_type in school_types:
                school_type = school_type.strip()
                general_insert(c, dbn, "School_Types", school_type, "School_Type_School")

            # inserting into Langs
            langs = info[schema["language_classes"]].split(",")
            for lang in langs:
                lang = lang.strip()
                if lang:
                    general_insert(c, dbn, "Langs", lang, "School_Lang")

            # inserting into AP_Classes
            courses = info[schema["advancedplacement_courses"]].split(",")
            for course in courses:
                course = course.strip()
                if course:
                    general_insert(c, dbn, "AP_Classes", course, "School_AP")

            # inserting into Xtra_Curr
            xtras = info[schema["extracurricular_activities"]].split(",")
            for xtra in xtras:
                xtra = xtra.strip()
                if xtra:
                    xtra_curr_insert(c, dbn, xtra)

            # inserting into sports
            sports_girls_psal = info[schema["psal_sports_girls"]].split(",")
            sports_insert(c, dbn, sports_girls_psal, 1, "F")

            sports_boys_psal = info[schema["psal_sports_boys"]].split(",")
            sports_insert(c, dbn, sports_boys_psal, 1, "M")

            sports_coed_psal = info[schema["psal_sports_coed"]].split(",")
            sports_insert(c, dbn, sports_coed_psal, 1, "C")

            sports = info[schema["school_sports"]].split(",")
            sports_insert(c, dbn, sports, 0, "C")   # technically, unknown gender?

            conn.commit()

        conn.close()

    # # Create table
    # c.execute('''CREATE TABLE stocks
    #          (date text, trans text, symbol text, qty real, price real)''')
    #
    # # Insert a row of data
    # c.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")
    #
    # # Save (commit) the changes
    # conn.commit()
    #
    # # We can also close the connection if we are done with it.
    # # Just be sure any changes have been committed or they will be lost.
    # conn.close()
    #
    # # Never do this -- insecure!
    # symbol = 'RHAT'
    # c.execute("SELECT * FROM stocks WHERE symbol = '%s'" % symbol)
    #
    # # Do this instead
    # t = ('RHAT',)
    # c.execute('SELECT * FROM stocks WHERE symbol=?', t)
    # print c.fetchone()
    #
    # # Larger example that inserts many records at a time
    # purchases = [('2006-03-28', 'BUY', 'IBM', 1000, 45.00),
    #              ('2006-04-05', 'BUY', 'MSFT', 1000, 72.00),
    #              ('2006-04-06', 'SELL', 'IBM', 500, 53.00),
    #             ]
    # c.executemany('INSERT INTO stocks VALUES (?,?,?,?,?)', purchases)


def main():
    simple_import("../../db/nyc_hs_dir.db", "../../src/DOE_High_School_Directory_2016.csv")
    return

if __name__ == '__main__':
    main()