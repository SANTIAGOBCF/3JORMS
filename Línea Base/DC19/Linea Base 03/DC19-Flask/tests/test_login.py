# import unittest
# import time
# from datetime import datetime
# from app import create_app, db
# from app.models import User, AnonymousUser, Role, Permission
# from flask_testing import LiveServerTestCase

# from selenium import webdriver


# class LoginTestCase(unittest.TestCase):
#     def setUp(self):
#         self.driver = webdriver.Chrome("chromedriver.exe")
#         self.app = create_app('testing')
#         self.app_context = self.app.app_context()
#         self.app_context.push()
#         db.create_all()
#         Role.insert_roles()

#     def tearDown(self):
#         db.session.remove()
#         db.drop_all()
#         self.app_context.pop()

#     def test_already_dni_registered(self):
#         """
#         Verifica que no se puedan crear una cuenta con un DNI ya registrado.
#         """
#         u = User(dni=76011315)
#         db.session.add(u);
#         db.session.commit();

#         self.driver.get("http://127.0.0.1:5000/auth/register")
#         self.driver.find_element_by_id("full_name").send_keys("Roger Anthony Ramos Paredes")
#         self.driver.find_element_by_id("dni").send_keys("76011315")
#         self.driver.find_element_by_id("cui").send_keys("3")
#         self.driver.find_element_by_id("email").send_keys("rogrp6@mail.com")
#         self.driver.find_element_by_id("alias").send_keys("rogrp")
#         self.driver.find_element_by_id("password").send_keys("clave1")
#         self.driver.find_element_by_id("password2").send_keys("clave1")
#         self.driver.find_element_by_id("submit").click()

#         self.assertTrue(self.driver.current_url == "http://127.0.0.1:5000/auth/register")

#         User.query.filter_by(dni=76011314).delete()
#         db.session.commit()

#     def test_new_dni_user(self):
#         """
#         Verifica que se puede crear una cuenta con un DNI que hasta el momento no ha sido registrado,
#         enviando al usuario a continuacion a la pantalla de login.
#         """
#         self.driver.get("http://127.0.0.1:5000/auth/register")
#         self.driver.find_element_by_id("full_name").send_keys("Roger Anthony Ramos Paredes")
#         self.driver.find_element_by_id("dni").send_keys("76011315")
#         self.driver.find_element_by_id("cui").send_keys("3")
#         self.driver.find_element_by_id("email").send_keys("rogrp6@mail.com")
#         self.driver.find_element_by_id("alias").send_keys("rogrp")
#         self.driver.find_element_by_id("password").send_keys("clave1")
#         self.driver.find_element_by_id("password2").send_keys("clave1")

#         self.driver.find_element_by_id("submit").click()
#         # time.sleep(3)
#         self.assertTrue(self.driver.current_url == "http://127.0.0.1:5000/auth/login")
