#!/usr/bin/env python

"""
THIS SCRIPT IS USED FOR EDUCATIONAL PURPOSES ONLY. DO NOT USE IT IN ILLEGAL WAY!!!
"""

import base64
from datetime import datetime
from hashlib import sha1
import zlib
from M2Crypto import DSA


def keymaker(organisation, server_id, license_edition, license_type_name, purchase_date=datetime.today(), private_key='./private.pem'):
    license_types = ('ACADEMIC', 'COMMERCIAL', 'COMMUNITY', 'DEMONSTRATION', 'DEVELOPER', 'NON_PROFIT', 'OPEN_SOURCE', 'PERSONAL', 'STARTER', 'HOSTED', 'TESTING')
    license_editions = ('BASIC', 'STANDARD', 'PROFESSIONAL', 'ENTERPRISE')
    if license_type_name not in license_types:
        raise ValueError('License Type Name must be one of the following values:\n\t%s' % ', '.join(license_types))
    if license_edition not in license_editions:
        raise ValueError('License Edition must be one of the following values:\n\t%s' % ', '.join(license_editions))

    header = purchase_date.ctime()
    properties = {
        # 'Description': 'JIRA\\: Developer',
        # 'CreationDate': purchase_date.strftime('%Y-%m-%d'),
        # 'jira.LicenseEdition': license_edition,
        # 'Evaluation': 'false',
        # 'jira.LicenseTypeName': license_type_name,
        # 'jira.active': 'true',
        # 'licenseVersion': '2',
        # 'MaintenanceExpiryDate': '2099-12-31',
        # 'Organisation': organisation,
        # 'jira.NumberOfUsers': '-1',
        # 'ServerID': server_id,
        # 'SEN': 'SEN-L0000000',
        # 'LicenseID': 'LIDSEN-L0000000',
        # 'LicenseExpiryDate': '2099-12-31',
        # 'PurchaseDate': purchase_date.strftime('%Y-%m-%d')

#        'com.thed.zephyr.je.active':'true',
#        'Description':'Zephyr for JIRA - Test Management for JIRA\: Commercial',
#        'NumberOfUsers':'-1', 
#        'CreationDate': purchase_date.strftime('%Y-%m-%d'),
#        'Evaluation':'false',
#        'licenseVersion':'2', 
#        'MaintenanceExpiryDate':'2099-12-31',
#        'Organisation':organisation,
#        'SEN':'SEN-L0000000',
#        'LicenseExpiryDate': '2099-12-31',
#        'LicenseTypeName': license_type_name,
#        'PurchaseDate': purchase_date.strftime('%Y-%m-%d')

#	'Description':'Confluence (Server)\: Evaluation',
#	'CreationDate':'2016-06-04',
#	'conf.active':'true',
#	'conf.Starter':'false',
#	'ContactEMail':'gongxd@lejiayuan.cn',
#	'Evaluation':'true',
#	'conf.LicenseTypeName':'COMMERCIAL',
#	'licenseVersion':'2',
#	'MaintenanceExpiryDate':'2099-12-31',
#	'Organisation':'Evaluation license',
#	'ServerID':server_id,
#	'SEN':'SEN-L0000000',
#	'LicenseID':'LIDSEN-L7989958',
#	'conf.NumberOfUsers':'-1',
#	'LicenseExpiryDate':'2099-12-31',
#	'PurchaseDate':'2016-06-04',

#	'Description':'HTML for Confluence\: Evaluation',
#	'NumberOfUsers':'-1',
#	'CreationDate':'2016-06-04',
#	'ContactEMail':'gongxd@lejiayuan.cn',
#	'Evaluation':'true',
#	'licenseVersion':'2',
#	'MaintenanceExpiryDate':'2099-07-03',
#	'Organisation':'Evaluation license',
#	'org.swift.confluence.html.active':'true',
#	'SEN':'SEN-L7991799',
#	'LicenseExpiryDate':'2099-07-03',
#	'org.swift.confluence.html.Starter':'false',
#	'LicenseTypeName':'COMMERCIAL',
#	'org.swift.confluence.html.enterprise':'true',
#	'PurchaseDate':'2099-07-03',

#	'Description':'Balsamiq Mockups for Confluence Server\: Evaluation',
#	'NumberOfUsers':'-1',
#	'CreationDate':'2016-06-04',
#	'com.balsamiq.confluence.plugins.mockups.enterprise':'true',
#	'ContactEMail':'gongxd@lejiayuan.cn',
#	'Evaluation':'true',
#	'com.balsamiq.confluence.plugins.mockups.Starter':'false',
#	'licenseVersion':'2',
#	'MaintenanceExpiryDate':'2099-07-03',
#	'com.balsamiq.confluence.plugins.mockups.active':'true',
#	'Organisation':'Evaluation license',
#	'SEN':'SEN-L0000000',
#	'LicenseExpiryDate':'2099-07-03',
#	'LicenseTypeName':'COMMERCIAL',
#	'PurchaseDate':'2016-06-04',

#	'Description':'ProtoShare - Interactive Mockups\: Evaluation',
#	'NumberOfUsers':'-1',
#	'com.protoshare.confluence.plugins.protoshare-confluence.enterprise':'true',
#	'CreationDate':'2016-06-04',
#	'ContactEMail':'gongxd@lejiayuan.cn',
#	'Evaluation':'true',
#	'com.protoshare.confluence.plugins.protoshare-confluence.Starter':'false',
#	'licenseVersion':'2',
#	'MaintenanceExpiryDate':'2099-07-04',
#	'Organisation':'Evaluation license',
#	'SEN':'SEN-L0000000',
#	'LicenseExpiryDate':'2099-07-04',
#	'LicenseTypeName':'COMMERCIAL',
#	'com.protoshare.confluence.plugins.protoshare-confluence.active':'true',
#	'PurchaseDate':'2016-06-04',

#	'Description':'Sketchboard.Me for Confluence\: Evaluation',
#	'NumberOfUsers':'-1',
#	'CreationDate':'2016-06-04',
#	'net.sevenscales.confluence.plugins.sketcho-confluence.Starter':'false',
#	'ContactEMail':'gongxd@lejiayuan.cn',
#	'Evaluation':'true',
#	'licenseVersion':'2',
#	'MaintenanceExpiryDate':'2099-07-04',
#	'Organisation':'Evaluation license',
#	'SEN':'SEN-L0000000',
#	'LicenseExpiryDate':'2099-07-04',
#	'LicenseTypeName':'COMMERCIAL',
#	'net.sevenscales.confluence.plugins.sketcho-confluence.active':'true',
#	'net.sevenscales.confluence.plugins.sketcho-confluence.enterprise':'true',
#	'PurchaseDate':'2016-06-04',

#	'Description':'Yoikee Creator Templates by Mind Mapping\: Evaluation',
#	'NumberOfUsers':'-1',
#	'CreationDate':'2016-06-04',
#	'com.keinoby.confluence.plugins.yoikee-creator.active':'true',
#	'com.keinoby.confluence.plugins.yoikee-creator.Starter':'false',
#	'com.keinoby.confluence.plugins.yoikee-creator.enterprise':'true',
#	'ContactEMail':'gongxd@lejiayuan.cn',
#	'Evaluation':'true',
#	'licenseVersion':'2',
#	'MaintenanceExpiryDate':'2099-07-04',
#	'Organisation':'Evaluation license',
#	'SEN':'SEN-L0000000',
#	'LicenseExpiryDate':'2099-07-04',
#	'LicenseTypeName':'COMMERCIAL',
#	'PurchaseDate':'2016-06-04',

#	'Description':'EasyMind\: Evaluation',
#	'NumberOfUsers':'-1',
#	'CreationDate':'2016-06-04',
#	'cz.morosystems.atlassian.plugin.easymind.enterprise':'true',
#	'ContactEMail':'gongxd@lejiayuan.cn',
#	'Evaluation':'true',
#	'cz.morosystems.atlassian.plugin.easymind.Starter':'false',
#	'licenseVersion':'2',
#	'MaintenanceExpiryDate':'2099-07-04',
#	'Organisation':'Evaluation license',
#	'SEN':'SEN-L7992124',
#	'cz.morosystems.atlassian.plugin.easymind.active':'true',
#	'LicenseExpiryDate':'2099-07-04',
#	'LicenseTypeName':'COMMERCIAL',
#	'PurchaseDate':'2099-07-04',

#	'Description':'Docs - JavaDocs, PHPDocs, HTML-Pages...\: Evaluation',
#	'NumberOfUsers':'-1',
#	'CreationDate':'2016-06-04',
#	'ContactEMail':'gongxd@lejiayuan.cn',
#	'Evaluation':'true',
#	'net.meixxi.confluence.docs.docs-plugin.active':'true',
#	'licenseVersion':'2',
#	'MaintenanceExpiryDate':'2016-07-04',
#	'Organisation':'Evaluation license',
#	'SEN':'SEN-L7992224',
#	'LicenseExpiryDate':'2016-07-04',
#	'LicenseTypeName':'COMMERCIAL',
#	'net.meixxi.confluence.docs.docs-plugin.enterprise':'true',
#	'net.meixxi.confluence.docs.docs-plugin.Starter':'false',
#	'PurchaseDate':'2016-06-04',

#	"Description":"Gantt-Chart for JIRA\: Evaluation",
#	"NumberOfUsers":"-1",
#	"de.polscheit.jira.plugins.gantt.active":"true",
#	"CreationDate":"2016-07-14",
#	"ContactEMail":"gongxd@lejiayuan.cn",
#	"Evaluation":"true",
#	"de.polscheit.jira.plugins.gantt.enterprise":"true",
#	"licenseVersion":"2",
#	"MaintenanceExpiryDate":"2099-08-12",
#	"Organisation":"sskaje",
#	"SEN":"SEN-L0000000",
#	"LicenseExpiryDate":"2099-08-12",
#	"de.polscheit.jira.plugins.gantt.Starter":"false",
#	"LicenseTypeName":"COMMERCIAL",
#	"PurchaseDate":"2016-07-14",

#        "com.allenta.jira.plugins.gitlab.gitlab-listener.enterprise":"true",
#        "NumberOfUsers":"-1",
#        "Organisation":"sskaje",
#        "ContactEMail":"gongxd@lejiayuan.cn",
#        "licenseVersion":"2",
#        "Evaluation":"true",
#        "Description":"GitLab Listener\: Evaluation",
#        "com.allenta.jira.plugins.gitlab.gitlab-listener.Starter":"false",
#        "PurchaseDate":"2016-03-07",
#        "com.allenta.jira.plugins.gitlab.gitlab-listener.active":"true",
#        "LicenseTypeName":"COMMERCIAL",
#        "MaintenanceExpiryDate":"2099-04-05",
#        "SEN":"SEN-000000",
#        "CreationDate":"2016-03-07",
#        "LicenseExpiryDate":"2099-04-05",

#jira software 
#"NumberOfUsers":"-1", 
#"jira.NumberOfUsers":"-1", 
#"PurchaseDate":"2017-01-04", 
#"LicenseTypeName":"COMMERCIAL", 
#"LicenseExpiryDate":"2099-12-31", 
#"ContactEMail":"gongxd@lejiayuan.cn", 
#"ServerID":"BOLV-5F7S-6593-F6Z2", 
#"jira.product.jira-software.active":"true", 
#"jira.product.jira-software.DataCenter":"true", 
#"Subscription":"true", 
#"jira.LicenseEdition":"ENTERPRISE", 
#"greenhopper.LicenseTypeName":"COMMERCIAL", 
#"MaintenanceExpiryDate":"2099-12-31", 
#"jira.product.jira-software.NumberOfUsers":"-1", 
#"LicenseID":"LIDSEN-L0000000", 
#"jira.DataCenter":"true", 
#"SEN":"SEN-L0000000", 
#"jira.product.jira-software.Starter":"false", 
#"Organisation":"Evaluation license", 
#"CreationDate":"2017-01-04", 
#"licenseVersion":"2", 
#"greenhopper.enterprise":"true", 
#"Description":"JIRA Software (Data Center)\: Evaluation",
#"jira.active":"true", 
#"jira.LicenseTypeName":"COMMERCIAL", 
#"greenhopper.active":"true", 
#"Evaluation":"true"

#"NumberOfUsers":"-1", 
#"jira.product.jira-core.NumberOfUsers":"-1", 
#"jira.NumberOfUsers":"-1", 
#"PurchaseDate":"2017-01-06", 
#"LicenseTypeName":"COMMERCIAL", 
#"LicenseExpiryDate":"2099-12-31", 
#"ContactEMail":"gongxd@lejiayuan.cn", 
#"ServerID":"BOLV-5F7S-6593-F6Z2", 
#"jira.product.jira-core.Starter":"false", 
#"jira.LicenseEdition":"ENTERPRISE", 
#"jira.product.jira-core.active":"true", 
#"MaintenanceExpiryDate":"2099-12-31", 
#"LicenseID":"LIDSEN-L0000000", 
#"SEN":"SEN-L0000000", 
#"Organisation":"Evaluation license", 
#"CreationDate":"2017-01-06", 
#"licenseVersion":"2", 
#"Description":"JIRA Core (Server)\: Evaluation", 
#"jira.active":"true", 
#"jira.LicenseTypeName":"COMMERCIAL", 
#"Evaluation":"true", 
"jira.product.jira-servicedesk.active":"true",
"jira.product.jira-servicedesk.Starter":"false",
"NumberOfUsers":"-1",
"PurchaseDate":"2017-01-06",
"com.atlassian.servicedesk.active":"true",
"LicenseTypeName":"COMMERCIAL",
"LicenseExpiryDate":"2099-12-31",
"ContactEMail":"gongxd@lejiayuan.cn",
"ServerID":"BOLV-5F7S-6593-F6Z2",
"com.atlassian.servicedesk.LicenseTypeName":"COMMERCIAL",
"jira.product.jira-servicedesk.NumberOfUsers":"-1",
"MaintenanceExpiryDate":"2099-12-31",
"com.atlassian.servicedesk.enterprise":"true",
"LicenseID":"LIDSEN-L0000000",
"SEN":"SEN-L0000000",
"Organisation":"Evaluation license",
"CreationDate":"2017-01-06",
"com.atlassian.servicedesk.numRoleCount":"-1",
"licenseVersion":"2",
"Description":"JIRA Service Desk (Server)\: Evaluation",
"Evaluation":"true",


    }
    properties_text = '#%s\n%s' % (header, '\n'.join(['%s=%s' % (key, value) for key, value in properties.iteritems()]))
    compressed_properties_text = zlib.compress(properties_text, 9)
    license_text_prefix = map(chr, (13, 14, 12, 10, 15))
    license_text = ''.join(license_text_prefix + [compressed_properties_text])

    dsa = DSA.load_key(private_key)
    assert dsa.check_key()
    license_signature = dsa.sign_asn1(sha1(license_text).digest())
    license_pair_base64 = base64.b64encode('%s%s%s' % (unichr(len(license_text)).encode('UTF-32BE'), license_text, license_signature))
    license_str = '%sX02%s' % (license_pair_base64, base_n(len(license_pair_base64), 31))
    return license_str


def main():
    license_edition = 'ENTERPRISE'
    license_type_name = 'COMMERCIAL'
    organisation = 'sskaje'  # Change this to what you like
    server_id = 'BJNK-7Z93-8XNA-DJW2'  # Change this to your server ID
    print keymaker(organisation, server_id, license_edition, license_type_name)


def base_n(num, b, numerals="0123456789abcdefghijklmnopqrstuvwxyz"):
    return ((num == 0) and "0") or (base_n(num // b, b).lstrip("0") + numerals[num % b])

if __name__ == '__main__':
    main()
