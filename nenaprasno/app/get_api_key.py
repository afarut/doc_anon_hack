import requests


def get_iam_token():
	headers = {
	    'Content-Type': 'application/x-www-form-urlencoded',
	}

	data = '{"yandexPassportOauthToken":"y0_AgAAAAB2DmlFAATuwQAAAAEHmqNuAADPprX_ktRPFraUoikIhPQHMI-XGA"}'

	response = requests.post('https://iam.api.cloud.yandex.net/iam/v1/tokens', headers=headers, data=data)
	return response.json()


print(get_iam_token())
