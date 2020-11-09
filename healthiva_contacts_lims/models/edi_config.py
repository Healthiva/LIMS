# -*- coding: utf-8 -*-

import os
import re
from odoo.tools.misc import profile
from os import listdir
from os.path import isfile, join
from odoo.exceptions import UserError 
from odoo import models, fields, api

class SyncDocumentType(models.Model):

    _inherit = 'sync.document.type'

    doc_code = fields.Selection(selection_add=[
                                ('import_contact_hl7', 'Import hl7 contact'),
                                ('export_contact_hl7', 'Export hl7 contact')
                                ])

    @profile('/home/zna/Documents/prof.profile')
    @api.model
    def _do_export_contact_hl7(self, conn, sync_action_id, values):
        '''
        @param conn : sftp/ftp connection class.
        @param sync_action_id: recorset of type `edi.sync.action`
        @param values:dict of values that may be useful to various methods
        @return bool : return bool (True|False)
        '''
        conn._connect()
        conn.cd(sync_action_id.dir_path)
        results = []
        results.append(self.parse_msh(self))
        results.append(self.parse_patient(self))
        for provider in self.provider_ids:
            results.append(self.parse_provider(provider))
        for insurance in self.insurance_ids:
            results.append(self.parse_insurance(insurance))
        for guarantor in self.guarantor_ids:
            results.append(self.parse_guarantor(guarantor))
        for diagnosis in self.diagnosis_ids:
            results.append(self.parse_diagnosis(diagnosis))
        for general_info in self.general_info_ids:
            results.append(self.parse_general_info(general_info))
        for common_order in self.common_order_ids:
            results.append(self.parse_common_order(common_order))
        for observation in self.observation_ids:
            results.append(self.parse_observation(observation))
        for result in self.result_ids:
            results.append(self.parse_result(result))
        final = { "document": "", "missing": "", "is_missing": False }
        for dic in results:
            final = { "document": final["document"] + dic["document"], "missing": final["missing"] + dic["missing"] }
            if dic["is_missing"]:
                final["is_missing"] = True
        if final["is_missing"]:
            raise UserError(final["missing"])
        final["document"]
        filename = 'result.hl7'
        with open(filename, 'wt') as f:
            f.write(final["document"])
            conn.upload_file(filename, f)
            f.close()
        conn._disconnect()
        return True

    @api.model
    def _do_import_contact_hl7(self, conn, sync_action_id, values):
        '''
        @param conn : sftp/ftp connection class.
        @param sync_action_id: recorset of type `edi.sync.action`
        @param values:dict of values that may be useful to various methods
        @return bool : return bool (True|False)
        '''
        conn._connect()
        conn.cd(sync_action_id.dir_path)
        files = conn.ls()
        if files:
            for edifile in files:
                patient = None
                message = None
                observation = None
                with open(edifile, 'rt') as f:
                    lines = f.read().splitlines()
                    for line in lines:
                        fields = self.get_string_fields(line)
                        if fields[0] == "MSH":
                            message = self.create_msh(fields)
                        elif fields[0] == "PID":
                            patient = self.identify_patient(fields, message)
                        elif fields[0] == "PV1":
                            self.create_provider(fields, patient)
                        elif fields[0] == "IN1":
                            self.create_insurance(fields, patient)
                        elif fields[0] == "GT1":
                            self.create_guarantor(fields, patient)
                        elif fields[0] == "DG1":
                            self.create_diagnosis(fields, patient)
                        elif fields[0] == "ZCI":
                            self.create_general_info(fields, patient)
                        elif fields[0] == "ORC":
                            self.create_common_order(fields, patient)
                        elif fields[0] == "OBR":
                            observation = self.identify_patient(fields, patient)
                        elif fields[0] == "OBX":
                            self.create_result(fields, observation)
                    f.close()
        conn._disconnect()
        return True
        
    def get_string_fields(self, str):
        fields = re.split(r"(?<!\\)\|", str)
        for i,field in enumerate(fields):
            fields[i] = re.split(r"(?<!\\)\^", field)
            if len(fields[i]) == 1:
                fields[i] = fields[i][0]
        return fields

    def fill_fields(self, fields, idx, subidx=-1):
        val = ""
        try:
            if subidx >= 0:
                if subidx == 0 and not isinstance(fields[idx], list):
                    val = fields[idx]
                elif not isinstance(fields[idx], list):
                    val = ""
                else:
                    val = fields[idx][subidx]
            else:
                val = fields[idx]
        except:
            val = ""
        return val

    def strtofloat(self, str):
        try:
            return float(str)
        except:
            pass
        return

    def strtoint(self, str):
        try:
            return int(str)
        except:
            pass
        return

    def get_id(self, instance):
        try:
            return instance.id
        except:
            pass
        return

    def identify_patient(self, fields, message):
        vals = {
            "sequence_number": self.strtoint(self.fill_fields(fields, 1)),
            "external_pid": self.fill_fields(fields, 2),
            "assigned_pid": self.fill_fields(fields, 3),
            "alternate_pid": self.fill_fields(fields, 4),
            "name": self.fill_fields(fields, 5, 1) + " " + self.fill_fields(fields, 5, 0),
            "last_name": self.fill_fields(fields, 5, 0),
            "first_name": self.fill_fields(fields, 5, 1),
            "middle_name": self.fill_fields(fields, 5, 2),
            "mother_maiden": self.fill_fields(fields, 6),
            "birth_date": self.fill_fields(fields, 7, 0),
            "age_years": self.strtoint(self.fill_fields(fields, 7, 1)),
            "age_months": self.strtoint(self.fill_fields(fields, 7, 2)),
            "age_days": self.strtoint(self.fill_fields(fields, 7, 3)),
            "gender": self.fill_fields(fields, 8),
            "alias": self.fill_fields(fields, 9),
            "race": self.fill_fields(fields, 10),
            "patient_address1": self.fill_fields(fields, 11, 0),
            "patient_address2": self.fill_fields(fields, 11, 1),
            "patient_address_city": self.fill_fields(fields, 11, 2),
            "patient_address_state": self.fill_fields(fields, 11, 3),
            "patient_address_zip": self.fill_fields(fields, 11, 4),
            "country_code": self.fill_fields(fields, 12),
            "phone": self.fill_fields(fields, 13, 0),
            "tele_use_code": self.fill_fields(fields, 13, 1),
            "tele_equip_type": self.fill_fields(fields, 13, 2),
            "tele_address": self.fill_fields(fields, 13, 3),
            "work_phone": self.fill_fields(fields, 14),
            "language": self.fill_fields(fields, 15),
            "marital_status": self.fill_fields(fields, 16),
            "religion": self.fill_fields(fields, 17),
            "account_number": self.fill_fields(fields, 18, 0),
            "check_digit": self.fill_fields(fields, 18, 1),
            "check_digit_scheme": self.fill_fields(fields, 18, 2),
            "bill_type": self.fill_fields(fields, 18, 3),
            "abn_flag": self.fill_fields(fields, 18, 4),
            "specimen_status": self.fill_fields(fields, 18, 5),
            "is_fasting": self.fill_fields(fields, 18, 6),
            "ssn": self.fill_fields(fields, 19),
            "driver_license": self.fill_fields(fields, 20),
            "mother_identifier": self.fill_fields(fields, 21),
            "ethnic_group": self.fill_fields(fields, 22),
            "message_header_id": message.id
        }
        patient = self.env['res.partner']
        record = patient.search([('external_pid', '=', vals['external_pid'])])
        if record:
            record = patient.write(1, record.id, vals)
        else:
            record = patient.write(0, 0, vals)
        return record

    def identify_observation(self, fields, patient):
        vals = {
            "sequence_number": self.strtoint(self.fill_fields(fields, 1)),
            "foreign_accessionid": self.fill_fields(fields, 2, 0),
            "foreign_appid": self.fill_fields(fields, 2, 1),
            "internal_accessionid": self.fill_fields(fields, 3, 0),
            "internal_appid": self.fill_fields(fields, 3, 1),
            "battery_identifier": self.fill_fields(fields, 4, 0),
            "battery_text": self.fill_fields(fields, 4, 1),
            "coding_system1": self.fill_fields(fields, 4, 2),
            "priority": self.fill_fields(fields, 5),
            # "": fields[6],
            "specimen_collect_date": self.fill_fields(fields, 7),
            "specimen_collect_end_time": self.fill_fields(fields, 8),
            "collection_volume": self.strtoint(self.fill_fields(fields, 9, 0)),
            "collection_uom": self.fill_fields(fields, 9, 1),
            "collector_identifier": self.fill_fields(fields, 10),
            "action_code": self.fill_fields(fields, 11),
            "danger_code": self.fill_fields(fields, 12),
            "clinic_info": self.fill_fields(fields, 13, 0),
            "clinic_info_back": self.fill_fields(fields, 13, 1),
            "specimen_receipt_date": self.fill_fields(fields, 14),
            "specimen_source": self.fill_fields(fields, 15),
            "providerid": self.strtoint(self.fill_fields(fields, 16, 0)),
            "provider_last": self.fill_fields(fields, 16, 1),
            "provider_first": self.fill_fields(fields, 16, 2),
            "provider_middle": self.fill_fields(fields, 16, 3),
            "provider_suffix": self.fill_fields(fields, 16, 4),
            "provider_prefix": self.fill_fields(fields, 16, 5),
            "provider_degree": self.fill_fields(fields, 16, 6),
            "source_table": self.fill_fields(fields, 16, 7),
            "phone": self.fill_fields(fields, 17),
            "alternate_foreign_accessionid": self.fill_fields(fields, 18),
            "requester_field2": self.fill_fields(fields, 19),
            "producer_field1": self.fill_fields(fields, 20, 0),
            "microbiology_organism": self.fill_fields(fields, 20, 1),
            "coding_system2": self.fill_fields(fields, 20, 2),
            "producer_field2": self.fill_fields(fields, 21),
            "report_date": self.fill_fields(fields, 22),
            "producer_charge": self.fill_fields(fields, 23),
            "producer_sectionid": self.fill_fields(fields, 24),
            "order_result_status": self.fill_fields(fields, 25),
            "organism_link": self.fill_fields(fields, 26, 0),
            "subid": self.fill_fields(fields, 26, 1),
            "quantity_timing": self.strtoint(self.fill_fields(fields, 27)),
            "courtesy_copies": self.strtoint(self.fill_fields(fields, 28)),
            "parent_order_link": self.fill_fields(fields, 29),
            "patient_id": self.get_id(patient)
        }
        observation = self.env['healthiva.observation']
        record = observation.search([('foreign_accessionid', '=', vals['foreign_accessionid'])])
        if record:
            record = observation.write(1, record.id, vals)
        else:
            record = observation.write(0, 0, vals)
        return record

    def create_msh(self, fields):
        # Creates record using fill_fields helper method
        return self.env['healthiva.message_header'].create([{
            "field_delimiter": "|",
            "component_delimiter": self.fill_fields(fields, 1),
            "sending_application": self.fill_fields(fields, 2),
            "sending_facility": self.fill_fields(fields, 3),
            "receiving_application": self.fill_fields(fields, 4),
            "receiving_facility": self.fill_fields(fields, 5),
            "receive_date": self.fill_fields(fields, 6),
            "security": self.fill_fields(fields, 7),
            "message_type": self.fill_fields(fields, 8),
            "message_controlid": self.fill_fields(fields, 9),
            "processingid": self.fill_fields(fields, 10),
            "hl7_version": self.fill_fields(fields, 11)
        }])

    def create_patient(self, fields, message):
        return self.env['res.partner'].create([])

    def create_provider(self, fields, patient):
        self.env['healthiva.provider'].create([{
            "sequence_number": self.strtoint(self.fill_fields(fields, 1)),
            "patient_class": self.fill_fields(fields, 2),
            "assigned_location": self.fill_fields(fields, 3),
            "admission_type": self.fill_fields(fields, 4),
            "preadmit_number": self.fill_fields(fields, 5),
            "prior_location": self.fill_fields(fields, 6),
            "attending_doctor_npi": self.fill_fields(fields, 7, 0),
            "attending_doctor_first": self.fill_fields(fields, 7, 1),
            "attending_doctor_last": self.fill_fields(fields, 7, 2),
            "referring_doctor": self.fill_fields(fields, 8),
            "consulting_doctor": self.fill_fields(fields, 9),
            "hospital_service": self.fill_fields(fields, 10),
            "temp_location": self.fill_fields(fields, 11),
            "pretest_indicator": self.fill_fields(fields, 12),
            "readmission": self.fill_fields(fields, 13),
            "admit_source": self.fill_fields(fields, 14),
            "ambulatory_status": self.fill_fields(fields, 15),
            "vip_indicator": self.fill_fields(fields, 16),
            "admitting_doctor": self.fill_fields(fields, 17),
            "patient_type": self.fill_fields(fields, 18),
            "visit_number": self.fill_fields(fields, 19),
            "financial_class": self.fill_fields(fields, 20),
            "charge_indicator": self.fill_fields(fields, 21),
            "courtesy_code": self.fill_fields(fields, 22),
            "credit_rating": self.fill_fields(fields, 23),
            "contract_code": self.fill_fields(fields, 24),
            "contract_date": self.fill_fields(fields, 25),
            "contract_total": self.fill_fields(fields, 26),
            "contract_period": self.fill_fields(fields, 27),
            "interest_code": self.fill_fields(fields, 28),
            "tbd_code": self.fill_fields(fields, 29),
            "tbd_date": self.fill_fields(fields, 30),
            "bda_code": self.fill_fields(fields, 31),
            "bd_transfer_total": self.fill_fields(fields, 32),
            "bd_recovery_total": self.fill_fields(fields, 33),
            "delete_indicator": self.fill_fields(fields, 34),
            "delete_date": self.fill_fields(fields, 35),
            "discharge_disposition": self.fill_fields(fields, 36),
            "discharge_location": self.fill_fields(fields, 37),
            "diet_type": self.fill_fields(fields, 38),
            "service_location": self.fill_fields(fields, 39),
            "bed_status": self.fill_fields(fields, 40),
            "account_status": self.fill_fields(fields, 41),
            "pending_loc": self.fill_fields(fields, 42),
            "prior_temp_location": self.fill_fields(fields, 43),
            "admit_date": self.fill_fields(fields, 44),
            "discharge_date": self.fill_fields(fields, 45),
            "current_balance": self.fill_fields(fields, 46),
            "charges_total": self.fill_fields(fields, 47),
            "adjustments_total": self.fill_fields(fields, 48),
            "payments_total": self.fill_fields(fields, 49),
            "alt_visitid": self.fill_fields(fields, 50),
            "visit_indicator": self.fill_fields(fields, 51),
            "other_provider": self.fill_fields(fields, 52),
            "patient_id": self.get_id(patient)
        }])

    def create_insurance(self, fields, patient):
        self.env['healthiva.insurance'].create([{
            "sequence_number": self.strtoint(self.fill_fields(fields, 1)),
            "plan_id": self.fill_fields(fields, 2),
            "id_number": self.fill_fields(fields, 3, 0),
            "payer_code": self.fill_fields(fields, 3, 1),
            "company_name": self.fill_fields(fields, 4),
            "company_address1": self.fill_fields(fields, 5, 0),
            "company_address2": self.fill_fields(fields, 5, 1),
            "company_address_city": self.fill_fields(fields, 5, 2),
            "company_address_state": self.fill_fields(fields, 5, 3),
            "company_address_zip": self.fill_fields(fields, 5, 4),
            "contact_name": self.fill_fields(fields, 6),
            "phone": self.fill_fields(fields, 7),
            "group_number": self.fill_fields(fields, 8),
            "group_name": self.fill_fields(fields, 9),
            "employerid": self.fill_fields(fields, 10),
            "employer_name": self.fill_fields(fields, 11),
            "plan_effective_date": self.fill_fields(fields, 12),
            "plan_expiration_date": self.fill_fields(fields, 13),
            "authorization_info": self.fill_fields(fields, 14),
            "plan_type": self.fill_fields(fields, 15),
            "insured_last_name": self.fill_fields(fields, 16, 0),
            "insured_first_name": self.fill_fields(fields, 16, 1),
            "insured_middle_name": self.fill_fields(fields, 16, 2),
            "insured_relation": self.fill_fields(fields, 17),
            "insured_dob": self.fill_fields(fields, 18),
            "insured_address1": self.fill_fields(fields, 19, 0),
            "insured_address2": self.fill_fields(fields, 19, 1),
            "insured_address_city": self.fill_fields(fields, 19, 2),
            "insured_address_state": self.fill_fields(fields, 19, 3),
            "insured_address_zip": self.fill_fields(fields, 19, 4),
            "assignment_benefits": self.fill_fields(fields, 20),
            "coordinator_benefits": self.fill_fields(fields, 21),
            "primary_payer": self.fill_fields(fields, 22),
            "notice_admit_code": self.fill_fields(fields, 23),
            "notice_admit_date": self.fill_fields(fields, 24),
            "report_eligibility_flag": self.fill_fields(fields, 25),
            "report_eligibility_date": self.fill_fields(fields, 26),
            "release_info_code": self.fill_fields(fields, 27),
            "preadmit_certification": self.fill_fields(fields, 28),
            "verification_date": self.fill_fields(fields, 29),
            "verification_by": self.fill_fields(fields, 30),
            "agreement_type": self.fill_fields(fields, 31),
            "bill_status": self.fill_fields(fields, 32),
            "reserve_days": self.fill_fields(fields, 33),
            "reserve_days_delay": self.fill_fields(fields, 34),
            "company_plan_code": self.fill_fields(fields, 35),
            "policy_number": self.fill_fields(fields, 36),
            "patient_id": self.get_id(patient)
        }])

    def create_guarantor(self, fields, patient):
        self.env['healthiva.guarantor'].create([{
            "sequence_number": self.strtoint(self.fill_fields(fields, 1)),
            "guarantor_number": self.fill_fields(fields, 2),
            "last_name": self.fill_fields(fields, 3, 0),
            "first_name": self.fill_fields(fields, 3, 1),
            "middle_name": self.fill_fields(fields, 3, 2),
            "spouse_name": self.fill_fields(fields, 4),
            "guarantor_address1": self.fill_fields(fields, 5, 0),
            "guarantor_address2": self.fill_fields(fields, 5, 1),
            "guarantor_address_city": self.fill_fields(fields, 5, 2),
            "guarantor_address_state": self.fill_fields(fields, 5, 3),
            "guarantor_address_zip": self.fill_fields(fields, 5, 4),
            "phone": self.fill_fields(fields, 6),
            "work_phone": self.fill_fields(fields, 7),
            "dob": self.fill_fields(fields, 8),
            "gender": self.fill_fields(fields, 9),
            "guarantor_type": self.fill_fields(fields, 10),
            "patient_relation": self.fill_fields(fields, 11),
            "ssn": self.fill_fields(fields, 12),
            "begin_date": self.fill_fields(fields, 13),
            "end_date": self.fill_fields(fields, 14),
            "priority": self.fill_fields(fields, 15),
            "employer_name": self.fill_fields(fields, 16),
            "patient_id": self.get_id(patient)
        }])

    def create_general_info(self, fields, patient):
        self.env['healthiva.general_info'].create([{
            "height": self.strtoint(self.fill_fields(fields, 1)),
            "weight_lb": self.strtoint(self.fill_fields(fields, 2, 0)),
            "weight_oz": self.strtoint(self.fill_fields(fields, 2, 1)),
            "weight_uom": self.fill_fields(fields, 2, 2),
            "collection_volume": self.strtoint(self.fill_fields(fields, 3, 0)),
            "collection_uom": self.fill_fields(fields, 3, 1),
            "fasting": self.fill_fields(fields, 4),
            "waist": self.strtoint(self.fill_fields(fields, 5)),
            "bp_systolic": self.strtoint(self.fill_fields(fields, 6, 0)),
            "bp_diastolic": self.strtoint(self.fill_fields(fields, 6, 1)),
            "pulse": self.strtoint(self.fill_fields(fields, 7)),
            "email": self.fill_fields(fields, 8),
            "patient_id": self.get_id(patient)
        }])

    def create_diagnosis(self, fields, patient):
        self.env['healthiva.diagnosis'].create([{
            "sequence_number": self.strtoint(self.fill_fields(fields, 1)),
            "code_method": self.fill_fields(fields, 2),
            "code_identifier": self.fill_fields(fields, 3, 0),
            "code_text": self.fill_fields(fields, 3, 1),
            "code_system": self.fill_fields(fields, 3, 2),
            "patient_id": self.get_id(patient)
        }])

    def create_common_order(self, fields, patient):
        self.env['healthiva.common_order'].create([{
            "order_control": self.fill_fields(fields, 1),
            "foreign_accessionid": self.fill_fields(fields, 2, 0),
            "applicationid": self.fill_fields(fields, 2, 1),
            "filler_accessionid": self.fill_fields(fields, 3, 0),
            "accession_owner": self.fill_fields(fields, 3, 1),
            "placer_number": self.fill_fields(fields, 4),
            "order_status": self.fill_fields(fields, 5),
            "response_flag": self.fill_fields(fields, 6),
            "quantity_timing": self.fill_fields(fields, 7),
            "parent": self.fill_fields(fields, 8),
            "transaction_date": self.fill_fields(fields, 9),
            "entered1": self.fill_fields(fields, 10),
            "entered2": self.fill_fields(fields, 11),
            "providerid": self.fill_fields(fields, 12, 0),
            "provider_last": self.fill_fields(fields, 12, 1),
            "provider_first": self.fill_fields(fields, 12, 2),
            "provider_middle": self.fill_fields(fields, 12, 3),
            "provider_suffix": self.fill_fields(fields, 12, 4),
            "provider_prefix": self.fill_fields(fields, 12, 5),
            "provider_degree": self.fill_fields(fields, 12, 6),
            "source_table": self.fill_fields(fields, 12, 7),
            "enterer_location": self.fill_fields(fields, 13),
            "phone": self.fill_fields(fields, 14),
            "patient_id": self.get_id(patient)
        }])

    def create_observation(self, fields, patient):
        self.env['healthiva.observation'].create([])

    def create_result(self, fields, patient):
        self.env['healthiva.result'].create([{
            "sequence_number": self.strtoint(self.fill_fields(fields, 1)),
            "value_type": self.fill_fields(fields, 2),
            "observation_identifier": self.fill_fields(fields, 3, 0),
            "observation_text": self.fill_fields(fields, 3, 1),
            "coding_system_name1": self.fill_fields(fields, 3, 2),
            "alternate_identifier": self.fill_fields(fields, 3, 3),
            "alternate_observation_text": self.fill_fields(fields, 3, 4),
            "alternate_observation_system": self.fill_fields(fields, 3, 5),
            "observation_subid": self.fill_fields(fields, 4),
            "observation_value": self.fill_fields(fields, 5, 0),
            "data_type": self.fill_fields(fields, 5, 1),
            "data_subtype": self.fill_fields(fields, 5, 2),
            "encoding": self.fill_fields(fields, 5, 3),
            "data_text": self.fill_fields(fields, 5, 4),
            "coding_system": self.fill_fields(fields, 5, 5),
            "identifier": self.fill_fields(fields, 6, 0),
            "result_text": self.fill_fields(fields, 6, 1),
            "coding_system_name2": self.fill_fields(fields, 6, 2),
            "ref_ranges": self.fill_fields(fields, 7),
            "abnormal_flags": self.fill_fields(fields, 8),
            "probability": self.fill_fields(fields, 9),
            "abnormal_test_nature": self.fill_fields(fields, 10),
            "result_status": self.fill_fields(fields, 11),
            "ref_range_update_date": self.fill_fields(fields, 12),
            "access_checks": self.fill_fields(fields, 13),
            "observation_date": self.fill_fields(fields, 14),
            "producerid": self.fill_fields(fields, 15),
            "observer": self.fill_fields(fields, 16),
            "observation_method": self.fill_fields(fields, 17),
            "equipment_identifier": self.fill_fields(fields, 18),
            "analysis_date": self.fill_fields(fields, 19),
            "reserver_hamorizing1": self.fill_fields(fields, 20),
            "reserver_hamorizing2": self.fill_fields(fields, 21),
            "reserver_hamorizing3": self.fill_fields(fields, 22),
            "performing_names": self.fill_fields(fields, 23),
            "performing_address": self.fill_fields(fields, 24),
            "performing_director": self.fill_fields(fields, 25),
            "release_category": self.fill_fields(fields, 26),
            "route_cause": self.fill_fields(fields, 27),
            "local_process_control": self.fill_fields(fields, 28),
            "patient_id": self.get_id(patient),
        }])
        
    def parse_msh(self, msh):
        instance = self.env["healthiva.message_header"]
        dic = msh.read()[0]
        fields = [
            "component_delimiter",
            "sending_application",
            "sending_facility",
            "receiving_application",
            "receiving_facility",
            "receive_date",
            "security",
            "message_type",
            "message_controlid",
            "processingid",
            "hl7_version",
        ]
        required = [1,2,3,4,5,6,8,9,10,11]
        line = "MSH|"
        return self.create_line(instance, dic, fields, [], required, line)
        
    def parse_patient(self, partner):
        instance = self.env["res.partner"]
        # Get a dictionary of the record passed in 
        dic = partner.read()[0]
        # Order matters in list since it represents the order of the incoming data
        fields = [
            "sequence_number",
            "external_pid",
            "assigned_pid",
            "alternate_pid",
            "last_name",
            "first_name",
            "middle_name",
            "mother_maiden",
            "birth_date",
            "age_years",
            "age_months",
            "age_days",
            "gender",
            "alias",
            "race",
            "patient_address1",
            "patient_address2",
            "patient_address_city",
            "patient_address_state",
            "patient_address_zip",
            "country_code",
            "phone",
            "tele_use_code",
            "tele_equip_type",
            "tele_address",
            "work_phone",
            "language",
            "marital_status",
            "religion",
            "account_number",
            "check_digit",
            "check_digit_scheme",
            "bill_type",
            "abn_flag",
            "specimen_status",
            "is_fasting",
            "ssn",
            "driver_license",
            "mother_identifier",
            "ethnic_group",
        ]
        # Indices that require a ^ delimiter instead of |
        subfield_delimiter_indices = [5,6,9,10,11,16,17,18,19,22,23,24,30,31,32,33,34,35]
        # Indices of required fields that need to be in sent message or else error warning will trigger
        required = [1,2,5,6,9,13,16,18,30,33]
        # Segment Identifier appended to beginning of row
        line = "PID|"
        # Fill in segment fields and create string of the line to be sent
        return self.create_line(instance, dic, fields, subfield_delimiter_indices, required, line)
    
    def parse_provider(self, provider):
        instance = self.env["healthiva.provider"]
        dic = provider.read()[0]
        fields = [
            "sequence_number",
            "patient_class",
            "assigned_location",
            "admission_type",
            "preadmit_number",
            "prior_location",
            "attending_doctor_npi",
            "attending_doctor_first",
            "attending_doctor_last",
            "referring_doctor",
            "consulting_doctor",
            "hospital_service",
            "temp_location",
            "pretest_indicator",
            "readmission",
            "admit_source",
            "ambulatory_status",
            "vip_indicator",
            "admitting_doctor",
            "patient_type",
            "visit_number",
            "financial_class",
            "charge_indicator",
            "courtesy_code",
            "credit_rating",
            "contract_code",
            "contract_date",
            "contract_total",
            "contract_period",
            "interest_code",
            "tbd_code",
            "tbd_date",
            "bda_code",
            "bd_transfer_total",
            "bd_recovery_total",
            "delete_indicator",
            "delete_date",
            "discharge_disposition",
            "discharge_location",
            "diet_type",
            "service_location",
            "bed_status",
            "account_status",
            "pending_loc",
            "prior_temp_location",
            "admit_date",
            "discharge_date",
            "current_balance",
            "charges_total",
            "adjustments_total",
            "payments_total",
            "alt_visitid",
            "visit_indicator",
            "other_provider",
        ]
        subfield_delimiter_indices = [7,8]
        required = [1,2]
        line = "PV1|"
        return self.create_line(instance, dic, fields, subfield_delimiter_indices, required, line)
    
    def parse_insurance(self, insurance):
        instance = self.env["healthiva.insurance"]
        dic = insurance.read()[0]
        fields = [
            "sequence_number",
            "plan_id",
            "id_number",
            "payer_code",
            "company_name",
            "company_address1",
            "company_address2",
            "company_address_city",
            "company_address_state",
            "company_address_zip",
            "contact_name",
            "phone",
            "group_number",
            "group_name",
            "employerid",
            "employer_name",
            "plan_effective_date",
            "plan_expiration_date",
            "authorization_info",
            "plan_type",
            "insured_last_name",
            "insured_first_name",
            "insured_middle_name",
            "insured_relation",
            "insured_dob",
            "insured_address1",
            "insured_address2",
            "insured_address_city",
            "insured_address_state",
            "insured_address_zip",
            "assignment_benefits",
            "coordinator_benefits",
            "primary_payer",
            "notice_admit_code",
            "notice_admit_date",
            "report_eligibility_flag",
            "report_eligibility_date",
            "release_info_code",
            "preadmit_certification",
            "verification_date",
            "verification_by",
            "agreement_type",
            "bill_status",
            "reserve_days",
            "reserve_days_delay",
            "company_plan_code",
            "policy_number",
        ]
        subfield_delimiter_indices = [3,6,7,8,9,21,22,26,27,28,29]
        required = [1,6,7,8,10,24,42,47]
        line = "IN1|"
        return self.create_line(instance, dic, fields, subfield_delimiter_indices, required, line)
    
    def parse_guarantor(self, guarantor):
        instance = self.env["healthiva.guarantor"]
        dic = guarantor.read()[0]
        fields = [
            "sequence_number",
            "guarantor_number",
            "last_name",
            "first_name",
            "middle_name",
            "spouse_name",
            "guarantor_address1",
            "guarantor_address2",
            "guarantor_address_city",
            "guarantor_address_state",
            "guarantor_address_zip",
            "phone",
            "work_phone",
            "dob",
            "gender",
            "guarantor_type",
            "patient_relation",
            "ssn",
            "begin_date",
            "end_date",
            "priority",
            "employer_name",
        ]
        subfield_delimiter_indices = [3,4,7,8,9,10]
        required = [1,3,4,6,8,9,10,11,17]
        line = "GT1|"
        return self.create_line(instance, dic, fields, subfield_delimiter_indices, required, line)
    
    def parse_general_info(self, general_info):
        instance = self.env["healthiva.general_info"]
        dic = general_info.read()[0]
        fields = [
            "height",
            "weight_lb",
            "weight_oz",
            "weight_uom",
            "collection_volume",
            "collection_uom",
            "fasting",
            "waist",
            "bp_systolic",
            "bp_diastolic",
            "pulse",
            "email",
        ]
        subfield_delimiter_indices = [2,3,5,9]
        required = []
        line = "ZCI|"
        return self.create_line(instance, dic, fields, subfield_delimiter_indices, required, line)
    
    def parse_diagnosis(self, diagnosis):
        instance = self.env["healthiva.diagnosis"]
        dic = diagnosis.read()[0]
        fields = [
            "sequence_number",
            "code_method",
            "code_identifier",
            "code_text",
            "code_system",
        ]
        subfield_delimiter_indices = [3,4]
        required = [1,3,5]
        line = "DG1|"
        return self.create_line(instance, dic, fields, subfield_delimiter_indices, required, line)
    
    def parse_common_order(self, common_order):
        instance = self.env["healthiva.common_order"]
        dic = common_order.read()[0]
        fields = [
            "order_control",
            "foreign_accessionid",
            "applicationid",
            "filler_accessionid",
            "accession_owner",
            "placer_number",
            "order_status",
            "response_flag",
            "quantity_timing",
            "parent",
            "transaction_date",
            "entered1",
            "entered2",
            "providerid",
            "provider_last",
            "provider_first",
            "provider_middle",
            "provider_suffix",
            "provider_prefix",
            "provider_degree",
            "source_table",
            "enterer_location",
            "phone",
        ]
        subfield_delimiter_indices = [2,4,14,15,16,17,18,19,20]
        required = [1,2]
        line = "ORC|"
        return self.create_line(instance, dic, fields, subfield_delimiter_indices, required, line)
    
    def parse_observation(self, observation):
        instance = self.env["healthiva.observation"]
        dic = observation.read()[0]
        fields = [
            "sequence_number",
            "foreign_accessionid",
            "foreign_appid",
            "internal_accessionid",
            "internal_appid",
            "battery_identifier",
            "battery_text",
            "coding_system1",
            "priority",
            "specimen_collect_date",
            "specimen_collect_end_time",
            "collection_volume",
            "collection_uom",
            "collector_identifier",
            "action_code",
            "danger_code",
            "clinic_info",
            "clinic_info_back",
            "specimen_receipt_date",
            "specimen_source",
            "providerid",
            "provider_last",
            "provider_first",
            "provider_middle",
            "provider_suffix",
            "provider_prefix",
            "provider_degree",
            "source_table",
            "phone",
            "alternate_foreign_accessionid",
            "requester_field2",
            "producer_field1",
            "microbiology_organism",
            "coding_system2",
            "producer_field2",
            "report_date",
            "producer_charge",
            "producer_sectionid",
            "order_result_status",
            "organism_link",
            "subid",
            "quantity_timing",
            "courtesy_copies",
            "parent_order_link",
        ]
        subfield_delimiter_indices = [2,4,6,7,12,17,20,21,22,23,24,25,26,31,32,39]
        required = [1,2,6,7,8,16]
        line = "OBR|"
        return self.create_line(instance, dic, fields, subfield_delimiter_indices, required, line)
    
    def parse_result(self, result):
        instance = self.env["healthiva.result"]
        dic = result.read()[0]
        fields = [
            "sequence_number",
            "value_type",
            "observation_identifier",
            "observation_text",
            "coding_system_name1",
            "alternate_identifier",
            "alternate_observation_text",
            "alternate_observation_system",
            "observation_subid",
            "observation_value",
            "data_type",
            "data_subtype",
            "encoding",
            "data_text",
            "coding_system",
            "identifier",
            "result_text",
            "coding_system_name2",
            "ref_ranges",
            "abnormal_flags",
            "probability",
            "abnormal_test_nature",
            "result_status",
            "ref_range_update_date",
            "access_checks",
            "observation_date",
            "producerid",
            "observer",
            "observation_method",
            "equipment_identifier",
            "analysis_date",
            "reserver_hamorizing1",
            "reserver_hamorizing2",
            "reserver_hamorizing3",
            "performing_names",
            "performing_address",
            "performing_director",
            "release_category",
            "route_cause",
            "local_process_control",
        ]
        subfield_delimiter_indices = [3,4,5,6,7,10,11,12,13,14,16,17]
        required = [1,3,4,5,22,23]
        line = "OBX|"
        return self.create_line(instance, dic, fields, subfield_delimiter_indices, required, line)

    def create_line(self, instance, dic, fields, subfield_delimiter_indices, required, line):
        missing = line[0:3] + " missing: "
        is_missing = False
        for i, field in enumerate(fields, start=1):
            if dic[field]:
                line += "{}".format(dic[field])
            elif not dic[field] and i in required:
                missing += instance._fields[field].string + ", "
                is_missing = True
            if i < len(fields):
                if i in subfield_delimiter_indices:
                    line += "^"
                else:
                    line += "|"
            else:
                line += "\n"
                missing += "\n\n"
        return { "document": line, "missing": missing, "is_missing": is_missing}