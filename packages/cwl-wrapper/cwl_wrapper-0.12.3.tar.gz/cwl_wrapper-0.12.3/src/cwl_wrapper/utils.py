def looking_for(what, cwl):
    if what in cwl:
        return cwl[what]
    else:
        return {}
