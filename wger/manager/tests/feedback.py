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

from django.core.urlresolvers import reverse
from django.core import mail

from wger.manager.models import Workout

from wger.manager.tests.testcase import WorkoutManagerTestCase
from wger.manager.tests.testcase import WorkoutManagerDeleteTestCase
from wger.manager.tests.testcase import WorkoutManagerEditTestCase


class FeedbackTestCase(WorkoutManagerTestCase):
    '''
    Tests the feedback form
    '''

    def send_feedback(self, logged_in=True):
        '''
        Helper function
        '''
        response = self.client.get(reverse('feedback'))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse('feedback'),
                                    {'comment': 'A very long and interesting comment'})
        if logged_in:
            self.assertEqual(response.status_code, 302)
            self.assertEqual(len(mail.outbox), 1)
            response = self.client.get(response['Location'])
            self.assertEqual(response.status_code, 200)

            # Short comment
            response = self.client.post(reverse('feedback'), {'comment': '12345'})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(response.context['form'].errors), 1)
        else:
            # No recaptcha field
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(mail.outbox), 0)

            # Correctly filled in reCaptcha
            response = self.client.post(reverse('feedback'),
                                        {'comment': 'A very long and interesting comment',
                                         'recaptcha_response_field': 'PASSED'})
            self.assertEqual(response.status_code, 302)
            self.assertEqual(len(mail.outbox), 1)
            response = self.client.get(response['Location'])
            self.assertEqual(response.status_code, 200)

    def test_send_feedback_admin(self):
        '''
        Tests the feedback form as an admin user
        '''

        self.user_login('admin')
        self.send_feedback()

    def test_send_feedback_user(self):
        '''
        Tests the feedback form as a regular user
        '''

        self.user_login('test')
        self.send_feedback()

    def test_send_feedback_logged_out(self):
        '''
        Tests the feedback form as a logged out user
        '''

        self.send_feedback(logged_in=False)
