from pdf2index import keywords


def test_keyex_abbreviations():
    text = """test text ABC (alternate
    bicycle compressor). with CD(change david) and jo (joint or)"""
    kw = keywords.keyex_abbreviations(text)
    kw_exp = {
        "alternate bicycle compressor (ABC)",
        "CD (change david)",
        "change david (CD)",
        "ABC (alternate bicycle compressor)",
    }
    assert kw == kw_exp


def test_keyex_capitalized():
    text = """This is AN Abbreviation TEST. Will
    it WORK?"""
    kw = keywords.keyex_capitalized(text)
    kw_exp = {"AN", "WORK", "TEST"}
    assert kw == kw_exp


wiki_pages = [
    "",
    "",
    """Single sign-on (SSO) is an authentication scheme that allows a user to
log in with a single ID to any of several related, yet independent, software systems.
True single sign-on allows the user to log in once and access services without re-entering
authentication factors.
""",
    """It should not be confused with same-sign on (Directory Server Authentication), often
accomplished by using the Lightweight Directory Access Protocol (LDAP) and stored LDAP
databases on (directory) servers.[1][2]
A simple version of single sign-on can be achieved over IP networks using cookies but
only if the sites share a common DNS parent domain.[3]
""",
    """For clarity, a distinction is made between Directory Server Authentication (same-sign
on) and single sign-on: Directory Server Authentication refers to systems requiring
authentication for each application but using the same credentials from a directory
server, whereas single sign-on refers to systems where a single authentication
provides access to multiple applications by passing the authentication token
seamlessly to configured applications.
""",
    """Conversely, single sign-off or single log-out (SLO) is the property whereby a single
action of signing out terminates access to multiple software systems.
As different applications and resources support different authentication mechanisms,
single sign-on must internally store the credentials used for initial authentication
and translate them to the credentials required for the different mechanisms.
Other shared authentication schemes, such as OpenID and OpenID Connect, offer other
services that may require users to make choices during a sign-on to a resource, but
can be configured for single sign-on if those other services (such as user consent)
are disabled.[4] An increasing number of federated social logons, like Facebook
Connect, do require the user to enter consent choices upon first registration with a
new resource, and so are not always single sign-on in the strictest sense.""",
]

wikitext = " ".join(wiki_pages)


def test_keyex_keybert_single():
    kw = keywords.keyex_keybert_single(wikitext)
    kw_exp = {
        "connect",
        "logons",
        "shared",
        "dns",
        "configured",
        "signing",
        "domain",
        "access",
        "sso",
        "openid",
        "server",
        "sign",
        "authentication",
        "single",
        "consent",
    }
    assert kw == kw_exp


def test_keyex_keybert_double():
    kw = keywords.keyex_keybert_double(wikitext)
    kw_exp = {
        "sso authentication",
        "different authentication",
        "shared authentication",
        "single authentication",
        "sign sso",
    }
    assert kw == kw_exp


def test_extract_keywords_from_text():
    kw = keywords.extract_keywords_from_text(wikitext)
    kw_exp = {
        "authentication same_sign",
        "DNS",
        "logons",
        "access",
        "single",
        "sign_on",
        "single sign_on",
        "sso authentication",
        "same_sign",
        "sign_on sso",
        "LDAP",
        "connect",
        "SLO",
        "consent",
        "sso",
        "signing",
        "log_out",
        "openid",
        "sign_off",
        "domain",
        "single authentication",
        "SSO",
        "IP",
        "ID",
        "authentication",
        "shared",
    }
    assert kw == kw_exp


def test_extract_keywords_from_text_list():
    kw = keywords.extract_keywords_from_text_list(wiki_pages)
    kw_exp = {
        "access": {2, 3, 4, 5},
        "allows": {2},
        "authentication": {2, 3, 4, 5},
        "authentication same_sign": {4},
        "authentication scheme": {2},
        "clarity": {4},
        "common": {3},
        "common dns": {3},
        "configured": {4},
        "confused same_sign": {3},
        "connect": {5},
        "consent": {5},
        "cookies": {3},
        "credentials": {5},
        "directory": {3, 4},
        "distinction": {4},
        "DNS": {3},
        "dns": {3},
        "dns parent": {3},
        "domain": {3},
        "ID": {2, 5},
        "id": {2},
        "independent": {2},
        "IP": {3},
        "ip": {3},
        "LDAP": {3},
        "ldap": {3},
        "log": {2},
        "log_out": {5},
        "log_out slo": {5},
        "logons": {5},
        "multiple": {4},
        "networks": {3},
        "openid": {5},
        "re_entering": {2},
        "refers": {4},
        "requiring": {4},
        "same_sign": {3, 4},
        "same_sign directory": {3},
        "same_sign single": {4},
        "scheme": {2},
        "server": {3, 4},
        "server authentication": {4},
        "server single": {4},
        "servers": {3},
        "services": {2},
        "shared": {5},
        "shared authentication": {5},
        "sign_off": {5},
        "sign_off single": {5},
        "sign_on": {2, 3, 4, 5},
        "sign_on allows": {2},
        "sign_on sso": {2},
        "signing": {5},
        "single": {2, 3, 4},
        "single authentication": {4},
        "single sign_off": {5},
        "single sign_on": {2, 3, 5},
        "SLO": {5},
        "slo": {5},
        "software": {2},
        "SSO": {2},
        "sso": {2},
        "sso authentication": {2},
        "systems": {2, 4},
        "user": {2, 5},
        "users": {5},
        "using": {4},
    }
    assert kw == kw_exp
