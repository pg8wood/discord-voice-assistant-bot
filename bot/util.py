def time_string(seconds):
    """
    Gets a string representing the number of seconds in hours, minutes, and seconds,
    but will not print leading zeroes.  
    """
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)

    hour_string = "%dh " % hours if hours > 0 else ""
    minute_string = "%dm " % minutes if minutes > 0 else ""
    second_string = "%ds" % seconds if seconds > 0 else ""

    return "%s%s%s" % (hour_string, minute_string, second_string)
