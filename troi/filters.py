import troi


class ArtistCreditFilterElement(troi.Element):
    '''
        Remove recordings if they do or do not belong to a given list of artists.
    '''

    def __init__(self, artist_credit_ids, include=False):
        '''
            Filter a list of Recordings based on their artist_credit_id.
            The default behaviour is to exclude the artists given, but if
            include=True then only the artists in the given list pass
            the filter. Throws RuntimeError is not all recordings have
            artist_credit_ids set.
        '''
        self.artist_credit_ids = artist_credit_ids
        self.include = include

    @staticmethod
    def inputs():
        return [Recording]

    @staticmethod
    def outputs():
        return [Recording]

    def read(self, inputs, debug=False):

        recordings = inputs[0]

        ac_index = {}
        for ac in self.artist_credit_ids:
            try:
                ac_index[ac] = 1
            except KeyError:
                raise RuntimeError(self.__name__ + " needs to have all input recordings to have ac.artist_credit_id defined!")

        results = []
        for r in recordings:
            if not r.artist or not r.artist.artist_credit_id:
                if debug:
                    print("- debug recording %s has not artist credit id" % (r.mbid))
                continue

            if self.include:
                if r.artist.artist_credit_id in ac_index:
                    results.append(r)
            else:
                if r.artist.artist_credit_id not in ac_index:
                    results.append(r)

        return results


class ArtistCreditLimiterElement(troi.Element):

    def __init__(self, limit=2, exclude_lower_ranked=True):
        '''
            This element examines there passed in recordings and if the count of
            recordings by any one artists exceeds the given limit, excessive recordigns
            are removed. If the flag exclude_lower_ranked is True, then the lowest
            ranked recordings are removed, otherwise the highest ranked recordings
            are removed. Throws RuntimeError is not all recordings have
            artist_credit_ids set.
        '''
        self.limit = limit
        self.exclude_lower_ranked = exclude_lower_ranked

    @staticmethod
    def inputs():
        return [Recording]

    @staticmethod
    def outputs():
        return [Recording]

    def read(self, inputs, debug=False):

        recordings = inputs[0]

        ac_index = {}
        for ac in self.artist_credit_ids:
            try:
                ac_index[ac] = 1
            except KeyError:
                raise RuntimeError(self.__name__ + " needs to have all input recordings to have ac.artist_credit_id defined!")

        results = []
        for r in recordings:
            if not r.artist or not r.artist.artist_credit_id:
                if debug:
                    print("- debug recording %s has not artist credit id" % (r.mbid))
                continue

            if self.include:
                if r.artist.artist_credit_id in ac_index:
                    results.append(r)
            else:
                if r.artist.artist_credit_id not in ac_index:
                    results.append(r)

        return results
