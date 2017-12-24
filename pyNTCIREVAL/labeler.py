class Labeler(dict):
    """
    Output a ranked list of documents with a relevance level
    by considering the args j and truncate for the 'compute' command

    Args:
        qrels: a dict of a document ID and a relevance level
        is_condensed: if True, treat the input as a condensed list (unjudged docs removed)
        truncate: truncate a ranked list at <truncate> if specified
    """

    def __init__(self, qrels, truncate=None, is_condensed=False):
        super(Labeler, self).__init__(qrels)
        self.truncate = truncate
        self.is_condensed = is_condensed

    def label(self, sysdocs):
        '''
        Output a ranked list of documents with a relevance level
        by considering the truncate and is_condensed options

        Args:
            sysdocs: a ranked list of document IDs.

        Returns:
            A ranked list of tuples of a document ID and a relevance level (int).
        '''
        result = []
        for idx, did in enumerate(sysdocs):
            grade = self.get(did, None)
            if self.is_condensed and grade is None:
                pass # do not output documents without rel judge
            else:
                result.append((did, grade))
            if self.truncate is not None and len(result) >= self.truncate:
                break
        return result
