"""
    Common form widgets
    ===================

    This module exposes common form widget classes.

"""

from django.forms.widgets import Select, Widget
from django.utils.dateparse import parse_duration


class ShortDurationSelectWidget(Widget):
    """ A simple Widget allowing to select a short duration (hours and minutes only).

    The maximum durattion that can be set using this widget is limited to 24 hours.

    """

    hours_field = '{}_hours'
    minutes_field = '{}_minutes'
    none_value = ('', '---')
    select_widget = Select
    template_name = 'forms/widgets/short_duration_select_widget.html'

    def get_context(self, name, value, attrs):
        """ Returns the context of the widget to use to render it. """
        context = super().get_context(name, value, attrs)

        try:
            parsed_duration = parse_duration(context['widget']['value'])
            assert parsed_duration is not None
        except (TypeError, AttributeError, AssertionError):
            parsed_hours, parsed_minutes = None, None
        else:
            parsed_hours = parsed_duration.seconds // 3600
            parsed_minutes = (parsed_duration.seconds % 3600) // 60

        hours_choices = [(h, h) for h in range(24)]
        if not self.is_required:
            hours_choices.insert(0, self.none_value)
        hours_name = self.hours_field.format(name)
        context['widget']['hours'] = (
            self.select_widget(attrs, choices=hours_choices)
            .get_context(
                name=hours_name,
                value=parsed_hours,
                attrs={**context['widget']['attrs'], 'id': 'id_{}'.format(hours_name)},
            )
            ['widget']
        )

        minutes_choices = [(m, m) for m in range(60)]
        if not self.is_required:
            minutes_choices.insert(0, self.none_value)
        minutes_name = self.minutes_field.format(name)
        context['widget']['minutes'] = (
            self.select_widget(attrs, choices=minutes_choices)
            .get_context(
                name=minutes_name,
                value=parsed_minutes,
                attrs={**context['widget']['attrs'], 'id': 'id_{}'.format(minutes_name)},
            )
            ['widget']
        )

        return context

    def value_from_datadict(self, data, files, name):
        """ Returns the value extracted from the datadict (and the underlying inputs). """
        hours = data.get(self.hours_field.format(name))
        minutes = data.get(self.minutes_field.format(name))

        if hours == minutes == '':
            return None

        if hours is not None and minutes is not None:
            try:
                return '{:02d}:{:02d}:00'.format(int(hours), int(minutes))
            except ValueError:
                pass

        return super().value_from_datadict(data, files, name)
