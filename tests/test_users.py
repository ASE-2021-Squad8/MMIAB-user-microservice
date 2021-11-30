import unittest
import os
import json


class TestUsers(unittest.TestCase):
    def setUp(self):
        from mib import create_app
        os.environ["FLASK_ENV"] = "testing"
        self.app = create_app()
        self.client = self.app.test_client()
        self._ctx = self.app.test_request_context()
        self._ctx.push()

    def test_01_create_user(self):
        # Create a user
        user = dict(
            firstname="Mario",
            lastname="Rossi",
            email="mario.rossi@example.org",
            dateofbirth="2000-01-01",
            password="abcd1234",
        )
        reply = self.client.post(
            "/api/user", data=json.dumps(user), content_type="application/json"
        )
        assert reply.status_code == 201

        # Try to create a user with an already registered email
        reply = self.client.post(
            "/api/user", data=json.dumps(user), content_type="application/json"
        )
        assert reply.status_code == 200

    def test_02_get_user_by_id(self):
        # Try to get user with id 9999
        reply = self.client.get("/api/user/9999")
        assert reply.status_code == 404

        # Get user with id 1
        reply = self.client.get("/api/user/1")
        user = reply.get_json()
        assert user["id"] == 1
        assert user["email"] == "mario.rossi@example.org"

    def test_03_get_user_public_details(self):
        # Try to get user with id 9999
        reply = self.client.get("/api/user/9999/public")
        assert reply.status_code == 404

        # Get user with id 1
        reply = self.client.get("/api/user/1/public")
        assert reply.status_code == 200
        user = reply.get_json()
        assert user["email"] == "mario.rossi@example.org"

    def test_04_get_email_of_user(self):
        # Try to get user with id 9999
        reply = self.client.get("/api/user/9999/email")
        assert reply.status_code == 404

        # Get user with id 1
        reply = self.client.get("/api/user/1/email")
        assert reply.status_code == 200
        user = reply.get_json()
        assert user["email"] == "mario.rossi@example.org"

    def test_05_get_user_by_email(self):
        # Try to get user with email unknown
        reply = self.client.get("/api/user_email/unknown@unknown.unknown")
        assert reply.status_code == 404

        # Get user with email mario.rossi@example.org
        reply = self.client.get("/api/user_email/mario.rossi@example.org")
        assert reply.status_code == 200
        user = reply.get_json()
        assert user["email"] == "mario.rossi@example.org"

    def test_06_get_users_list(self):
        # Get user public list
        reply = self.client.get("/api/user/list")
        assert reply.status_code == 200
        users = reply.get_json()
        assert len(users) == 1
        assert users[0]["id"] == 1
        assert users[0]["email"] == "mario.rossi@example.org"

    def test_07_public_users_list(self):
        # Get user public list
        reply = self.client.get("/api/user/list/public")
        assert reply.status_code == 200
        users = reply.get_json()
        assert len(users) == 1
        assert users[0]["email"] == "mario.rossi@example.org"

    def test_08_get_blacklist(self):
        # Try to get the blacklist of an unknown user
        reply = self.client.get("/api/user/black_list/9999")
        assert reply.status_code == 404

        # Check that candidates and blacklisted users are []
        reply = self.client.get("/api/user/black_list/1")
        assert reply.status_code == 200
        blacklist = reply.get_json()
        candidates = blacklist["candidates"]
        blacklisted = blacklist["blacklisted"]
        assert len(candidates) == 0
        assert len(blacklisted) == 0

    def test_09_authentication(self):
        # Try to test to test a user's authentication phase
        reply = self.client.post(
            "/api/authenticate",
            data=json.dumps(
                dict(
                    email="unknown@example.org",
                    password="abcd1234",
                )
            ),
            content_type="application/json",
        )
        assert reply.status_code == 400

        reply = self.client.post(
            "/api/authenticate",
            data=json.dumps(
                dict(
                    email="mario.rossi@example.org",
                    password="errpass",
                )
            ),
            content_type="application/json",
        )
        assert reply.status_code == 400

        reply = self.client.post(
            "/api/authenticate",
            data=json.dumps(
                dict(
                    email="mario.rossi@example.org",
                    password="abcd1234",
                )
            ),
            content_type="application/json",
        )
        assert reply.status_code == 200
        response_data = reply.get_json()
        assert response_data["authentication"] == "success"

    def test_10_change_password(self):
        # Try to change the password of an unknown user
        reply = self.client.put(
            "/api/user/password/9999",
            data=json.dumps(
                dict(currentpassword="", newpassword="", confirmpassword="")
            ),
            content_type="application/json",
        )
        assert reply.status_code == 404

        # Try to change the password using a wrong current password
        reply = self.client.put(
            "/api/user/password/1",
            data=json.dumps(
                dict(currentpassword="wrong", newpassword="new", confirmpassword="new")
            ),
            content_type="application/json",
        )
        assert reply.status_code == 401

        # Try to change the password with new pw and confirmation pw not matching
        reply = self.client.put(
            "/api/user/password/1",
            data=json.dumps(
                dict(currentpassword="abcd1234", newpassword="1", confirmpassword="2")
            ),
            content_type="application/json",
        )
        assert reply.status_code == 422

        # Correctly change the password
        reply = self.client.put(
            "/api/user/password/1",
            data=json.dumps(
                dict(
                    currentpassword="abcd1234",
                    newpassword="new",
                    confirmpassword="new",
                )
            ),
            content_type="application/json",
        )
        assert reply.status_code == 200

        # Check the authentication with the new password
        reply = self.client.post(
            "/api/authenticate",
            data=json.dumps(dict(email="mario.rossi@example.org", password="new")),
            content_type="application/json",
        )

        # Restore old password
        reply = self.client.put(
            "/api/user/password/1",
            data=json.dumps(
                dict(
                    currentpassword="new",
                    newpassword="abcd1234",
                    confirmpassword="abcd1234",
                )
            ),
            content_type="application/json",
        )
        assert reply.status_code == 200

    def test_11_modify_user_data(self):
        # Try to modify the data of an unknown user
        reply = self.client.put(
            "/api/user/data/9999",
            data=json.dumps(
                dict(
                    textemail="email@email.com",
                    textfirstname="firstname",
                    textlastname="lastname",
                    textbirth="2000-01-01",
                )
            ),
            content_type="application/json",
        )
        assert reply.status_code == 404

        # Try to change the email to an email that already exists in the db
        reply = self.client.post(
            "/api/user",
            data=json.dumps(
                dict(
                    firstname="Luca",
                    lastname="Bianchi",
                    email="luca.bianchi@example.org",
                    dateofbirth="2000-01-01",
                    password="abcd1234",
                )
            ),
            content_type="application/json",
        )
        assert reply.status_code == 201
        reply = self.client.put(
            "/api/user/data/1",
            data=json.dumps(
                dict(
                    textemail="luca.bianchi@example.org",
                    textfirstname="Mario",
                    textlastname="Rossi",
                    textbirth="2000-01-01",
                )
            ),
            content_type="application/json",
        )
        assert reply.status_code == 409

        # Change the user data
        reply = self.client.put(
            "/api/user/data/1",
            data=json.dumps(
                dict(
                    textemail="mario.rossi.new@example.org",
                    textfirstname="Mario_new",
                    textlastname="Rossi_new",
                    textbirth="1900-01-01",
                )
            ),
            content_type="application/json",
        )
        assert reply.status_code == 200

        # Check the data has been changed
        reply = self.client.get("/api/user/1")
        user = reply.get_json()
        assert user["email"] == "mario.rossi.new@example.org"
        assert user["firstname"] == "Mario_new"
        assert user["lastname"] == "Rossi_new"
        assert user["dateofbirth"] == "1900-01-01"

        # Restore old data
        reply = self.client.put(
            "/api/user/data/1",
            data=json.dumps(
                dict(
                    textemail="mario.rossi@example.org",
                    textfirstname="Mario",
                    textlastname="Rossi",
                    textbirth="2000-01-01",
                )
            ),
            content_type="application/json",
        )
        assert reply.status_code == 200

    def test_12_set_content_filter(self):
        # Try to set content filter to a user with a non-existent id
        reply = self.client.put(
            "/api/user/content_filter/9999",
            data=json.dumps(dict(filter=0)),
            content_type="application/json",
        )
        assert reply.status_code == 404

        # Try to set content filter to a user with a existent id
        reply = self.client.put(
            "/api/user/content_filter/1",
            data=json.dumps(dict(filter=1)),
            content_type="application/json",
        )
        assert reply.status_code == 200

        # Try take the user's data and then verify that the content filter has been correctly updated
        reply = self.client.get("/api/user/1")
        user = reply.get_json()
        assert user["id"] == 1
        assert user["email"] == "mario.rossi@example.org"
        assert user["content_filter"] == True

    def test_13_add_points_user(self):
        # Try to add points to a user with a non-existent id
        reply = self.client.put(
            "/api/user/points/9999",
            data=json.dumps(dict(points=60)),
            content_type="application/json",
        )
        assert reply.status_code == 404

        # Try to add points to a user with a existent id
        reply = self.client.put(
            "/api/user/points/1",
            data=json.dumps(dict(points=60)),
            content_type="application/json",
        )
        assert reply.status_code == 200

        # Try take the user's data and then
        # verify that the point has been correctly updated
        reply = self.client.get("/api/user/1")
        user = reply.get_json()
        assert user["id"] == 1
        assert user["email"] == "mario.rossi@example.org"
        assert user["points"] == 60

    def test_14_get_recipients_for_user(self):
        # Try to get the recipients for an unknown user
        reply = self.client.get("/api/user/9999/recipients")
        assert reply.status_code == 404

        # Get the list of recipients for the user 1
        # It should contain Luca Bianchi created in test_11_modify_user_data
        reply = self.client.get("/api/user/1/recipients")
        assert reply.status_code == 200
        recipients = reply.get_json()
        assert recipients[0]["id"] == 2
        assert recipients[0]["email"] == "luca.bianchi@example.org"

    def test_15_modify_black_list(self):
        # Try to add to the blacklist of an unknown user
        reply = self.client.put(
            "/api/user/black_list/9999",
            data=json.dumps(dict(
                op="add",
                users=[dict(id=1)],
            )),
            content_type="application/json"
        )
        
        # Create a new user
        reply = self.client.post(
            "/api/user",
            data=json.dumps(
                dict(
                    firstname="Fabio",
                    lastname="Verdi",
                    email="fabio.verdi@example.org",
                    dateofbirth="2000-01-01",
                    password="abcd1234",
                )
            ),
            content_type="application/json",
        )
        assert reply.status_code == 201

        # Add to blacklist Luca Bianchi (created in test_11_modify_user_data)
        reply = self.client.put(
            "/api/user/black_list/1",
            data=json.dumps(dict(
                op="add",
                users=[dict(id=2)],
            )),
            content_type="application/json"
        )
        assert reply.status_code == 200
        blacklist = reply.get_json()
        assert len(blacklist["blacklisted"]) == 1
        assert len(blacklist["candidates"]) == 1
        assert blacklist["blacklisted"][0]["id"] == 2
        assert blacklist["candidates"][0]["id"] == 3

        # Remove from blacklist Luca Bianchi
        reply = self.client.put(
            "/api/user/black_list/1",
            data=json.dumps(dict(
                op="delete",
                users=[dict(id=2)],
            )),
            content_type="application/json"
        )
        assert reply.status_code == 200
        blacklist = reply.get_json()
        assert len(blacklist["blacklisted"]) == 0
        assert len(blacklist["candidates"]) == 2
        assert blacklist["candidates"][0]["id"] == 2
        assert blacklist["candidates"][1]["id"] == 3

    def test_16_unregister_user(self):
        #Try to unsubscribe user with non-existent id
        reply = self.client.delete("/api/user/9999")
        assert reply.status_code == 404
        
        # Try to unsubscribe user Luca Bianchi (registered in test_11_modify_user_data)
        reply = self.client.delete("/api/user/2")
        assert reply.status_code == 200

        # Try take the user's data and then
        # verify that the user Luca Bianchi was successfully unsubscribed
        reply = self.client.get("/api/user/2")
        user = reply.get_json()
        assert user["email"] == "luca.bianchi@example.org"
        assert user["is_active"] == False

        #Try to authenticate with unsubscribed user
        reply = self.client.post(
            "/api/authenticate",
            data=json.dumps(dict(email="luca.bianchi@example.org", password="abcd1234")),
            content_type="application/json",
        )
        assert reply.status_code == 400
        
        

    def test_17_get_unregistered_users_list(self):
        #Try to get the list of unsubscribed users
        reply = self.client.get("/api/user/list/unregistered")
        assert reply.status_code == 200
        
        unregistered_userlist = reply.get_json()
        assert len(unregistered_userlist) == 1  
        assert unregistered_userlist[0]["id"] == 2    

    def test_18_report_user(self):
        # Try to report an unknown user
        reply = self.client.put(
            "/api/user/report",
            data=json.dumps(dict(useremail="unknown@unknown.com")),
            content_type="application/json"
        )
        assert reply.status_code == 404

        # Report Fabio Verdi 3 times (created in test_15_modify_black_list)
        for i in range(1,4):
            reply = self.client.put(
                "/api/user/report",
                data=json.dumps(dict(useremail="fabio.verdi@example.org")),
                content_type="application/json"
            )
            assert reply.status_code == 200
            # Check that reports == i
            reply = self.client.get("/api/user/3")
            user = reply.get_json()
            assert user["reports"] == i

        # Check that Fabio Verdi is not active anymore
        reply = self.client.get("/api/user/3")
        user = reply.get_json()
        assert user["email"] == "fabio.verdi@example.org"
        assert user["is_active"] == False

        # Try to authenticate with Fabio Verdi
        reply = self.client.post(
            "/api/authenticate",
            data=json.dumps(dict(email="fabio.verdi@example.org", password="new")),
            content_type="application/json",
        )
        assert reply.status_code == 400

    def test_19_get_banned_users_list(self):
        # Check that the banned user list only contains Fabio Verdi (created in test_15_modify_user_data)
        reply = self.client.get("/api/user/list/banned")
        assert reply.status_code == 200
        users = reply.get_json()
        assert len(users) == 1
        assert users[0]["id"] == 3
