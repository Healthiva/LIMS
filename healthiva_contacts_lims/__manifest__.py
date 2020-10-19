# -*- coding: utf-8 -*-
{
    'name': "H-Module",

    'summary': """
        EMR and Lab Controller System sends data to Odoo to be converted and stored then creates new file to be sent back to EMR""",

    'description': """
        Task ID: 2285516
        1.  Remove the radio button option of ‘Individual & Company from the form view in Contacts.
        2.  All fields to be added to the system should follow the HL7 standards described in the (HL7 Segment Details) document.
        3.  User should be able to Search, Filter and Group By all fields that will be added.
        4.  Add fields listed in the PID segment to the form view in Contacts
        5.  Add a new tab ‘MSH’ and add the all the fields mentioned in the MSH segment in the attached document (HL7 Segment Details).
        6.  Add state Info button (One2Many) as shown in the figure 1.0. All fields should be based on the relevant segments mentioned in the (HL7 Segment Details) document.
        7.  Remaining segments mentioned in the (HL7 Segment Details) document shall be added as a new model in the Contacts Module.

    """,

    'author': "Odoo Inc",
    'website': "http://www.odoo.com",
    'category': 'Custom Development',
    'version': '1.0',
    'depends': ['contacts', 'base_edi'],
    'data': [
        'security/security_groups.xml',
        'security/ir.model.access.csv',
        'views/blood_lead_views.xml',
        'views/res_config_settings.xml',
        'views/common_order_views.xml',
        'views/courtesy_views.xml',
        'views/diagnosis_views.xml',
        'views/general_info_views.xml',
        'views/diagnosis_views.xml',
        'views/general_info_views.xml',
        'views/guarantor_views.xml',
        'views/insurance_views.xml',
        'views/message_header_views.xml',
        'views/observation_views.xml',
        'views/provider_views.xml',
        'views/result_views.xml',
        'views/res_partner_views.xml',
        'data/edi_contact_data.xml',
    ]
}
