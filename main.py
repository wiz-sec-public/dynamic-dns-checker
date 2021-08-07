import dns.resolver
import json
import known_tlds


def get_a(domain, server=None):
    try:
        if server:
            my_resolver = dns.resolver.Resolver()
            my_resolver.nameservers = [server]
            answers = my_resolver.resolve(domain, 'A')
        else:
            answers = dns.resolver.resolve(domain, 'A')

        first_level_dns = []
        for rdata in answers:
            first_level_dns.append(str(rdata.to_text()))
        return first_level_dns
    except:
        return []


def get_ns(domain):
    first_level_dns = []
    try:
        answers = dns.resolver.resolve(domain, 'NS')
        first_level_dns = []
        for rdata in answers:
            first_level_dns.append(str(rdata.to_text()))
        return first_level_dns
    except dns.resolver.NXDOMAIN as e:
        for r in e.response(e.qnames()[0]).authority:
            for rr in r:
                first_level_dns.append(str(rr.mname.to_text()))
        return first_level_dns
    except:
        return []


def get_soa(domain, server=None):
    parent_domain = None
    try:
        if server:
            my_resolver = dns.resolver.Resolver()
            my_resolver.nameservers = [server]
            answers = my_resolver.resolve(domain, 'SOA', raise_on_no_answer=False)
        else:
            answers = dns.resolver.resolve(domain, 'SOA', raise_on_no_answer=False)

        for rdata in answers:
            return parent_domain, rdata.mname.to_text()

        for r in answers.response.authority:
            parent_domain = r.name.to_text()
            for rr in r:
                return parent_domain, rr.mname.to_text()

    except dns.resolver.NXDOMAIN as e:
        for r in e.response(e.qnames()[0]).authority:
            parent_domain = r.name.to_text()
            for rr in r:
                return parent_domain, rr.mname.to_text()
    except Exception as e:
        print(e)
        pass
    return None, None


def check_domain(domain):
    results = {
        'master_server': {
            'name': '',
            'ips': []
        },
        'inner_master_servers': [],
        'parent_domain': known_tlds.get_root_domain(domain)
    }

    parent_domain, master_server = get_soa(domain)
    if not master_server:
        return None

    master_server_ips = get_a(master_server)
    results['master_server']['ips'] = master_server_ips
    results['master_server']['name'] = master_server

    # if master_server.lower().endswith(parent_domain.lower()):
    #     return json.dumps(results)

    target_domain = parent_domain if parent_domain else domain
    for nameserver in get_ns(target_domain):
        maybe_soa = get_soa(target_domain, get_a(nameserver)[0])[1]
        maybe_soa_ips = get_a(maybe_soa, get_a(nameserver)[0])
        results['inner_master_servers'].append((nameserver, maybe_soa, maybe_soa_ips))

    return json.dumps(results)


def lambda_handler(event, context):
    try:
        data = event.get('body')
        if not data:
            return {'statusCode': 500, 'body': '500 is for grown ups'}

        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Credentials': True,
            },
            'body': check_domain(data.strip())
        }
    except Exception as e:
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Credentials': True,
            },
            'body': str(e)
        }


if __name__ == "__main__":
    test_domain = input("Domain: ").strip()
    print(test_domain)
    print(lambda_handler({'body': test_domain.strip()}, None))
