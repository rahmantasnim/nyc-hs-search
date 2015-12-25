import sqlite3


def peek_field_indices(src_file):
    with open(src_file) as f:
        schema= {}
        for idx, field in enumerate(f.readline().split('|')):
            schema[field] = idx
    return schema


def decide_dress_code(input):
    l_input = input.lower()
    if "uniform required" in l_input or "dress code required" in l_input:
        return 1
    return 0


def parse_line(line, schema):
    info = line.split('|')
    parsed_info= []
    parsed_info.append(info[schema["dbn"]])
    parsed_info.append(info[schema["school_name"]])
    parsed_info.append(info[schema["phone_number"]])
    parsed_info.append(info[schema["fax_number"]])
    parsed_info.append(info[schema["school_email"]])
    parsed_info.append(1 if "Yes"==info[schema["shared_space"]] else 0)
    parsed_info.append(info[schema["primary_address_line_1"]])
    parsed_info.append(int(info[schema["zip"]]))
    parsed_info.append(info[schema["website"]])
    parsed_info.append(int(info[schema["total_students"]]))
    parsed_info.append(decide_dress_code(info[schema["addtl_info2"]]))
    parsed_info.append(info[schema["start_time"]])
    parsed_info.append(info[schema["end_time"]])
    parsed_info.append(0 if "Not" in info[schema["school_accessibility_description"]] else 1)
    return tuple(parsed_info)


def simple_import(db_file, src_file):
    conn = sqlite3.connect(db_file)
    c = conn.cursor()

    schema = peek_field_indices(src_file)

    with open(src_file) as f:
        f.readline() # skipping first line containing fields
        for line in f:
            c.execute('''INSERT INTO Schools
                        %s, %s, %s, %s, %s, %d, %s, %d, %s, %d, %d, %s, %s, %d'''
                      % parse_line(line, schema))

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
    simple_import("db", "src")
    return

if __name__ == '__main__':
    main()