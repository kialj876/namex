import pytest
import jsonpickle

from urllib.parse import quote_plus

from namex.services.name_request.auto_analyse import AnalysisIssueCodes

from ...common import assert_issues_count_is_gt, assert_has_word_upper, save_words_list_classification, save_words_list_virtual_word_condition
from ..common import ENDPOINT_PATH
from ...common import token_header, claims


@pytest.mark.xfail(raises=ValueError)
def test_name_requires_consent_compound_word_request_response(client, jwt, app):
    words_list_classification = [{'word': 'CANADIAN', 'classification': 'DIST'},
                                 {'word': 'CANADIAN', 'classification': 'DESC'},
                                 {'word': 'SUMMERS', 'classification': 'DIST'},
                                 {'word': 'SUMMERS', 'classification': 'DESC'},
                                 {'word': 'GAMES', 'classification': 'DIST'},
                                 {'word': 'GAMES', 'classification': 'DESC'},
                                 {'word': 'BLAKE', 'classification': 'DIST'},
                                 {'word': 'BLAKE', 'classification': 'DESC'},
                                 {'word': 'ENGINEERING', 'classification': 'DIST'},
                                 {'word': 'ENGINEERING', 'classification': 'DESC'}
                                 ]
    save_words_list_classification(words_list_classification)

    words_list_virtual_word_condition = [
        {
            'words': 'SUMMER GAMES, WINTER GAMES',
            'consent_required': True, 'allow_use': True
        },
        {
            'words': 'CONSULTING ENGINEER, ENGINEER, ENGINEERING, INGENIERE, INGENIEUR, INGENIEUR CONSIEL, P ENG, PROFESSIONAL ENGINEER',
            'consent_required': True, 'allow_use': True
        }
    ]
    save_words_list_virtual_word_condition(words_list_virtual_word_condition)

    # create JWT & setup header with a Bearer Token using the JWT
    token = jwt.create_jwt(claims, token_header)
    headers = {'Authorization': 'Bearer ' + token, 'content-type': 'application/json'}

    test_params = [
        {
            'name': 'CANADIAN SUMMERS GAMES LIMITED',
            'location': 'BC',
            'entity_type': 'CR',
            'request_action': 'NEW'
        },
        {
            'name': 'BLAKE ENGINEERING LTD.',
            'location': 'BC',
            'entity_type': 'CR',
            'request_action': 'NEW'
        }
    ]

    for entry in test_params:
        query = '&'.join("{!s}={}".format(k, quote_plus(v)) for (k, v) in entry.items())
        path = ENDPOINT_PATH + '?' + query
        print('\n' + 'request: ' + path + '\n')
        response = client.get(path, headers=headers)
        payload = jsonpickle.decode(response.data)
        print("Assert that the payload contains issues")
        if isinstance(payload.get('issues'), list):
            assert_issues_count_is_gt(0, payload.get('issues'))
            assert_has_word_upper(AnalysisIssueCodes.NAME_REQUIRES_CONSENT, payload.get('issues'))
