# This file is part of Workout Manager.
#
# Workout Manager is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Workout Manager is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License

import logging

from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from wger.manager.tests.testcase import WorkoutManagerTestCase

logger = logging.getLogger('workout_manager.custom')


class RegistrationTestCase(WorkoutManagerTestCase):
    '''
    Tests registering a new user
    '''

    def test_register(self):

        # Fetch the registration page
        response = self.client.get(reverse('registration'))
        self.assertEqual(response.status_code, 200)

        # Fill in the registration form
        registration_data = {'username': 'myusername',
                             'password1': 'secret',
                             'password2': 'secret',
                             'email': 'not an email',
                             'recaptcha_response_field': 'PASSED', }
        count_before = User.objects.count()

        # Wrong email
        response = self.client.post(reverse('registration'), registration_data)
        self.assertFalse(response.context['form'].is_valid())
        self.user_logout()

        # Correct email
        registration_data['email'] = 'my.email@example.com'
        response = self.client.post(reverse('registration'), registration_data)
        count_after = User.objects.count()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(count_before + 1, count_after)
        self.user_logout()

        # Username already exists
        response = self.client.post(reverse('registration'), registration_data)
        count_after = User.objects.count()
        self.assertFalse(response.context['form'].is_valid())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(count_before + 1, count_after)

        # Email already exists
        registration_data['username'] = 'my.other.username'
        response = self.client.post(reverse('registration'), registration_data)
        count_after = User.objects.count()
        self.assertFalse(response.context['form'].is_valid())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(count_before + 1, count_after)

        # No email
        registration_data['email'] = ''
        response = self.client.post(reverse('registration'), registration_data)
        count_after = User.objects.count()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(count_before + 2, count_after)

        # Already logged in
        response = self.client.post(reverse('registration'), registration_data)
        count_after = User.objects.count()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(count_before + 2, count_after)
        self.assertIn('dashboard', response['Location'])
