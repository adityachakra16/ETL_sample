from extract import Extract
from transform import Transformation
from stage import Stage

if __name__ == "__main__":
    tasks = {
             {
              {"Setup":
                {"table_name" : "Therapy",
                 "columns": ["uniqueid SERIAL NOT NULL", "primaryid NUMERIC(1000) NOT NULL", "caseid NUMERIC(500) NOT NULL",/
                                "dsg_drug_seq NUMERIC(10)", "start_dt NUMERIC(8)", "end_dt NUMERIC(8)",/
                                "dur NUMERIC(150)", "dur_cod NUMERIC"],
                 "primary_key": ["uniqueid"],
                 "foreign_key": ["primaryid REFERENCES Drug(primaryid)", "dsg_drug_seq REFERENCES Drug(drug_seq)"],
                },
                {"table_name" : "Indication",
                 "columns": ["uniqueid SERIAL NOT NULL","primaryid NUMERIC(1000) NOT NULL", "caseid NUMERIC(500) NOT NULL",/
                                "indi_drug_seq NUMERIC(10)", "indi_pt VARCHAR(1000)"],
                 "primary_key": ["uniqueid"],
                 "foreign_key": ["primaryid REFERENCES Drug(primaryid)", "indi_drug_seq REFERENCES Drug(drug_seq)"],
                },
                {"table_name" : "Drug",
                 "columns": ["uniqueid SERIAL NOT NULL","primaryid NUMERIC(1000) NOT NULL", "caseid NUMERIC(500) NOT NULL", /
                                "drug_seq NUMERIC(10)", "role_cod VARCHAR(22)", "drugname VARCHAR(500)",/
                                 "prod_ai VARCHAR(500)", "val_vbm NUMERIC(22)",/
                                "route VARCHAR(500)", "dose_vbm VARCHAR(300)", "cum_dose_chr VARCHAR(15)", "cum_dose_unit VARCHAR(50)", "dechal VARCHAR(20)", "rechal VARCHAR(20)", "lot_num VARCHAR(1000)"/
                                "exp_dt NUMERIC(1000)", "nda_num NUMERIC(100)", "dose_amt VARCHAR(15)", "dose_unit VARCHAR(50)", "dose_form VARCHAR(50)", "dose_freq VARCHAR(50)"],
                 "primary_key": ["uniqueid"],
                 "foreign_key": ["primaryid REFERENCES Demographic(primaryid)"],
                },
                {"table_name" : "Demographic",
                 "columns": ["primaryid NUMERIC(1000) NOT NULL", "caseid NUMERIC(500) NOT NULL", "caseversion NUMERIC(10)", "i_f_code VARCHAR(1)", "event_dt NUMERIC(8)", "mfr_dt NUMERIC(8)", "init_fda_dt NUMERIC(8)",/
                                "fda_dt NUMERIC(8)", "rept_cod VARCHAR(9)", "auth_num VARCHAR(500)", "mfr_num VARCHAR(500)", "mfr_sndr VARCHAR(300)", "lit_ref VARCHAR(1000)", "age NUMERIC(12, 2)", "age_cod VARCHAR(7)",/
                                "age_grp NUMERIC", "sex VARCHAR(5)", "e_sub VARCHAR(1)", "wt NUMERIC(14,5)", "wt_cod VARCHAR(20)", "rept_dt NUMERIC(8)", "to_mfr VARCHAR(100)", "occp_cod VARCHAR(300)", /
                                "reporter_country VARCHAR(500)", "occr_country VARCHAR(2)"],
                 "primary_key": ["primaryid"],
                 "foreign_key": [""],
                },
                {"table_name" : "Reaction",
                 "columns": ["uniqueid SERIAL NOT NULL","primaryid NUMERIC(1000) NOT NULL", "caseid NUMERIC(500) NOT NULL", "pt VARCHAR(500)", "drug_rec_act VARCHAR(500)"],
                 "primary_key": ["uniqueid"],
                 "foreign_key": ["primaryid REFERENCES Demographic(primaryid)"],
                },
                {"table_name" : "Outcome",
                 "columns": ["uniqueid SERIAL NOT NULL","primaryid NUMERIC(1000) NOT NULL", "caseid NUMERIC(500) NOT NULL", "outc_cod VARCHAR(4000)"],
                 "primary_key": ["uniqueid"],
                 "foreign_key": ["primaryid REFERENCES Demographic(primaryid)"],
                },
                {"table_name" : "Report_Sources",
                 "columns": ["uniqueid SERIAL NOT NULL","primaryid NUMERIC(1000) NOT NULL", "caseid NUMERIC(500) NOT NULL", "rpsr_cod VARCHAR(32)"],
                 "primary_key": ["uniqueid"],
                 "foreign_key": ["primaryid REFERENCES Demographic(primaryid)"],
                },
             "Stage": ["Therapy", "Indication", "Drug", "Demographic", "Reaction", "Outcome", "Report_Sources"]
            },
           }

    '''
    if task == "both":
        Stage("csv", "CryptoMarkets")
        Transformation()
    elif task == "stage":
        Stage("fda", "Reaction")
        #Stage("csv", "CryptoMarkets")
    elif task == "transform":
        Transformation("CryptoMarkets")
    '''
