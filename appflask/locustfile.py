from locust import task, HttpUser, between


class CreateApplication(HttpUser):
    wait_time = between(1, 1)

    # def on_start(self):
    #     self.client.post("/login", {"username": "iammashed", "password": "1"})
    #
    # def on_stop(self):
    #     self.client.get("/logout")

    @task
    def profile(self):
        """
        To invoke locally run in terminal
        $locust -f locustfile.py --host=http://localhost:5001
        """
        self.client.post(
            "/api/applications",
            json={
                "email": "rustamallakov@gmail.com",
                "first_name": "Rustam",
                "last_name": "Allakov",
                "property_id": 4204603,
                "signature_base64_encoded": "iVBORw0KGgoAAAANSUhEUgAAAbgAAAAvCAIAAAAevEirAAAAA3NCSVQICAjb4U/gAAAACXBI"
                                            "WXMAAA7EAAAOxAGVKw4bAAADTklEQVR4nO3cy25bRRjA8Zk5N9vHt5PErWrAaaJcRIUQEipI"
                                            "gFjyAix4CJ4HXqI7kICqC6CorapKQSLQNEJREltqnEuPL7Ed28czwx7VHRYIMPr/XuCb1V8z"
                                            "+qSR1loBAJgjTVP1b58BAP7rCCUAOBBKAHAglADgQCgB/O9k5537d55++cWTu83pVL98YT09"
                                            "H+092Pn8q3azN3GttP2//4gA8A+xQuis082mxgaB8j07vBKlqt/ZT3/+/WzP5Nf6w7PQz8eB"
                                            "zIS1MxUXKqGY9CdDY7I065ykDw/j4+0oCVUhF3hy3hhCCWBxaSGGg53vXxx0JzLnlQt2kolk"
                                            "qyJ3u0cXo3ZYOH7UfKZlJYl8Ka1vCisrH63bvV/6J70sMHLSNZdHnUc/ZOPbte2NWqM874lN"
                                            "KAEsLi3EZe/+163H7cuepyLP1JbEuHnjvYvReDi7PBv89Gvzt1m0JIVXEFkcViuDyifmzjeD"
                                            "5+1JfSVIronsdLhz7+LUTqflaqMczRlDKAEsuuXKZx/G7Z758WH39Zq525a3E7m6VUrM6jvH"
                                            "/bc/3oi+67TGaSsLvVZnvxW2hapuVN56o1DKn5eur34qnh+UTX+s5w8glAAWnZReoMJIVJZz"
                                            "tz6o1mWyeX7WVIO+EULKwFdBIEvV+Fb9tXWZ1Rs6yOvTZ6P23sn+ihK1vzKArTeARSelKudv"
                                            "1strwdW3916cZ9oqpaQQQgopVJRfezP2BrOnu+0nA1nMie7BYPdwcHil8vOe2n/GjRLA4lJC"
                                            "xMV331fXt6Ik8MuzsTqy2424MfOqKq7rUuNaI6lXNpcikfPCdJq7Wb1Rt9ubvlkuFZfyG/VZ"
                                            "SZXXhSkWw+XkFTWUfIoBYGFZIaweXVkvkIEvzUwPJ6JQ8JQ2mTFa+L6emigMldRTrY2WURgp"
                                            "ORtPJ9Yq5YdSD42XF1orqbwgenkq0zQllADwKvweBABuhBIAHAglADgQSgBwIJQA4EAoAcCB"
                                            "UAKAA6EEAAdCCQAOhBIAHAglADgQSgBwIJQA4EAoAcCBUAKAA6EEAAdCCQAOhBIAHAglADgQ"
                                            "SgBwIJQA4EAoAcCBUAKAA6EEAAdCCQAOhBIAHAglADgQSgBwIJQA4EAoAcCBUAKAA6EEAIc/"
                                            "ACheIhvw2VbWAAAAAElFTkSuQmCC",
                "initials": "AK",
                "company_serving": "redux",
                "application_type": "new_homeowner",
                "payment_type": "card",
                "mailing_line1": "8615 CHEVY CHASE DR",
                "mailing_line2": None,
                "mailing_line3": "BOCA RATON FL 33433-1805",
                "mailing_city": "BOCA RATON",
                "mailing_state": "FL",
                "mailing_zip": "33433",
                "authorized_signer": 1,
                "text_updates_1": 1,
                "text_updates_2": 1,
                "email_updates": 1,
                "marketing_code": "Web",
                "phone_number_1": "587911173",
                "phone_number_2": "587911555",
                "tax_year": 2020
            }
        )
