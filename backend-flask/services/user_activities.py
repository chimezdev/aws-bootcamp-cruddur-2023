from datetime import datetime, timedelta, timezone
from aws_xray_sdk.core import xray_recorder

class UserActivities:
  def run(user_handle):
    #xray----
    with xray_recorder.in_segment('user_activities') as segment:
      current_user = {"user_handle": "Chimez Andrew"}
      segment.put_metadata('current_user', current_user, 'cruddur')
      model = {
        'errors': None,
        'data': None
      }
      now = datetime.now(timezone.utc)

      #xray----
      with xray_recorder.in_subsegment('hard-coded user') as subsegment:
        if user_handle == None or len(user_handle) < 1:
          model['errors'] = ['blank_user_handle']
        else:
          results = [{
            'uuid': '248959df-3079-4947-b847-9e0892d1bab4',
            'handle':  'Andrew Brown',
            'message': 'Cloud is fun!',
            'created_at': (now - timedelta(days=1)).isoformat(),
            'expires_at': (now + timedelta(days=31)).isoformat()
          }]
          model['data'] = results
          subsegment.put_annotation('Andrew_user', len(results))
      return model