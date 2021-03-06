from opendc.models.experiment import Experiment
from opendc.models.room_state import RoomState
from opendc.util import database, exceptions
from opendc.util.rest import Response

def GET(request):
    """Get this Experiment's Room States."""

    # Make sure required parameters are there

    try:
        request.check_required_parameters(
            path = {
                'simulationId': 'int',
                'experimentId': 'int'
            }
        )

    except exceptions.ParameterError as e:
        return Response(400, e.message)

    # Instantiate an Experiment from the database

    experiment = Experiment.from_primary_key((request.params_path['experimentId'],))

    # Make sure this Experiment exisits

    if not experiment.exists():
        return Response(404, '{} not found.'.format(experiment))

    # Make sure this user is authorized to view this Experiment's Room States

    if not experiment.google_id_has_at_least(request.google_id, 'VIEW'):
        return Response(403, 'Forbidden from viewing Room States for {}.'.format(experiment))

    # Get and return the Room States

    if 'tick' in request.params_query:
        room_states = RoomState.from_experiment_id_and_tick(
            request.params_path['experimentId'],
            request.params_query['tick']
        )

    else:
        room_states = RoomState.from_experiment_id(request.params_path['experimentId'])

    return Response(
        200,
        'Successfully retrieved Room States for {}.'.format(experiment),
        [x.to_JSON() for x in room_states]
    )
