import base64
import json
import os
from datetime import datetime
import filetype
from .hik_dataclasses import HikDevice
from .hik_error import HikDeviceGatewayError


class HikAccessControl:

    def add_person(self, device: HikDevice, employee_num: str, name: str, begin_time: datetime, end_time: datetime):
        if begin_time.replace(second=0, microsecond=0).isoformat() == end_time.replace(second=0,
                                                                                       microsecond=0).isoformat():
            raise HikDeviceGatewayError('Begin and End DateTimes cannot be the same.')

        raw = '''{
            "UserInfo": [
                {
                    "employeeNo": "",
                    "name": "",
                    "Valid": {
                        "beginTime": "2017-01-01T00:00:00",
                        "endTime": "2027-12-31T23:59:59"
                    }
                }
            ]
        }'''
        json_body = json.loads(raw)
        json_body['UserInfo'][0]['employeeNo'] = employee_num
        json_body['UserInfo'][0]['name'] = name
        json_body['UserInfo'][0]['Valid']['beginTime'] = begin_time.replace(second=0, microsecond=0).isoformat()
        json_body['UserInfo'][0]['Valid']['endTime'] = end_time.replace(second=0, microsecond=0).isoformat()

        url_path_params = f"/ISAPI/AccessControl/UserInfo/Record?format=json&devIndex={device.devIndex}"
        response = self.json_query(
            "POST",
            self.baseurl + url_path_params,
            json_body)

        if 'errorMsg' in response:
            raise HikDeviceGatewayError(response['errorMsg'])

        if 'UserInfoOutList' not in response:
            raise HikDeviceGatewayError("'UserInfoOutList' missing from response body.")

        if 'UserInfoOut' not in response['UserInfoOutList']:
            raise HikDeviceGatewayError("'UserInfoOut' missing from response body.")

        if not isinstance(response['UserInfoOutList']['UserInfoOut'], list):
            raise HikDeviceGatewayError("'UserInfoOut' is not a list.")

        if len(response['UserInfoOutList']['UserInfoOut']) == 0:
            return []

        if 'statusCode' not in response['UserInfoOutList']['UserInfoOut'][0]:
            raise HikDeviceGatewayError("'statusCode' missing from response body.")

        if response['UserInfoOutList']['UserInfoOut'][0]['statusCode'] != 1:
            if 'errorMsg' in response['UserInfoOutList']['UserInfoOut'][0]:
                raise HikDeviceGatewayError(response['UserInfoOutList']['UserInfoOut'][0]['errorMsg'])
            else:
                raise HikDeviceGatewayError(
                    f"Error - StatusCode: {str(response['UserInfoOutList']['UserInfoOut'][0]['statusCode'])}")

        return True

    def delete_person(self, device: HikDevice, employee_num: str):
        raw = '''{
            "UserInfoDetail": {
                "mode": "byEmployeeNo",
                "EmployeeNoList": [
                    {
                        "employeeNo": "123456"
                    }
                ]
            }
        }'''
        json_body = json.loads(raw)
        json_body['UserInfoDetail']['EmployeeNoList'][0]['employeeNo'] = employee_num

        url_path_params = f"/ISAPI/AccessControl/UserInfoDetail/Delete?format=json&devIndex={device.devIndex}"
        response = self.json_query(
            "PUT",
            self.baseurl + url_path_params,
            json_body)

        if 'statusCode' not in response:
            raise HikDeviceGatewayError("'statusCode' missing from response body.")

        if response['statusCode'] != 1:
            if 'errorMsg' in response:
                raise HikDeviceGatewayError(response['errorMsg'])
            else:
                raise HikDeviceGatewayError(f"Error - StatusCode: {str(response['statusCode'])}")

        return True

    def add_card(self, device: HikDevice, employee_num: str, card_num: str):
        raw = '''{
            "CardInfo": {
                "employeeNo": "123456",
                "cardNo": "1234567890"
            }
        }'''
        json_body = json.loads(raw)
        json_body['CardInfo']['employeeNo'] = employee_num
        json_body['CardInfo']['cardNo'] = card_num

        url_path_params = f"/ISAPI/AccessControl/CardInfo/Record?format=json&devIndex={device.devIndex}"
        response = self.json_query(
            "POST",
            self.baseurl + url_path_params,
            json_body)

        if 'statusCode' not in response:
            raise HikDeviceGatewayError("'statusCode' missing from response body.")

        if response['statusCode'] != 1:
            if 'errorMsg' in response:
                raise HikDeviceGatewayError(response['errorMsg'])
            else:
                raise HikDeviceGatewayError(f"Error - StatusCode: {str(response['statusCode'])}")

        return True

    def delete_card(self, device: HikDevice, card_num: str):
        raw = '''{
            "CardInfoDelCond": {
                "CardNoList": [
                    {
                        "cardNo": "1234567890"
                    }
                ]
            }
        }'''
        json_body = json.loads(raw)
        json_body['CardInfoDelCond']['CardNoList'][0]['cardNo'] = card_num

        url_path_params = f"/ISAPI/AccessControl/CardInfo/Delete?format=json&devIndex={device.devIndex}"
        response = self.json_query(
            "PUT",
            self.baseurl + url_path_params,
            json_body)

        if 'statusCode' not in response:
            raise HikDeviceGatewayError("'statusCode' missing from response body.")

        if response['statusCode'] != 1:
            if 'errorMsg' in response:
                raise HikDeviceGatewayError(response['errorMsg'])
            else:
                raise HikDeviceGatewayError(f"Error - StatusCode: {str(response['statusCode'])}")

        return True

    def add_face(self, device: HikDevice, employee_num: str,
                 face_img_filepath: str = None,
                 face_img_base64: str = None):
        raw = '''{
                    "FaceInfo": {
                        "employeeNo": "123456"
                    }
                }'''

        json_body = json.loads(raw)
        json_body['FaceInfo']['employeeNo'] = employee_num

        files = None
        if face_img_filepath is not None:
            if not os.path.isfile(face_img_filepath):
                raise HikDeviceGatewayError(f'Failed to find {face_img_filepath}')

            if not filetype.is_image(face_img_filepath):
                raise HikDeviceGatewayError(f'{face_img_filepath} is not an image')

            files = {
                'data': (None, json.dumps(json_body).encode('ascii'), 'application/json'),
                'FaceDataRecord': (None, open(face_img_filepath, 'rb'), 'image/jpeg')
            }

        if face_img_base64 is not None:
            files = {
                'data': (None, json.dumps(json_body).encode('ascii'), 'application/json'),
                'FaceDataRecord': (None, base64.b64decode(face_img_base64.encode('ascii')), 'image/jpeg')
            }

        if files is None:
            raise HikDeviceGatewayError("Valid image not provided.")

        url_path_params = f"/ISAPI/Intelligent/FDLib/FaceDataRecord?format=json&devIndex={device.devIndex}"
        response = self.json_query(
            "POST",
            self.baseurl + url_path_params,
            None,
            files=files)

        if 'statusCode' not in response:
            raise HikDeviceGatewayError("'statusCode' missing from response body.")

        if response['statusCode'] != 1:
            if 'errorMsg' in response:
                if 'subStatusCode' in response:
                    raise HikDeviceGatewayError(f"{response['errorMsg']} - {response['subStatusCode']}")
                raise HikDeviceGatewayError(response['errorMsg'])
            else:
                raise HikDeviceGatewayError(f"Error - StatusCode: {str(response['statusCode'])}")

        return True

    def delete_face(self, device: HikDevice, employee_num: str):
        raw = '''{
            "FaceInfoDelCond": {
                "EmployeeNoList": [
                    {
                        "employeeNo": "123456"
                    }
                ]
            }
        }'''
        json_body = json.loads(raw)
        json_body['FaceInfoDelCond']['EmployeeNoList'][0]['employeeNo'] = employee_num

        url_path_params = f"/ISAPI/Intelligent/FDLib/FDSearch/Delete?format=json&devIndex={device.devIndex}"
        response = self.json_query(
            "PUT",
            self.baseurl + url_path_params,
            json_body)

        if 'statusCode' not in response:
            raise HikDeviceGatewayError("'statusCode' missing from response body.")

        if response['statusCode'] != 1:
            if 'errorMsg' in response:
                raise HikDeviceGatewayError(response['errorMsg'])
            else:
                raise HikDeviceGatewayError(f"Error - StatusCode: {str(response['statusCode'])}")

        return True
