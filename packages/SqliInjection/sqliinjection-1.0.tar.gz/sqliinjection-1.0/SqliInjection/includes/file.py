from SqliInjection.includes import scan
def reader(input,output):
    try:
        with open(input,'r') as file:
            for line in file:
                scan.sqlscan(line.strip(),output)
    except FileNotFoundError:
        print("File not found. check the file path and name")