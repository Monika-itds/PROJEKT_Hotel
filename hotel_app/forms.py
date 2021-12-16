from django import forms

class AvailabilityForm(forms.Form):
    ROOM_CATEGORIES = (
        ('STA', 'standard'),
        ('DEL', 'deluxe'),
        ('SUP', 'superior'),
        ('PRE', 'prezydencki'),
        ('KIN', 'królewski')
    )
    room_category = forms.ChoiceField(choices=ROOM_CATEGORIES, required=True)
    check_in = forms.DateTimeField(required=True, input_formats=["%Y-%m-%dT%H:%M", ])
    check_out = forms.DateTimeField(required=True, input_formats=["%Y-%m-%dT%H:%M", ])