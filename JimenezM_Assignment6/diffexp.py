# diffexp.py

class DiffExp:
    """Collection of Differential Expression info from .matrix file
    Args:
        transcript_info(string): One differential expression informtation.
    Attributes:
        transcript(str):
        sp_ds(float): diauxic shift
        sp_hs(float): heat shock
        sp_log(float): logarithmic growth
        sp_plat(float): plateau phase
    Methods:
        data_attributes: Return the data sample attributes as a tuple
    """

    def __init__(self, transcript_info):
        self.transcript_info = transcript_info
        self.transcript, self.sp_ds, self.sp_hs, self.sp_log, self.sp_plat \
            = transcript_info.rstrip().split("\t")

    def __repr__(self):
        return f"DiffExp({self.transcript_info})"

    def data_attributes(self):
        """Return tuple that contains data sample attributes"""

        return (self.sp_ds, self.sp_hs, self.sp_log, self.sp_plat)
