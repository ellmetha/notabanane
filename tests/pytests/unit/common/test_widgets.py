from main.common.widgets import ShortDurationSelectWidget


class TestShortDurationSelectWidget:
    def test_properly_creates_two_select_fields_for_hours_and_minutes(self):
        widget = ShortDurationSelectWidget()
        context = widget.get_context('my_time', None, {})

        assert context['widget']['hours']['name'] == 'my_time_hours'
        assert (
            context['widget']['hours']['optgroups'] ==
            self._generate_optgroups('my_time_hours', 24, required=False)
        )

        assert context['widget']['minutes']['name'] == 'my_time_minutes'
        assert (
            context['widget']['minutes']['optgroups'] ==
            self._generate_optgroups('my_time_minutes', 60, required=False)
        )

    def test_properly_hides_the_additional_options_if_the_input_is_not_required(self):
        widget = ShortDurationSelectWidget()
        widget.is_required = True
        context = widget.get_context('my_time', None, {})

        assert context['widget']['hours']['name'] == 'my_time_hours'
        assert (
            context['widget']['hours']['optgroups'] ==
            self._generate_optgroups('my_time_hours', 24, required=True)
        )
        assert context['widget']['hours']['optgroups'][0][1][0]['label'] == 0

        assert context['widget']['minutes']['name'] == 'my_time_minutes'
        assert (
            context['widget']['minutes']['optgroups'] ==
            self._generate_optgroups('my_time_minutes', 60, required=True)
        )
        assert context['widget']['minutes']['optgroups'][0][1][0]['label'] == 0

    def test_properly_adds_the_additional_options_if_the_input_is_not_required(self):
        widget = ShortDurationSelectWidget()
        context = widget.get_context('my_time', None, {})

        assert context['widget']['hours']['name'] == 'my_time_hours'
        assert (
            context['widget']['hours']['optgroups'] ==
            self._generate_optgroups('my_time_hours', 24, required=False)
        )
        assert context['widget']['hours']['optgroups'][0][1][0]['label'] == '---'

        assert context['widget']['minutes']['name'] == 'my_time_minutes'
        assert (
            context['widget']['minutes']['optgroups'] ==
            self._generate_optgroups('my_time_minutes', 60, required=False)
        )
        assert context['widget']['minutes']['optgroups'][0][1][0]['label'] == '---'

    def test_properly_generates_context_if_the_duration_value_cannot_be_parsed(self):
        widget = ShortDurationSelectWidget()
        context = widget.get_context('my_time', 'dummy', {})

        assert context['widget']['hours']['name'] == 'my_time_hours'
        assert context['widget']['minutes']['name'] == 'my_time_minutes'

    def test_properly_selects_the_right_hours_and_minutes_options_depending_on_the_value(self):
        widget = ShortDurationSelectWidget()
        context = widget.get_context('my_time', '01:40:00', {})

        assert context['widget']['hours']['name'] == 'my_time_hours'
        assert context['widget']['hours']['optgroups'][2][1][0]['selected'] is True

        assert context['widget']['minutes']['name'] == 'my_time_minutes'
        assert context['widget']['minutes']['optgroups'][41][1][0]['selected'] is True

    def test_extract_none_from_the_data_dict_when_the_underlying_input_values_are_blank(self):
        widget = ShortDurationSelectWidget()
        assert widget.value_from_datadict({'t_hours': '', 't_minutes': ''}, {}, 't') is None

    def test_extract_the_formatted_duration_when_the_underlying_input_values_are_not_blank(self):
        widget = ShortDurationSelectWidget()
        assert (
            widget.value_from_datadict({'t_hours': '1', 't_minutes': '40'}, {}, 't') ==
            '01:40:00'
        )

    def test_does_not_extract_values_if_one_input_value_is_blank(self):
        widget = ShortDurationSelectWidget()
        assert widget.value_from_datadict({'t_hours': '1'}, {}, 't') is None

    def test_does_not_extract_values_if_one_input_value_is_not_a_valid_integer(self):
        widget = ShortDurationSelectWidget()
        assert widget.value_from_datadict({'t_hours': '1', 't_minutes': 'dummy'}, {}, 't') is None

    def _generate_optgroups(self, name, count, required=False):
        optgroups = []
        offset = 0
        if not required:
            offset = 1
            optgroups.append((
                None,
                [
                    {
                        'name': name,
                        'value': '',
                        'label': '---',
                        'selected': True,
                        'index': '0',
                        'attrs': {'selected': True},
                        'type': 'select',
                        'template_name': 'django/forms/widgets/select_option.html',
                        'wrap_label': True
                    }
                ],
                0
            ))
        for i in range(count):
            optgroups.append((
                None,
                [
                    {
                        'name': name,
                        'value': i,
                        'label': i,
                        'selected': False,
                        'index': str(i + offset),
                        'attrs': {},
                        'type': 'select',
                        'template_name': 'django/forms/widgets/select_option.html',
                        'wrap_label': True
                    }
                ],
                i + offset
            ))
        return optgroups
