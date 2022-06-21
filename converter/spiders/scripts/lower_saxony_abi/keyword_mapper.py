import logging
import os
import pprint
import re


class LoSaxKeywordMapper:
    """
    KeywordMapper for 'Abituraufgaben' from Lower Saxony
    see: https://za-aufgaben.nibis.de

    Provides discipline- and keyword-mapping for the abbreviations found in the to be parsed '.pdf'-filenames.
    """
    discipline_mapping = {
        # SkoHub discipline Mapping, see: https://github.com/openeduhub/oeh-metadata-vocabs/blob/master/discipline.ttl
        'BRC': 'Wirtschaft und Verwaltung',
        'BVW': 'Wirtschaftskunde',
        'Ernaehrung': 'Ernährung und Hauswirtschaft',
        'EvReligion': 'Religion',
        'Franz': 'Französisch',
        'GesPfl': 'Gesundheit',
        'KathReligion': 'Religion',
        'Mathe': 'Mathematik',
        'MatheTech': 'Mathematik',
        'MatheWirt': 'Mathematik',
        'PaedPsych': 'Pädagogik',
        'PolitikWirtschaft': 'Politik',
        'VW': 'Wirtschaftskunde',
        'WerteNormen': 'Ethik',
    }

    keyword_mapping = {
        # additional discipline information, specific for Lower Saxony:
        'BRC': 'Betriebswirtschaft mit Rechnungswesen-Controlling',
        'BVW': 'Betriebs- und Volkswirtschaft',
        'Ernaehrung': 'Ernährung und Hauswirtschaft',
        'EvReligion': 'Evangelische Religion',
        'Franz': 'Französisch',
        'GesPfl': 'Gesundheit-Pflege',
        'KathReligion': 'Katholische Religion',
        'Mathe': 'Mathematik',
        'MatheTech': 'Mathematik - Berufliches Gymnasium - Technik',
        'MatheWirt': 'Mathematik - Berufliches Gymnasium - Wirtschaft / Gesundheit und Soziales',
        'PaedPsych': 'Pädagogik-Psychologie',
        'PolitikWirtschaft': 'Politik-Wirtschaft',
        'VW': 'Volkswirtschaft',
        'WerteNormen': 'Werte und Normen',
        # additional keywords
        'Neu': 'Neubeginn',
        'BG': 'Berufsgymnasium (BG)',
        'ZBW': 'Zweiter Bildungsweg (ZBW) / Freie Waldorfschulen / Nichtschüler',
        'CAS': 'Computer Algebra System (CAS)',
        'GTR': 'Grafikfähiger Taschenrechner (GTR)',
        'WTR': 'Wissenschaftlicher Taschenrechner',
        'EA': 'Kurs auf erhöhtem Anforderungsniveau (eA)',
        'GA': 'Kurs auf grundlegendem Anforderungsniveau (gA)',
        'HV': 'Hörverständnis',
        'ME': 'Material',  # for students or teachers
        'L': 'Erwartungshorizont / Bewertungsbogen (Lehrer)',
        'Lehrer': 'Erwartungshorizont / Bewertungsbogen (Lehrer)',
        'mitExp': 'mit Experimentieren',
        'ohneExp': 'ohne Experimentieren',
        'mitExpElektrik': 'mit Experimentieren - Elektrik',
        'mitExpOptik': 'mit Experimentieren - Optik',
        'mitExpWellen': 'mit Experimentieren - Wellen',
        '_ALLGE': 'Allgemein (ALLGE)',
        '_LA': 'Lineare Algebra (LA)',
        '_LA_AG': 'Lineare Algebra / Analytische Geometrie (LA_AG)',
        '_STOCH': 'Stochastik (STOCH)',
        'AnlagenTSP': 'Anlagen - Thematische Schwerpunkte',
        'TS': 'Thematische Schwerpunkte / Themenschwerpunkte',
        'TSP': 'Thematische Schwerpunkte / Themenschwerpunkte'
    }
    # For Debugging:
    logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')
    pp = pprint.PrettyPrinter(indent=4)

    def extract_pdf_metadata(self, pdf_dictionary):
        """
        expects a pdf_dictionary consisting of two strings: {'filename': 'path_to_file'}
        then does a 3 step conversion:

        - sorting the pdf_entries into either 'general' or 'additional' .pdf files
        - using RegEx to extract metadata from the filename into a pdf dictionary
        - cleaning up the dictionary of 'None'-Types
        - mapping keywords

        afterwards returns two final pdf_dictionary for 'normal' and 'additional' .pdf files, where

        - key = 'unique_filename_of_a_pdf_file.pdf'
        - values = nested dictionary (with keys like 'discipline', 'year', 'pdf_path', 'keywords'

        :param pdf_dictionary: dict
        :return: pdf_dictionary_general, pdf_dictionary_additional_files
        """
        pdf_dictionary_raw = pdf_dictionary
        pdf_temp = dict()
        pdf_additional_files = dict()
        for pdf_item in pdf_dictionary_raw.keys():
            logging.debug(self.pp.pformat(pdf_item))
            if pdf_item.startswith('Anlage') or pdf_item.startswith('TSP'):
                logging.debug(f"Filtered out {pdf_item} from {pdf_dictionary_raw.get(pdf_item)}")
                pdf_additional_files.update({pdf_item: pdf_dictionary_raw.get(pdf_item)})
            else:
                regex_general = re.compile(r'(?P<year>\d{4})'
                                           r'(?P<discipline>.+?)'
                                           r'(?P<new_begin_1st>Neu)?'  # Neubeginner (2. Fremdsprache als Neubeginner)
                                           r'(?P<secondary_school_type>BG|ZBW|FWS)?'
                                           # Berufsgymnasium / Zweiter Bildungsweg / Freie Waldorfschulen?
                                           r'(?P<obligation>Pflicht)?'  # Pflichtfach
                                           r'(?P<calculator>CAS|GTR|WTR)?'
                                           # ComputerAlgebraSystem / Grafikfähiger Taschenrechner / 
                                           # Wissenschaftlicher TR 
                                           r'(?P<course_type>EA|GA)?'
                                           r'(?P<listening_comprehension>HV)?'  # Hörverständnis
                                           r'(?P<material_or_expectations>M|ME)?'
                                           # Material (für Schüler) oder Erwartungshorizont (für Lehrer)
                                           r'(?P<physics_topic>(mitExp)?(Elektrik|Optik|Wellen)?'
                                           r'|ohneExp)?'
                                           r'(?P<new_begin_2nd>Neu)?'
                                           r'(?P<math_topic>_ALLGE|_LA|_LA_AG|_STOCH)?'
                                           # Allgemein / LinAlg / analytische Geometrie / Stochastik
                                           r'(?P<attachment_2nd>Anlagen|AnlagenTSP|TS|TS\d{4})?'
                                           # TSP bzw. TS = Thematische Schwerpunkte / Themenschwerpunkte
                                           r'(?P<assignment_part>Aufg\d|A\d)?'
                                           r'(?P<teacher>Lehrer|L)?'
                                           r'(\.pdf)')
                if regex_general.search(pdf_item) is not None:
                    regex_result_dict = regex_general.search(pdf_item).groupdict()

                    # For Debugging - In case we want to see the individual (raw) RegEx results:
                    logging.debug(self.pp.pformat(regex_result_dict))

                    # filterung out the invalid (NoneType) values from the initial regex results with a temporary list:
                    only_valid_values = list()
                    for value in regex_result_dict.values():
                        if value is not None and value != '':
                            only_valid_values.append(value)

                    # Discipline-Mapping to SkoHub vocabulary:
                    if regex_result_dict.get('discipline') in self.discipline_mapping.keys():
                        regex_result_dict.update(
                            {'discipline': self.discipline_mapping.get(regex_result_dict.get('discipline'))})
                    # Mapping '<filename>Lehrer.pdf' to SkoHub intendedEndUserRole:
                    if regex_result_dict.get('teacher') is None:
                        regex_result_dict.update({'intendedEndUserRole': 'learner'})
                    elif regex_result_dict.get('teacher') == "Lehrer":
                        regex_result_dict.update({'intendedEndUserRole': 'teacher'})

                    # For Debugging - this is the 'working list' of keywords without any of the 'None'-types:
                    logging.debug(f"PDF File: {pdf_item} // only_valid_keywords: {only_valid_values}")

                    keywords_cleaned_and_mapped = list()
                    keywords_cleaned_and_mapped.append('Schriftliche Abituraufgaben Niedersachsen')
                    for potential_keyword in only_valid_values:
                        if potential_keyword in self.keyword_mapping:
                            potential_keyword = self.keyword_mapping.get(potential_keyword)
                        assignment_regex = re.compile(r"Aufg\d")
                        if assignment_regex.search(potential_keyword) is not None:
                            potential_keyword = potential_keyword.replace('Aufg', 'Aufgabe ')
                        assignment_regex = re.compile(r"A\d")
                        if assignment_regex.search(potential_keyword) is not None:
                            # matches "A1", "A2" etc. to find "Aufgabe"-acronyms
                            potential_keyword = potential_keyword.replace('A', 'Aufgabe ')
                        keywords_cleaned_and_mapped.append(potential_keyword)
                    logging.debug(self.pp.pformat(keywords_cleaned_and_mapped))

                    # TODO: keywords
                    #  - Erwartungshorizont für Lehrer
                    #  - relative / absolute path?
                    dict_of_current_pdf = {
                        pdf_item.split(os.path.sep)[-1]: {
                            'discipline': regex_result_dict.get('discipline'),
                            'year': regex_result_dict.get('year'),
                            'pdf_path': pdf_dictionary_raw.get(pdf_item),
                            'keywords': keywords_cleaned_and_mapped,
                            'intendedEndUserRole': regex_result_dict.get('intendedEndUserRole')
                        }
                    }
                    pdf_temp.update(dict_of_current_pdf)

        logging.debug(self.pp.pformat(pdf_temp))
        logging.debug(f"length of pdf_temp: {len(pdf_temp)}")
        logging.debug(f"amount of filtered out (additional) pdfs: {len(pdf_additional_files)}")
        logging.debug(f"Filtered out pdf items: {pdf_additional_files.items()}")
        # self.pp.pprint(pdf_additional_files)
        if len(pdf_additional_files) > 0:
            pdf_additional_files = self.extract_pdf_metadata_from_additional_files(pdf_dictionary=pdf_additional_files)
        return pdf_temp, pdf_additional_files

    def extract_pdf_metadata_from_additional_files(self, pdf_dictionary):
        """
        Since not all '.pdf'-filenames are following the same naming syntax, this method processes the filenames that
        can't be parsed by the more generic extract_pdf_metadata()-method.

        Expects a pdf_dictionary consisting of two strings: {'filename': 'path_to_file'}
        then does a 3 step conversion:

        - sorting the pdf_entries into either 'general' or 'additional' .pdf files
        - using RegEx to extract metadata from the filename into a pdf dictionary
        - cleaning up the dictionary of 'None'-Types
        - mapping keywords

        afterwards returns two final pdf_dictionary for 'normal' and 'additional' .pdf files, where

        - key = 'unique_filename_of_a_pdf_file.pdf'
        - values = nested dictionary (with the following keys: 'discipline', 'year', 'pdf_path', 'keywords'

        :param pdf_dictionary: dict
        :return: nested dict = { '.pdf filename': {
            'discipline': '...',
            'year': '...',
            'pdf_path': '...',
            'keywords': '...' }
            }
        """
        pdf_working_dict = pdf_dictionary
        pdf_filenames_and_metadata_dict = dict()
        for pdf_filename in pdf_working_dict.keys():
            regex_additional_files = re.compile(r'(?P<attachment>Anlage .+ im Fach|TSP)?'
                                                r'(?P<discipline>.+?)'
                                                r'(?P<attachment_2nd>TS)?'
                                                r'(?P<year>\d{4})?'
                                                r'(?P<attachment_3rd>Anlagen)?'
                                                r'(.pdf)')
            if regex_additional_files.search(pdf_filename) is not None:
                regex_result_dict_temporary: dict = regex_additional_files.search(pdf_filename).groupdict()
                logging.debug(self.pp.pformat(regex_result_dict_temporary))

                # extract and clean up the keyword-list:
                only_valid_values = list()
                for value in regex_result_dict_temporary.values():
                    if value is not None and value != '':
                        only_valid_values.append(value)
                logging.debug(only_valid_values)

                # Discipline-Mapping to SkoHub vocabulary:
                if regex_result_dict_temporary.get('discipline') in self.discipline_mapping.keys():
                    regex_result_dict_temporary.update(
                        {'discipline': self.discipline_mapping.get(regex_result_dict_temporary.get('discipline'))})

                keywords_cleaned_and_mapped = list()
                for potential_keyword in only_valid_values:
                    if potential_keyword in self.keyword_mapping:
                        potential_keyword = self.keyword_mapping.get(potential_keyword)
                    keywords_cleaned_and_mapped.append(potential_keyword)
                keywords_cleaned_and_mapped.append('Schriftliche Abituraufgaben Niedersachsen')

                logging.debug(self.pp.pformat(keywords_cleaned_and_mapped))
                dict_of_current_pdf = {
                    pdf_filename: {
                        'discipline': regex_result_dict_temporary.get('discipline'),
                        'year': regex_result_dict_temporary.get('year'),
                        'pdf_path': pdf_working_dict.get(pdf_filename),
                        'keywords': keywords_cleaned_and_mapped
                    }
                }
                pdf_filenames_and_metadata_dict.update(dict_of_current_pdf)
        return pdf_filenames_and_metadata_dict
