import os

COMPANY_SUPPLIERS_ROUTE = "/companies/{id}/suppliers"
SUPPLIER_ITEM_ROUTE = "supplier"
SUPPLIER_ITEM_RUNNING_ORDERS_ROUTE = "supplier_running_orders"
SUPPLIER_ITEM_INVOICED_ORDERS_ROUTE = "supplier_invoiced_orders"
SUPPLIER_ITEM_INVOICES_ROUTE = "/suppliers/{id}/invoices"
SUPPLIER_ITEM_INVOICES_EXPORT_ROUTE = SUPPLIER_ITEM_INVOICES_ROUTE + ".{extension}"
COMPANY_SUPPLIERS_ADD_ROUTE = os.path.join(COMPANY_SUPPLIERS_ROUTE, "add")

API_COMPANY_SUPPLIERS_ROUTE = "/api/v1/companies/{id}/suppliers"
SUPPLIER_REST_ROUTE = "/api/v1/suppliers/{id}"
SUPPLIER_STATUS_LOG_ROUTE = "/api/v1/suppliers/{id}/statuslogentries"
SUPPLIER_STATUS_LOG_ITEM_ROUTE = "/api/v1/suppliers/{eid}/statuslogentries/{id}"


def includemeZZZ(config):
    route = API_COMPANY_SUPPLIERS_ROUTE
    pattern = r"{}".format(route.replace("id", r"id:\d+"))
    config.add_route(
        route,
        pattern,
        traverse="/companies/{id}",
    )

    config.add_route(
        SUPPLIER_ITEM_ROUTE,
        r"/suppliers/{id:\d+}",
        traverse="/suppliers/{id}",
    )

    config.add_route(
        SUPPLIER_ITEM_RUNNING_ORDERS_ROUTE,
        r"/suppliers/{id:\d+}/running_orders",
        traverse="/suppliers/{id}",
    )
    config.add_route(
        SUPPLIER_ITEM_INVOICED_ORDERS_ROUTE,
        r"/suppliers/{id:\d+}/invoiced_orders",
        traverse="/suppliers/{id}",
    )

    for route in (
        SUPPLIER_REST_ROUTE,
        SUPPLIER_ITEM_ESTIMATION_ROUTE,
        SUPPLIER_ITEM_INVOICE_ROUTE,
        SUPPLIER_ITEM_INVOICE_EXPORT_ROUTE,
        SUPPLIER_STATUS_LOG_ROUTE,
    ):
        pattern = r"{}".format(route.replace("id", r"id:\d+"))
        config.add_route(
            route,
            pattern,
            traverse="/suppliers/{id}",
        )

    route = SUPPLIER_STATUS_LOG_ITEM_ROUTE
    pattern = r"{}".format(route.replace("id", r"id:\d+"))
    config.add_route(
        route,
        pattern,
        traverse="/statuslogentries/{id}",
    )

    for route in (COMPANY_SUPPLIERS_ROUTE, COMPANY_SUPPLIERS_ADD_ROUTE):
        pattern = r"{}".format(route.replace("id", r"id:\d+"))
        config.add_route(route, pattern, traverse="/companies/{id}")

    config.add_route(
        "suppliers.csv", r"/company/{id:\d+}/suppliers.csv", traverse="/companies/{id}"
    )


def includeme(config):
    config.add_route(
        "supplier",
        "/suppliers/{id}",
        traverse="/suppliers/{id}",
    )
    config.add_route(
        "supplier_running_orders",
        "/suppliers/{id}/running_orders",
        traverse="/suppliers/{id}",
    )

    config.add_route(
        "supplier_invoiced_orders",
        "/suppliers/{id}/invoiced_orders",
        traverse="/suppliers/{id}",
    )
    config.add_route(
        "supplier_invoices",
        "/suppliers/{id}/invoices",
        traverse="/suppliers/{id}",
    )

    config.add_route(
        "supplier_expenselines",
        "/suppliers/{id}/expenselines",
        traverse="/suppliers/{id}",
    )

    config.add_route(
        "/api/v1/companies/{id}/suppliers",
        "/api/v1/companies/{id}/suppliers",
        traverse="/companies/{id}",
    )
    config.add_route(
        "/api/v1/suppliers/{id}",
        "/api/v1/suppliers/{id}",
        traverse="/suppliers/{id}",
    )

    config.add_route(
        "/api/v1/suppliers/{id}/statuslogentries",
        r"/api/v1/suppliers/{id:\d+}/statuslogentries",
        traverse="/suppliers/{id}",
    )

    config.add_route(
        "/api/v1/suppliers/{eid}/statuslogentries/{id}",
        r"/api/v1/suppliers/{eid:\d+}/statuslogentries/{id:\d+}",
        traverse="/statuslogentries/{id}",
    )

    config.add_route(
        "company_suppliers",
        r"/company/{id:\d+}/suppliers",
        traverse="/companies/{id}",
    )

    config.add_route(
        "suppliers.csv", r"/company/{id:\d+}/suppliers.csv", traverse="/companies/{id}"
    )
    for i in range(2):
        index = i + 1
        route_name = "company_suppliers_import_step%d" % index
        path = r"/company/{id:\d+}/suppliers/import/%d" % index
        config.add_route(route_name, path, traverse="/companies/{id}")
