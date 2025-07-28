# Redux API Documentation

These are the API's available for the Redux front-end:

1. Get Suggested Properties by matching address
2. Get Home Owner / Property info
3. Submit Application

## Current API Domain
To make API calls, please use this domain: `https://portal.redux.tax/`

## Get Home Owner & Property

Retrieve Home Owner & Property information

**URL** : `api/property`

**Method** : `GET`

**URL Parameters**

Please specify one of the required parameters (either **address** or **property_id** or **code**)

* **address** / Required / Property full address
* **property_id** / Required / Property Identity Number
* **code** / Required / Generated code for Property Identity Number
* **county** / Optional / County
* **state** / Optional / State
* **zip** / Optional / Zip

### Example Requests

1. `GET https://portal.redux.tax/api/property?address=8615%20CHEVY%20CHASE%20DR%20BOCA%20RATON%2033433&county=Palm%20Beach`
2. `GET https://portal.redux.tax/api/property?property_id=2726267`
3. `GET https://portal.redux.tax/api/property?property_id=781689`
4. `GET https://portal.redux.tax/api/property?property_id=1326997`
5. `GET https://portal.redux.tax/api/property?address=570%20MONROE%20BLVD`
6. `GET https://portal.redux.tax/api/property?code=6BJISH`

### Success Response

```
{
  "payload": {
    "address_iscondo": true, 
    "address_latitude": null, 
    "address_line1": "8615 CHEVY CHASE DR", 
    "address_line2": null, 
    "address_longitude": null, 
    "address_number": "8615", 
    "address_state": "FLORIDA", 
    "address_street": "CHEVY CHASE", 
    "address_zip": 33433, 
    "full_address": "8615 CHEVY CHASE DR BOCA RATON 33433", 
    "owners": [
      "DANIEL CHAYA"
    ], 
    "property_id": 4204603
  }, 
  "status": 1
}
```


### Error Responses

1. **Request**: `GET https://portal.redux.tax/api/property`

**Response**:
```
{
    "error": "bad_request",
    "message": "Specify one of required parameters 'property_id' or 'address'"
}
```
2. **Request**: `GET https://portal.redux.tax/api/property?property_id=462024911`

**Response**:
```
{
    "error": "not_found",
    "message": "No property found"
}
```
3. **Request**: `GET https://portal.redux.tax/api/property?address=NW%20TER%20LAUDERDALE%20LAKES`

**Response**:
```

{
    "error": "multiple_found",
    "message": "Multiple properties found"
}
```

## Get Suggested Properties

Receive a list of suggested properties by providing partial address. The limit is set to 15 properties.

**URL** : `api/properties`

**Method** : `GET`

**URL Parameters**

* **address** / Required / Incomplete Property addrses
* **county** / Optional / County
* **state** / Optional / State
* **zip** / Optional / Zip

### Example Requests

1. `GET https://portal.redux.tax/api/properties?address=NW%20TER%20LAUDERDALE%20LAKES`
2. `GET https://portal.redux.tax/api/properties?address=%20STEWART%20AVE%20GARDEN%20CITY`
3. `GET https://portal.redux.tax/api/properties?address=PALM%20AVE%20MIRAMAR`
4. `GET https://portal.redux.tax/api/properties?address=COLLINS%20AVE%20714%20Miami%20Beach&zip=33141`

### Success Response

```
{
  "payload": {
    "properties": [
      {
        "address_iscondo": true, 
        "address_latitude": null, 
        "address_line1": "6969 COLLINS AVE 714", 
        "address_line2": null, 
        "address_longitude": null, 
        "address_number": "6969", 
        "address_state": "FLORIDA", 
        "address_street": " COLLINS AVE 714", 
        "address_zip": 33141, 
        "full_address": "6969 COLLINS AVE 714 Miami Beach 33141", 
        "property_id": 3207776
      }, 
      {
        "address_iscondo": true, 
        "address_latitude": null, 
        "address_line1": "7600 COLLINS AVE 714", 
        "address_line2": null, 
        "address_longitude": null, 
        "address_number": "7600", 
        "address_state": "FLORIDA", 
        "address_street": " COLLINS AVE 714", 
        "address_zip": 33141, 
        "full_address": "7600 COLLINS AVE 714 Miami Beach 33141", 
        "property_id": 3201855
      }
    ]
  }, 
  "status": 1
}
```


### Error Responses

1. **Request**: `GET https://portal.redux.tax/api/properties`

**Response**:
```
{
    "error": "missing_address",
    "message": "Required parameter 'address' was not specified"
}
```
2. **Request**: `GET https://portal.redux.tax/api/properties?address=11111%20NW%20NW%2056%20ST%20OAKLAND%20PARK`

**Response**:
```
{
    "error": "not_found",
    "message": "No property found"
} 
```

### Notes

Response contains information about the property including its unique `property_id` parameters. 
Please save the `property_id` param of a selected property as it is required for application submission.

## Submit Application

This API allows submission of the applications. On success a new application will be submitted and later reviewed by the internal staff member.

**URL** : `api/applications`

**Method** : `POST`

**Payload Parameters**

All of the parameters described below are to be in the main JSON body.

* **email**: Email of a user
* **first_name**: First Name of a user
* **last_name**: Last Name of a user
* **property_id**: Property ID of a property that user selected
* **signature_base64_encoded**: A photo of user's signature. Base64 Encoded. PNG format.
* **initials**: User's Initials
* **company_serving**: The company that does registration. In our case it must be equal 'redux'
* **application_type**: Application Type. Currently possible values: `standard`, `new_homeowner`, `misspelled_in_county_records`, `co_owner`, `authorized_signor`
* **payment_type**: Payment Type. Currently possible values: `card`, `check`
* **payment_link**: Payment link.
* **mailing_line1**: Mailing address line1 of a user
* **mailing_line2**: Mailing address line2 of a user
* **mailing_line3**: Mailing address line3 of a user
* **mailing_city**: Mailing address city of a user
* **mailing_state**: Mailing address state of a user
* **mailing_zip**: Mailing address zip of a user 
* **authorized_signer**: User confirmed they are authorized. Needs to be equal `1`/`true`.
* **text_updates_1**: Preferences for Text Updates for the first Phone Number `1`/`true` or `0`/`false`.
* **text_updates_2**: Preferences for Text Updates for the second Phone Number `1`/`true` or `0`/`false`.
* **email_updates**: Preferences for Email Updates `1`/`true` or `0`/`false`.
* **pin_entered**: Track whether user entered pin or not `1`/`true` or `0`/`false`.
* **marketing_code**: Marketing code if any
* **phone_number_1**: User's first Phone Number
* **phone_number_2**: User's second Phone Number (optional, can be null)
* **tax_year**: Tax Year of the application. Currently expected value: `2020`

## Headers requirements

Only JSON type is supported, thus a JSON header needs to be present:

`Content-Type	application/json`

### Example POST Requests

```
{
	"email": "user@alandarev.com",
	"first_name": "Daniel",
	"last_name": "Chaya",
	"property_id": 4204603,
	"signature_base64_encoded":"iVBORw0KGgoAAAANSUhEUgAAAbgAAAAvCAIAAAAevEirAAAAA3NCSVQICAjb4U/gAAAACXBIWXMAAA7EAAAOxAGVKw4bAAADTklEQVR4nO3cy25bRRjA8Zk5N9vHt5PErWrAaaJcRIUQEipIgFjyAix4CJ4HXqI7kICqC6CorapKQSLQNEJREltqnEuPL7Ed28czwx7VHRYIMPr/XuCb1V8z+qSR1loBAJgjTVP1b58BAP7rCCUAOBBKAHAglADgQCgB/O9k5537d55++cWTu83pVL98YT09H+092Pn8q3azN3GttP2//4gA8A+xQuis082mxgaB8j07vBKlqt/ZT3/+/WzP5Nf6w7PQz8eBzIS1MxUXKqGY9CdDY7I065ykDw/j4+0oCVUhF3hy3hhCCWBxaSGGg53vXxx0JzLnlQt2kolkqyJ3u0cXo3ZYOH7UfKZlJYl8Ka1vCisrH63bvV/6J70sMHLSNZdHnUc/ZOPbte2NWqM874lNKAEsLi3EZe/+163H7cuepyLP1JbEuHnjvYvReDi7PBv89Gvzt1m0JIVXEFkcViuDyifmzjeD5+1JfSVIronsdLhz7+LUTqflaqMczRlDKAEsuuXKZx/G7Z758WH39Zq525a3E7m6VUrM6jvH/bc/3oi+67TGaSsLvVZnvxW2hapuVN56o1DKn5eur34qnh+UTX+s5w8glAAWnZReoMJIVJZztz6o1mWyeX7WVIO+EULKwFdBIEvV+Fb9tXWZ1Rs6yOvTZ6P23sn+ihK1vzKArTeARSelKudv1strwdW3916cZ9oqpaQQQgopVJRfezP2BrOnu+0nA1nMie7BYPdwcHil8vOe2n/GjRLA4lJCxMV331fXt6Ik8MuzsTqy2424MfOqKq7rUuNaI6lXNpcikfPCdJq7Wb1Rt9ubvlkuFZfyG/VZSZXXhSkWw+XkFTWUfIoBYGFZIaweXVkvkIEvzUwPJ6JQ8JQ2mTFa+L6emigMldRTrY2WURgpORtPJ9Yq5YdSD42XF1orqbwgenkq0zQllADwKvweBABuhBIAHAglADgQSgBwIJQA4EAoAcCBUAKAA6EEAAdCCQAOhBIAHAglADgQSgBwIJQA4EAoAcCBUAKAA6EEAAdCCQAOhBIAHAglADgQSgBwIJQA4EAoAcCBUAKAA6EEAAdCCQAOhBIAHAglADgQSgBwIJQA4EAoAcCBUAKAA6EEAIc/ACheIhvw2VbWAAAAAElFTkSuQmCC",
	"initials":	"AK",
	"company_serving": "redux",
	"application_type": "new_homeowner",
	"payment_link": "https://www.redux.tax/pages/application-form",
	"payment_type": "card",
	"mailing_line1": "8615 CHEVY CHASE DR",
	"mailing_line2": null,
	"mailing_line3": "BOCA RATON FL 33433-1805",
	"mailing_city": "BOCA RATON",
	"mailing_state": "FL",
	"mailing_zip": "33433",
	"authorized_signer": 1,
	"text_updates_1": 1,
	"text_updates_2": 1,
	"pin_entered": 1,
	"email_updates": 1,
	"marketing_code": "Web",
	"phone_number_1": "587911173",
	"phone_number_2": "587911555",
	"tax_year": 2020
}
```

### Success Response

```
{
	"status": 1,
	"payload":	{
		"application_id": 123,
	}
}
```


### Error Responses

On any of the values received not as expected an informative error message will be provided.

**Example**

```
"message": {
	"authorized_signer":	[
		"Invalid value"
	],
	"property_id":	[
		"Property with id=429303111111 was not found"
	]
}
```
Explains there are two errors in the form: authorized_signer invalid value and invalid property id.

### Notes
When testing Application Submission, feel free to use the provided example as long as you modify the property_id to some other existing value. Otherwise the application might be rejected due to duplication constraints.

## Generate PDF

On success a new pdf file will be generated.

**URL** : `api/pdf`

**Method** : `POST`

**Payload Parameters**

All of the parameters described below are to be in the main JSON body.

* **application_type**: Application Type. Currently possible values: `standard`, `new_homeowner`, `misspelled_in_county_records`, `co_owner`, `authorized_signor`
* **marketing_code**: Marketing code if any
* **client_id**: The ID of client
* **apn**: Property APN number
* **county**: Property county. Currently possible values: `broward`, `miamidade`, `palmbeach`
* **tax_year**: The Tax Year


## Headers requirements

Only JSON type is supported, thus a JSON header needs to be present:

`Content-Type	application/json`

### Example POST Requests

```
{
	"application_type": "standard",
	"marketing_code": "Web",
	"client_id": 20,
	"apn": "484317040160",
	"tax_year": 2020,
	"county": "broward"
}
```
