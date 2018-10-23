def export_row(answer):
    obj = answer.answers
    obj['created_at'] = answer.created_at
    obj['updated_at'] = answer.updated_at
    return obj
