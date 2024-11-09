from tethys_sdk.base import TethysAppBase


class PopulationApp(TethysAppBase):
    """
    Tethys app class for Population App.
    """

    name = 'Population App'
    description = ''
    package = 'population_app'  # WARNING: Do not change this value
    index = 'home'
    icon = f'{package}/images/population_tracker_logo.png'
    root_url = 'population-app'
    color = '#718093'
    tags = ''
    enable_feedback = False
    feedback_emails = []