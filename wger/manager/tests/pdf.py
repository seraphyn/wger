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

from wger.manager.tests.testcase import WorkoutManagerTestCase


class WorkoutPdfExportTestCase(WorkoutManagerTestCase):
    '''
    Tests exporting a workout as a pdf
    '''

    def export_pdf(self, fail=False):
        '''
        Helper function to test exporting a workout as a pdf
        '''

        # Create a workout
        response = self.client.get(reverse('wger.manager.pdf.workout_log', kwargs={'id': 3}))

        if fail:
            self.assertIn(response.status_code, (404, 302))
        else:
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response['Content-Type'], 'application/pdf')
            self.assertEqual(response['Content-Disposition'], 'attachment; filename=Workout.pdf')

            # Approximate size, there's a timestamp in the document
            self.assertGreater(len(response.content), 3200)

    def test_export_pdf_anonymous(self):
        '''
        Tests exporting a workout as a pdf as an anonymous user
        '''

        self.export_pdf(fail=True)

    def test_export_pdf_owner(self):
        '''
        Tests exporting a workout as a pdf as the owner user
        '''

        self.user_login('test')
        self.export_pdf(fail=False)

    def test_export_pdf_other(self):
        '''
        Tests exporting a workout as a pdf as a logged user not owning the data
        '''

        self.user_login('admin')
        self.export_pdf(fail=True)
