proc Ada {args} {
    # ada inputs 0 range first
    # python - split by space then use getattr getattr(ada.Context(), list[index])
    return [python -eval "ada.nuke.utils.parse_tcl_string('$args')"]
}


