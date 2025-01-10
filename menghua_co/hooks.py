app_name = "menghua_co"
app_title = "Menghua Co"
app_publisher = "Ecosoft"
app_description = "Menghua Co\'s ERP"
app_email = "kittiu@ecosoft.co.th"
app_license = "mit"
required_apps = ["frappe/erpnext", "frappe/hrms", "ecosoft-frappe/erpnext_thailand", "kittiu/cash_holder_summary"]

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "menghua_co",
# 		"logo": "/assets/menghua_co/logo.png",
# 		"title": "Menghua Co",
# 		"route": "/menghua_co",
# 		"has_permission": "menghua_co.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/menghua_co/css/menghua_co.css"
# app_include_js = "/assets/menghua_co/js/menghua_co.js"

# include js, css files in header of web template
# web_include_css = "/assets/menghua_co/css/menghua_co.css"
# web_include_js = "/assets/menghua_co/js/menghua_co.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "menghua_co/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "menghua_co/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "menghua_co.utils.jinja_methods",
# 	"filters": "menghua_co.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "menghua_co.install.before_install"
# after_install = "menghua_co.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "menghua_co.uninstall.before_uninstall"
# after_uninstall = "menghua_co.uninstall.after_uninstall"

after_migrate = ["menghua_co.custom.print_format_setting.set_print_format_as_disable"]

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "menghua_co.utils.before_app_install"
# after_app_install = "menghua_co.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "menghua_co.utils.before_app_uninstall"
# after_app_uninstall = "menghua_co.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "menghua_co.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"menghua_co.tasks.all"
# 	],
# 	"daily": [
# 		"menghua_co.tasks.daily"
# 	],
# 	"hourly": [
# 		"menghua_co.tasks.hourly"
# 	],
# 	"weekly": [
# 		"menghua_co.tasks.weekly"
# 	],
# 	"monthly": [
# 		"menghua_co.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "menghua_co.install.before_tests"

# Overriding Methods
# ------------------------------
#
override_whitelisted_methods = {
	"erpnext.selling.doctype.quotation.quotation.make_sales_order": "menghua_co.custom.quotation.make_sales_order"
}
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "menghua_co.task.get_dashboard_data"
# }
override_doctype_dashboards = {
	"Sales Order": "menghua_co.custom.dashboard_overrides.get_dashboard_data_for_sales_order",
	"Work Order": "menghua_co.custom.dashboard_overrides.get_dashboard_data_for_work_order",
	"Material Request": "menghua_co.custom.dashboard_overrides.get_dashboard_data_for_material_request",
}
# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]
# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["menghua_co.utils.before_request"]
# after_request = ["menghua_co.utils.after_request"]

# Job Events
# ----------
# before_job = ["menghua_co.utils.before_job"]
# after_job = ["menghua_co.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"menghua_co.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

doctype_js = {
    "Sales Order": "public/js/sales_order.js",
    "Quotation": "public/js/quotation.js",
    "Work Order": "public/js/work_order.js",
    "Purchase Invoice":"public/js/purchase_invoice.js",
}

doc_events = {
    "Work Order": {
        "after_insert": "menghua_co.custom.work_order.auto_create_manufacturing_order"
    },
    "Material Request": {
        "before_insert": "menghua_co.custom.material_request.set_created_by_full_name"
    }
}

fixtures = [
    {"dt": "Property Setter", "filters": [
        [
            "name", "in", [
                "Purchase Order Item-item_name-in_list_view",
                "Purchase Order Item-rate-columns",
                "Purchase Order Item-amount-columns",
                "Purchase Order Item-received_qty-in_list_view",
                "Purchase Order Item-received_qty-columns",
                "Purchase Order Item-warehouse-in_list_view",
                "Purchase Order Item-item_name-columns",
                "Purchase Order Item-schedule_date-columns",
                "Quotation Item-item_code-columns",
                "Quotation Item-description-in_list_view",
                "Quotation Item-description-columns",
                "Quotation Item-qty-columns",
                "Quotation Item-uom-columns",
                "Quotation Item-actual_qty-columns",
                "Quotation Item-rate-columns",
                "Quotation Item-actual_qty-in_list_view",
                "Sales Order Item-item_code-columns",
                "Sales Order Item-actual_qty-in_list_view",
                "Sales Order Item-rate-columns",
                "Sales Order Item-warehouse-in_list_view",
                "Purchase Invoice-supplier_invoice_details-collapsible",
                "Address-address_type-description",
                "Address-address_title-description",
                "Address-address_line1-description",
                "Address-address_line2-description",
                "Address-city-description",
                "Address-county-description",
                "Address-state-description",
                "Address-country-description",
                "Address-pincode-description",
                "Address-email_id-description",
                "Address-phone-description",
                "Address-fax-description",
                "Expense Claim Detail-amount-columns",
                "Expense Claim Detail-description-columns",
                "Material Request-title-in_list_view",
                "Material Request-workflow_state",
                "Material Request-main-title_field",
                "Sales Invoice-payment_terms_template-allow_on_submit",
                "Sales Invoice-payment_schedule-allow_on_submit",
            ]
        ]
    ]},
    {"dt": "Custom Field", "filters": [
        [
            "name", "in", [
                "Sales Order-custom_mh_order_type",
                "Quotation-custom_mh_order_type",
                "Company-custom_mh_setting",
                "Company-auto_mo_from_so",
                "Company-auto_mo_from_mr",
                "Company-custom_column_checkbox",
                "Quotation-custom_delivery_date",
                "Warehouse-custom_mh_detail",
                "Warehouse-custom_lock",
                "Warehouse-custom_row",
                "Warehouse-custom_column_break_mh_detail",
                "Warehouse-custom_shelf",
                "Warehouse-custom_block",
                "Work Order-custom_section_break_bqfoz",
                "Work Order-custom_note",
                "Expense Claim Detail-custom_section_break_shipping",
                "Expense Claim Detail-custom_shipping",
                "Expense Claim Detail-custom_column_break_shippingg",
                "Expense Claim Detail-custom_customer",
                "Address-contact",
                "Material Request-created_by",
                "Manufacturing Order-custom_section_break_yvi1r",
                "Manufacturing Order-custom_mo_printed",
            ]
        ]
    ]}
]