from ConfigParser import SafeConfigParser
def get_list(filename, section, option):
    parser = SafeConfigParser()
    parser.read(filename)
    value = parser.get(section, option)
    return list(filter(None, (x.strip() for x in value.splitlines())))

if __name__ == "__main__":
    print get_list('config.ini', 'Domains', 'devDomainList')
    print get_list('config.ini', 'Domains', 'idcDomainList')
