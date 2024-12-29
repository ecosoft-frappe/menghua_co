from frappe import _


def get_dashboard_data_for_sales_order(data):
    data["non_standard_fieldnames"].update({
        "Sales Order": "sales_order",
    })
    for transaction in data["transactions"]:
        if transaction["label"] == _("Manufacturing"):
            transaction["items"].append("Manufacturing Order")
    return data


def get_dashboard_data_for_work_order(data):
    data["non_standard_fieldnames"].update({
        "Work Order": "work_order",
    })
    data["internal_links"].update({
        "Material Request": "material_request",
    })
    for transaction in data["transactions"]:
        if transaction["label"] == _("Reference"):
            transaction["items"].append("Manufacturing Order")
    return data


def get_dashboard_data_for_material_request(data):
    data["non_standard_fieldnames"].update({
        "Material Request": "material_request",
    })
    for transaction in data["transactions"]:
        if transaction["label"] == _("Manufacturing"):
            transaction["items"].append("Manufacturing Order")
    return data