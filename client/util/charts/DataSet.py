from datetime import timedelta


class DataSet:
    def __init__(self, from_data=None):
        self._x = []
        self._ys = []
        self._start_date = None
        self._date_type = 'day'

        self.pull_from_existing_data_set(from_data=from_data)

    '''Deserialize information from an external data set dictionary'''
    def pull_from_existing_data_set(self, from_data=None):
        if from_data is not None and isinstance(from_data, dict):
            if 'x' in from_data:
                self.set_x(from_data['x'])

            if 'ys' in from_data:
                self.set_ys(from_data['ys'])

            if 'start_date' in from_data:
                if 'date_type' in from_data:
                    self.set_start_date(start_date=from_data['start_date'], date_type=from_data['date_type'])
                else:
                    self.set_start_date(start_date=from_data['start_date'])

    def set_x(self, x):
        self._x = x

    def set_ys(self, ys):
        self._ys = ys

    def append_y_set(self, y):
        self._ys.append(y)

    '''
        Set the start date if a date series is to be used with the y data sets
        optionally specify the date_type (possible types: hour, day, week, month, year, financial)
    '''
    def set_start_date(self, start_date=None, date_type='day'):
        self._start_date = start_date
        self._date_type = date_type

    '''Get the serialized data dictionary for use in charts'''
    def get_data_dict(self):
        if len(self._x) == 0:
            self.generate_x()

        return {
            'x': self._x,
            'ys': self._ys
        }

    def generate_x(self):
        data_len = len(self._ys[0]['data'])
        if self._start_date is not None:
            if self._date_type == 'hour':
                self._x = [str(self._start_date + timedelta(hours=x)) for x in range(data_len)]
            elif self._date_type == 'week':
                self._x = [str(self._start_date + timedelta(weeks=x)) for x in range(data_len)]
            elif self._date_type == 'months':
                self._x = [str(self._start_date + timedelta(weeks=x*4)) for x in range(data_len)]
            elif self._date_type == 'year':
                self._x = [str(self._start_date + timedelta(weeks=x*52)) for x in range(data_len)]
            else:
                self._x = [str(self._start_date + timedelta(days=x)) for x in range(data_len)]
        else:
            self._x = range(0, data_len)
