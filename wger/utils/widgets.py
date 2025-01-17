# -*- coding: utf-8 -*-

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
import uuid
from itertools import chain

from django.forms.widgets import SelectMultiple

from django.utils.translation import ugettext as _
from django.utils.encoding import force_unicode
from django.utils.html import escape
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe


class ExerciseAjaxSelect(SelectMultiple):
    '''
    Custom widget that allows to select exercises from an autocompleter

    This is basically modified MultipleSelect widget
    '''

    def render(self, name, value, attrs=None, choices=()):
        if value is None:
            value = []
        final_attrs = self.build_attrs(attrs, name=name)

        output = [u'<div class="ym-fbox-text">']
        output.append(u'<input type="text" id="exercise-search">')
        output.append(u'</div>')

        output.append('<div id="exercise-search-log">')
        options = self.render_options(choices, value)
        if options:
            output.append(options)
        output.append('</div>')

        return mark_safe(u'\n'.join(output))

    def render_options(self, choices, selected_choices):
        # Normalize to strings.
        selected_choices = set(force_unicode(v) for v in selected_choices)
        output = []
        for option_value, option_label in chain(self.choices, choices):
            output.append(self.render_option(selected_choices, option_value, option_label))
        return u'\n'.join(output)

    def render_option(self, selected_choices, option_value, option_label):
        option_value = force_unicode(option_value)
        if option_value in selected_choices:

            return u'''
                    <div id="a%(div_id)s" class="ajax-exercise-select">
                        <a href="#">
                        <img src="/static/images/icons/status-off.svg"
                             width="14"
                             height="14"
                             alt="Delete">
                        </a> %(value)s
                        <input type="hidden" name="exercises" value="%(id)s">
                    </div>
            ''' % {'value': conditional_escape(force_unicode(option_label)),
                   'id': escape(option_value),
                   'div_id': uuid.uuid4()}

        else:
            return ''


class TranslatedSelectMultiple(SelectMultiple):
    '''
    A SelectMultiple widget that translates the options
    '''

    def render_option(self, selected_choices, option_value, option_label):
        return super(TranslatedSelectMultiple, self).render_option(selected_choices,
                                                                   option_value,
                                                                   _(option_label))
