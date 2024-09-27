from SqliInjection.units import checknet
from SqliInjection.units import url
from SqliInjection.units import banner
import argparse
from SqliInjection.includes import scan
from SqliInjection.includes import file
import webbrowser


parser = argparse.ArgumentParser()
parser.add_argument("-u","--url",help="Enter target url ")
parser.add_argument("-l","--list",help="Enter File name")
parser.add_argument("-o","--output",help="Enter Output File name")
parser.add_argument('-b','--blog',action="store_true",help="For more info about the cve")

args = parser.parse_args()

def main():
    if args.url:
        banner.banner()
        scan.sqlscan(args.url,args.output)
    if args.list:
        banner.banner()
        file.reader(args.list,args.output)
    if args.blog:
        webbrowser.open(url.data.blog)

if __name__ == "__main__":
    if checknet.net():
        main()
    else:
        print("Check Internet")