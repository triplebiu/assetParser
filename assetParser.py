import os
import argparse
import re
from netaddr import *

def find_allurl(rawinput):
    isurl = re.compile(
        r'(https?://[\w\.-]+(:\d+)?([\w!@#$%^&*\(\)_+=\[\]\{\}\\\|;:,\./\?-]*)?)')
    allurl = re.findall(isurl, rawinput)
    return allurl

def find_alldomain(rawinput):
    isdomain = re.compile(
        r'([\w\.-]+\.(cn|com|net|top|io|org|info|vip|xyz))')
    alldomain = re.findall(isdomain, rawinput)
    return alldomain

def find_allip(rawinput):
    isip = re.compile(
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/\d{1,3}|\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}-\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}-\d{1,3}|\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}s(?:\,\d{1,3})+')
    allip = re.findall(isip, rawinput)
    return allip

def doextraction(inputFile, ispathsplit):
    filePath,fileName=os.path.split(inputFile)
    fname = fileName[:fileName.rfind(".")]
    fileContent = ""
    with open(inputFile) as rawf:
        fileContent = rawf.read()
    
    # 提取IP
    ipf = os.path.join(filePath,fname+"_ip.txt")
    ipset = set()
    with open(ipf,"w",encoding='utf-8') as f:
        rawiplist = find_allip(fileContent)
        for rawip in rawiplist:
            tmp = re.search(r'^(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})-(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})$',rawip)
            if tmp:
                try:
                    _ = IPNetwork(tmp[1])
                    _ = IPNetwork(tmp[2])
                    for item in iter_iprange(tmp[1],tmp[2]):
                        if str(item) not in ipset:
                            ipset.add(str(item))
                            f.write("%s\n"%str(item).split("/")[0])
                    continue
                except:
                    print("invalid IP: %s"%tmp[0])
            tmp = re.search(r'^(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})-(\d{1,3})$',rawip)
            if tmp:
                try:
                    _ = IPNetwork(tmp[1])
                    _ = IPNetwork(tmp[1][:tmp[1].rfind(".")]+".%s"%tmp[2])
                    for i in iter_iprange(tmp[1],tmp[1][:tmp[1].rfind(".")]+".%s"%tmp[2]):
                        if str(item) not in ipset:
                            ipset.add(str(item))
                            f.write("%s\n"%str(item).split("/")[0])

                    continue
                except:
                    print("invalid IP: %s"%tmp[0])
            tmp = re.search(r'^(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/\d{1,2})$',rawip)
            if tmp:
                try:
                    for i in IPNetwork(tmp[1]):
                        if str(item) not in ipset:
                            ipset.add(str(item))
                            f.write("%s\n"%str(item).split("/")[0])
                    continue
                except:
                    print("invalid IP: %s"%tmp[0])
            tmp = re.search(r'^(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})$',rawip)
            if tmp:
                try:
                    item = IPNetwork(tmp[1])
                    if str(item) not in ipset:
                        ipset.add(str(item))
                        f.write("%s\n"%str(item).split("/")[0])
                        # f.write("%s\n"%str(item))
                    continue
                except:
                    print("invalid IP: %s"%tmp[0])
    print("\nextract %5d  IPs     to %s"%(len(ipset),ipf))

    # 提取域名
    domainf = os.path.join(filePath,fname+"_domain.txt")
    domainset = set()
    with open(domainf,"w",encoding='utf-8') as f:
        rawdomainlist = find_alldomain(fileContent)
        for item,_ in rawdomainlist:
            if item not in domainset:
                domainset.add(item)
                f.write("%s\n"%item)
    print("\nextract %5d  DOMAINs to %s"%(len(domainset),domainf))

    # 提取url
    urlf = os.path.join(filePath,fname+"_url.txt")

    if ispathsplit:
        urlf = os.path.join(filePath,fname+"_url_pathsplited.txt")

    urlset = set()
    with open(urlf,"w",encoding='utf-8') as f:
        rawurllist = find_allurl(fileContent)
        for item in rawurllist:
            item = item[0]

            if item not in urlset:
                urlset.add(item)
                f.write("%s\n"%item)

            if ispathsplit:
                tmp = 999
                if -1< item.find('?') < tmp:
                    tmp = item.find('?')
                if -1< item.find('#') < tmp:
                    tmp = item.find('#')
                item = item[:tmp]
                tmp = re.search(r'(https?:/)(.*)',item)
                urltmp = tmp[1]
                for segment in tmp[2].split("/"):
                    if segment != "":
                        urltmp += "/"+segment
                        if urltmp not in urlset:
                            urlset.add(urltmp)
                            f.write("%s\n"%urltmp)
    print("\nextract %5d  URLs    to %s"%(len(urlset),urlf))
    print()

def main():
    parser=argparse.ArgumentParser()

    parser.add_argument('-f',dest="rawinputfile",required=True,help="Raw Input File")

    # parser.add_argument('--ip',dest='ipoutfile',help="Extract ips to the file")
    # parser.add_argument('--domain',dest="domainoutfile",help="Extract domain to the file")
    # parser.add_argument('--url',dest='urloutfile',help="Extract url to the file")

    parser.add_argument('--pathsplit', dest='pathsplit', action="store_true", default=False, help="is split url path")

    args=parser.parse_args()

    if os.path.exists(args.rawinputfile):
        doextraction(args.rawinputfile, args.pathsplit)
    else:
        print("文件不存在")

if __name__ == '__main__':
    main()