from datetime import timezone

"""
Changes default timezone which will be used
in database. Does not change already created tuples.
Used for most db entity creation. 
"""

prefered_timezone = timezone.utc
