import json
import logging

import xmltodict

from .exceptions import ApiError

logger = logging.getLogger(__name__)


class JsonParser:
    def parse_response(self, content):
        try:
            parsed_content = json.loads(content)
        except (ValueError, TypeError) as error_message:
            raise ApiError('Api returned wrong JSON: {}'.format(error_message))
        else:
            content = parsed_content.get('Response', {})
            if content.get('ErrorCode') != 0:
                msg = 'Api Error {}'.format(content.get('ErrorMessage', ''))
                logger.error(msg)
                raise ApiError(msg)
            return parsed_content


class XMLParser:
    def parse_response(self, content):
        try:
            parsed_content = xmltodict.parse(content)
        except ValueError as error_message:
            raise ApiError('Api returned wrong XML: {}'.format(error_message))
        else:
            errors = parsed_content.get('Errors', {})
            if errors:
                raise ApiError('Api Error {}'.format(errors.get('ErrorMessage', '')))
            return parsed_content
