import re
def extractimage(list):
    chl = [];
    ele = [];
    resultdict = [];
    tempdict = {};
    str2 = "";
    i = 0;
    numberofcha = 0;
    pattern = re.compile(r"\((.*?)\)", re.I | re.X)
    print list
    for item in list:
        # we should analysis the image info string into a imageInfo_dict
        str1 = str(item);
        # print str1;
        str1 = pattern.findall(str1);
        for fomula in str1:
            formula = re.split(", ", fomula);
            numberofcha = fomula.count("=");
            # print numberofcha;
            for words in formula:
                words = re.split("=", words);
                # print words
                for word in words:
                    if (i % 2 == 0):
                        chl.append(word);
                    else:
                        ele.append(word);
                    i = i + 1;
    for i in range(0, len(chl) - 1):
        tempdict.setdefault(chl[i], ele[i]);
        if (i % numberofcha == 0 and i != 0):
            # print tempdict;
            resultdict.append(tempdict);
            tempdict = {};
    # print imagelist;
    # for item in resultdict:
    #    print item;
    return resultdict


def extractfirst(list):
    # print list
    start = 0;
    end = 0;
    eqf = False;
    eqb = False;
    chl = [];
    ele = [];
    tempdict = {};
    resultdict = [];
    for item in list:
        # print item
        str1 = str(item)
        # print str1
        for i in range(0, len(str1)):
            # print i;
            if (str1[i] == "("):
                start = i;
                # print start
            if (str1[i] == ")"):
                end = i;
        str2 = str1[start + 1:end].strip();
        # print str2
        # print start
        start = 0;
        # print len(str2)
        for j in range(0, len(str2)):
            if (str2[j] == "="):
                # print j
                if (start == 0):
                    # print "chl = "+str2[start:j];
                    chl.append(str2[start:j])
                    start = j + 1;
                else:
                    for k in range(start, j)[::-1]:
                        # print k
                        # print j
                        if (str2[k] == "," or str2[k] == ")"):
                            if (len(ele) >= 1):
                                for l in range(start, k):
                                    if (str2[l] == "="):
                                        # print "chl = " + str2[start:l];
                                        chl.append(str2[start:l]);
                                        # print "ele = " + str2[l+1:k];
                                        # print k
                                        ele.append(str2[l + 1:k]);
                                        break;
                            else:
                                # print "ele = "+str2[start:k]
                                ele.append(str2[start:k]);
                            start = k + 2;
                            # print str2[start];
                            break;

        for k in range(start, len(str2)):
            if (str2[k] == "="):
                # print "chl = " + str2[start:k];
                chl.append(str2[start:k]);
                # print "ele = " + str2[k+1:len(str2)];
                ele.append(str2[k + 1:len(str2)]);
                break;

        for j in range(0, len(ele)):
            tempdict.setdefault(chl[j], ele[j]);
        resultdict.append(tempdict);
        tempdict = {};
        chl = [];
        ele = [];
        # break;
    return resultdict;


def extractnetwork(list):
    start = 0;
    end = 0;
    result2 = [];
    result1 = extractfirst(list);
    result3 = [];
    result4 = [];
    dict1 = {};

    '''
    for item in result1:
        print item.__getitem__("attrs")
        '''
    tempdict = {};

    chl = [];
    ele = [];
    count = 0;
    s = 0;
    for item in result1:
        str1 = str(item.__getitem__("attrs"));

        for i in range(0, len(str1)):
            if (str1[i] == "{"):
                start = i;
            if (str1[i] == "}"):
                end = i;

        str2 = str1[start + 1:end];
        str3 = str2.split(",")
        count = 0
        for formula in str3:
            words = formula.split(":");
            # print "words"+str(words)
            for word in words:
                if (count % 2 == 0):
                    chl.append(word.replace("u'", "").replace("'", "").strip());
                    # print word
                else:
                    ele.append(word.replace("u'", "").replace("'", "").replace("}]", "").strip());
                count += 1;

        # print len(chl)
        for j in range(0, len(chl) - 1):
            # print j
            tempdict.setdefault(chl[j], ele[j]);

        dict1.setdefault("attrs", tempdict);
        dict1.setdefault("loaded", item.__getitem__("loaded"));

        result2.append(dict1);

        tempdict = {};
        chl = [];
        ele = [];
        dict1 = {};
        dict2 = {};

    return result2;


#[{'loaded': 'True', 'attrs': {'end': '10.0.5.254', 'start': '10.0.5.2', 'host_routes': '[]', 'ipv6_address_mode': 'None', 'ip_version': '4', 'gateway_ip': '10.0.5.1', 'cidr': '10.0.5.0/24', 'id': 'e9a98c9a-67af-4727-a3ee-57c3b1098c49'}},
# {'loaded': 'True', 'attrs': {'end': '172.16.1.254', 'start': '172.16.1.2', 'host_routes': '[]', 'ipv6_address_mode': 'None', 'ip_version': '4', 'gateway_ip': '172.16.1.1', 'cidr': '172.16.1.0/24', 'id': '5373d01b-8f59-4f2c-9a0c-6936d44e9dc0'}},
# {'loaded': 'True', 'attrs': {'end': '202.112.113.240', 'start': '202.112.113.224', 'host_routes': '[]', 'ipv6_address_mode': 'None', 'ip_version': '4', 'gateway_ip': '202.112.113.1', 'cidr': '202.112.113.0/24', 'id': 'ce500f45-b8f9-42fa-a9e5-cd31b04b4822'}},
# {'loaded': 'True', 'attrs': {'end': '172.16.1.254', 'start': '172.16.1.2', 'host_routes': '[]', 'ipv6_address_mode': 'None', 'ip_version': '4', 'gateway_ip': '172.16.1.1', 'cidr': '172.16.1.0/24', 'id': 'e7d4b480-94d7-45dc-80e4-34c027b4cd33'}},
# {'loaded': 'True', 'attrs': {'end': '172.16.1.254', 'start': '172.16.1.2', 'host_routes': '[]', 'ipv6_address_mode': 'None', 'ip_version': '4', 'gateway_ip': '172.16.1.1', 'cidr': '172.16.1.0/24', 'id': '611d2a64-b694-4b9d-a409-439598a234f8'}},
# {'loaded': 'True', 'attrs': {'end': '172.16.1.254', 'start': '172.16.1.2', 'host_routes': '[]', 'ipv6_address_mode': 'None', 'ip_version': '4', 'gateway_ip': '172.16.1.1', 'cidr': '172.16.1.0/24', 'id': '7035afbc-c47e-48c8-a8c2-214f3e3b2fb2'}},
# {'loaded': 'True', 'attrs': {'end': '172.17.1.254', 'start': '172.17.1.2', 'host_routes': '[]', 'ipv6_address_mode': 'None', 'ip_version': '4', 'gateway_ip': '172.17.1.1', 'cidr': '172.17.1.0/24', 'id': '26c23852-121f-4766-8592-f334dbc26e8a'}},
# {'loaded': 'True', 'attrs': {'end': '172.16.2.254', 'start': '172.16.2.2', 'host_routes': '[]', 'ipv6_address_mode': 'None', 'ip_version': '4', 'gateway_ip': '172.16.2.1', 'cidr': '172.16.2.0/24', 'id': 'b23824dc-6a52-4732-be2f-c67ea11f516f'}},
# {'loaded': 'True', 'attrs': {'end': '192.168.230.254', 'start': '192.168.230.2', 'host_routes': '[]', 'ipv6_address_mode': 'None', 'ip_version': '4', 'gateway_ip': '192.168.230.1', 'cidr': '192.168.230.0/24', 'id': '3e531dec-84a2-4dff-9c76-0703f4e8b0ba'}},
# {'loaded': 'True', 'attrs': {'end': '172.16.2.254', 'start': '172.16.2.2', 'host_routes': '[]', 'ipv6_address_mode': 'None', 'ip_version': '4', 'gateway_ip': '172.16.2.1', 'cidr': '172.16.2.0/24', 'id': 'b70ae15d-e763-43de-a88d-a5823647aa49'}}]
